import copy
from pathlib import Path

import torch

from .. import device
from ..equations import pde_1d_heat
from ..nets.training_tools import OptimizerData
from ..pinns.pinn_losses import PinnLossesData
from ..sampling import (
    sampling_functions,
    sampling_ode,
    sampling_parameters,
    sampling_pde,
    uniform_sampling,
)
from ..sampling.data_sampling_pde_tx import (
    pde_loss_evaluation,
    pde_loss_evaluation_bc,
    pde_loss_evaluation_ini,
    pde_tx_data,
)
from scimba.nets import training


class TrainerPINOSpaceTime(training.AbstractTrainer):
    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, **kwargs):
        self.pde = kwargs.get("pde", pde_1d_heat.HeatEquation())

        self.network = kwargs.get("network", None)
        if self.network is None:
            raise ValueError("network must be provided to TrainerPINOSpaceTime")

        self.sampler = kwargs.get("sampler", None)

        if self.sampler is None:
            x_usampler = sampling_pde.XSampler(self.pde)
            t_usampler = sampling_ode.TSampler(
                sampler=uniform_sampling.UniformSampling, ode=self.pde
            )
            mu_usampler = sampling_parameters.MuSampler(
                sampler=uniform_sampling.UniformSampling, model=self.pde
            )
            self.sampler = pde_tx_data(
                sampler_t=t_usampler,
                sampler_x=x_usampler,
                sampler_params=mu_usampler,
                source=sampling_functions.Default_ParametricFunction_tx(),
                boundary=sampling_functions.Default_ParametricFunction_x(),
                initial=sampling_functions.Default_ParametricFunction_x(),
                n_sensor=70,
                n_sensor_bc=40,
                n_sensor_ini=30,
                resample_sensors=False,
            )

        self.optimizers = kwargs.get("optimizers", OptimizerData(**kwargs))
        self.losses = kwargs.get("losses", PinnLossesData(**kwargs))
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.pde.file_name)
        self.file_name = folder_for_saved_networks / file_name
        self.batch_size = kwargs.get("batch_size", 1000)

        self.create_network()
        print(">> load network", self.file_name)
        self.load(self.file_name)

        self.to_be_trained = kwargs.get("to_be_trained", self.to_be_trained)
        self.pre_training = True
        self.post_training = False

    def residual(
        self,
        sample: pde_loss_evaluation,
        sample_bc: pde_loss_evaluation_bc,
        sample_ini: pde_loss_evaluation_ini,
        f: torch.tensor,
    ) -> torch.Tensor:
        """Compute the PDE residual from samples, at inner points.

        :param sample: sample for the inner domain
        :type sample: pde_loss_evaluation
        :param sample_bc: sample for the boundary condition
        :type sample_bc: pde_loss_evaluation_bc
        :param sample_ini: sample for the initial condition
        :type sample_ini: pde_loss_evaluation_ini
        :param f: sampled values of f, at inner points
        :type f: torch.Tensor
        :return: the residual of the PDE at the sampled points
        :rtype: torch.Tensor
        """

        # compute w and its derivatives
        t, x, mu = sample.t_loss, sample.x_loss, sample.params
        w = self.network.setup_w_dict(t, x, mu, sample, sample_bc, sample_ini)
        self.network.get_first_derivatives(w, t, x)

        if self.pde.second_derivative_t:
            self.network.get_second_derivatives_t(w, t)
        if self.pde.second_derivative_x:
            self.network.get_second_derivatives_x(w, x)

        # compute the PDE residual and concatenate it, if needed
        pde_residual = self.pde.residual(w, t, x, mu, f=f)
        if isinstance(pde_residual, torch.Tensor):
            return pde_residual
        elif isinstance(pde_residual, tuple):
            return torch.cat(pde_residual, axis=0)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def bc_residual(
        self,
        sample: pde_loss_evaluation,
        sample_bc: pde_loss_evaluation_bc,
        sample_ini: pde_loss_evaluation_ini,
        f: torch.tensor,
    ) -> torch.Tensor:
        """Compute the PDE residual from samples, at boundary points.

        :param sample: sample for the inner domain
        :type sample: pde_loss_evaluation
        :param sample_bc: sample for the boundary condition
        :type sample_bc: pde_loss_evaluation_bc
        :param sample_ini: sample for the initial condition
        :type sample_ini: pde_loss_evaluation_ini
        :param f: sampled values of f, at boundary points
        :type f: torch.Tensor
        :return: the residual of the PDE at the sampled points
        :rtype: torch.Tensor
        """

        # compute w and its derivatives
        t, x, mu = sample_bc.t_loss_bc, sample_bc.x_loss_bc, sample_bc.params_bc
        w = self.network.setup_w_dict(t, x, mu, sample, sample_bc, sample_ini)
        self.network.get_first_derivatives(w, t, x)

        # compute the PDE boundary residual and concatenate it, if needed
        pde_bc_residual = self.pde.bc_residual(w, t, x, mu)
        if isinstance(pde_bc_residual, torch.Tensor):
            return pde_bc_residual
        elif isinstance(pde_bc_residual, tuple):
            return torch.cat(pde_bc_residual, axis=1)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def ini_residual(
        self,
        sample: pde_loss_evaluation,
        sample_bc: pde_loss_evaluation_bc,
        sample_ini: pde_loss_evaluation_ini,
        f: torch.tensor,
    ) -> torch.Tensor:
        """Compute the PDE residual from samples, at initial points.

        :param sample: sample for the inner domain
        :type sample: pde_loss_evaluation
        :param sample_bc: sample for the boundary condition
        :type sample_bc: pde_loss_evaluation_bc
        :param sample_ini: sample for the initial condition
        :type sample_ini: pde_loss_evaluation_ini
        :param f: sampled values of f, at initial points
        :type f: torch.Tensor
        :return: the residual of the PDE at the sampled points
        :rtype: torch.Tensor
        """

        # compute w and its derivatives
        t, x, mu = sample_ini.t_loss_ini, sample_ini.x_loss_ini, sample_ini.params_ini
        w = self.network.setup_w_dict(t, x, mu, sample, sample_bc, sample_ini)
        self.network.get_first_derivatives(w, t, x)

        # compute the PDE boundary residual and concatenate it, if needed
        pde_ini_residual = self.pde.initial_condition(x, mu) - w["w"]
        return pde_ini_residual
    
    def apply_pre_training(self, **kwargs):
        n_data_f = kwargs.get("n_data_f", 0)
        n_data_tx = kwargs.get("n_data_tx", 0)

        if n_data_f > 0 or n_data_tx > 0:
            self.data_sample = self.pde.make_data(n_data_tx)

    def apply_post_training(self, **kwargs):
        pass

    
    def create_batch_data(self,**kwargs):
        n_collocation = kwargs.get("n_collocation_tx", 1_000)
        n_data = kwargs.get("n_data_tx", 0)
        if n_collocation == 0:
            m = self.input_t.size()[0]
        if n_data == 0:
            m = n_collocation
        if n_data > 0 and n_collocation > 0:
            m = min(self.input_t.size()[0], n_collocation)
        return m,torch.randperm(m)

    def evaluate_losses(self,epoch,step, **kwargs):
        n_simu = kwargs.get("n_simu", 10)
        n_collocation_tx = kwargs.get("n_collocation_x", 200)
        n_bc_collocation_tx = kwargs.get("n_bc_collocation_tx", 0)
        n_ini_collocation_x = kwargs.get("n_ini_collocation_x", 0)
       
        if n_simu > 0 and n_collocation_tx > 0:
            sample, f_loss, sample_bc, f_loss_bc, sample_ini, f_loss_ini = (
                self.sampler.sampling(n_collocation_tx, n_simu)
            )
            f_out = self.residual(sample, sample_bc, sample_ini, f_loss)
            zeros = torch.zeros_like(f_out)
            self.losses.update_residual_loss(
                self.losses.residual_f_loss(f_out, zeros)
            )

            # Check this part in case the BC are not hardly imposed
        if self.losses.bc_loss_bool:
            sample, f_loss, sample_bc, f_loss_bc, sample_ini, f_loss_ini = (
                self.sampler.sampling(n_bc_collocation_tx, n_simu)
            )
            bc_residual = self.bc_residual(
                sample, sample_bc, sample_ini, f_loss_bc
            )
            bc_zeros = torch.zeros_like(bc_residual)
            self.losses.update_bc_loss(
                self.losses.bc_f_loss(bc_residual, bc_zeros)
            )

        if self.losses.init_loss_bool:
            sample, f_loss, sample_bc, f_loss_bc, sample_ini, f_loss_ini = (
                self.sampler.sampling(n_ini_collocation_x, n_simu)
            )
            ini_residual = self.bc_residual(
                sample, sample_bc, sample_ini, f_loss_bc
            )
            ini_zeros = torch.zeros_like(ini_residual)
            self.losses.update_init_loss(
                self.losses.init_f_loss(ini_residual, ini_zeros)
            )

        if self.losses.data_loss_bool:
            indices = self.permutation[step : step + self.batch_size]
            masked_sample = self.data_sample[indices]
            prediction = self.network.get_w(masked_sample)
            self.losses.update_data_loss(
                self.losses.data_f_loss(prediction, masked_sample)
            )

            
    def plot(self, random=False, n_visu=1_000, reference_solution=None):
        import matplotlib.pyplot as plt

        _, ax = plt.subplots(1, 3, figsize=(15, 5))
        ax[0] = self.losses.plot(ax[0])

        n_visu = n_visu

        sample, f_loss, sample_bc, _, sample_ini, __ = self.sampler.sampling(n_visu, 1)

        end_time = self.pde.time_domain[1]
        t = end_time * torch.ones_like(sample.t_loss)

        mu = sample.params[0, 0] * torch.ones_like(sample.params)

        x = sample.x_loss
        x_ = x.get_coordinates()[:, 0]

        parameter_string = ", ".join(
            [f"{mu[0, i].detach().cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        if reference_solution is None:
            reference_solution = self.pde.reference_solution

        w_pred = self.network.setup_w_dict(t, x, mu, sample, sample_bc, sample_ini)
        w_pred = w_pred["w"][:, 0]
        w_ex = reference_solution(t, x, mu)[:, 0]

        ax[1].scatter(x_.detach().cpu(), w_ex.detach().cpu(), label="exact")
        ax[1].scatter(x_.detach().cpu(), w_pred.detach().cpu(), label="prediction")

        ax[1].set_title(f"prediction, parameters = {parameter_string}")
        ax[1].legend()

        error = torch.abs(w_pred - w_ex).detach().cpu()

        ax[2].scatter(x_.detach().cpu(), error)
        ax[2].set_title("prediction error")

        plt.show()
