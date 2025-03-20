import copy
from pathlib import Path

import torch

from .. import device
from ..equations import pde_1d_laplacian
from ..nets.training_tools import OptimizerData
from ..pinns.pinn_losses import PinnLossesData
from ..sampling import (
    sampling_functions,
    sampling_parameters,
    sampling_pde,
    uniform_sampling,
)
from ..sampling.data_sampling_pde_x import (
    pde_loss_evaluation,
    pde_loss_evaluation_bc,
    pde_x_data,
)
from ..nets import training


class TrainerPINOSpace(training.AbstractTrainer):
    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, **kwargs):
        self.pde = kwargs.get("pde", pde_1d_laplacian.LaplacianSine(k=1))

        self.network = kwargs.get("network", None)
        if self.network is None:
            raise ValueError("network must be provided to TrainerPINOSpace")

        self.sampler = kwargs.get("sampler", None)

        if self.sampler is None:
            x_usampler = sampling_pde.XSampler(self.pde)
            mu_usampler = sampling_parameters.MuSampler(
                sampler=uniform_sampling.UniformSampling, model=self.pde
            )
            self.sampler = pde_x_data(
                sampler_x=x_usampler,
                sampler_params=mu_usampler,
                source=sampling_functions.Default_ParametricFunction_x(),
                boundary=sampling_functions.Default_ParametricFunction_x(),
                n_sensor=70,
                n_sensor_bc=40,
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
        self.pre_training=True
        self.post_training = False


    def residual(
        self,
        sample: pde_loss_evaluation,
        sample_bc: pde_loss_evaluation_bc,
        f: torch.tensor,
    ) -> torch.tensor:
        x, mu = sample.x_loss, sample.params

        w = self.network.setup_w_dict(x, mu, sample, sample_bc)
        self.network.get_first_derivatives(w, x)

        if self.pde.second_derivative:
            self.network.get_second_derivatives(w, x)

        # compute the PDE residual and concatenate it, if needed
        pde_residual = self.pde.residual(w, x, mu, f=f)
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
        f_bc: torch.tensor,
    ) -> torch.tensor:
        mu, x = sample_bc.params_bc, sample_bc.x_loss_bc
        # compute w and its derivative
        w = self.network.setup_w_dict(x, mu, sample, sample_bc)
        self.network.get_first_derivatives(w, x)

        # compute the PDE boundary residual and concatenate it, if needed
        pde_bc_residual = self.pde.bc_residual(w, x, mu, f=f_bc)
        if isinstance(pde_bc_residual, torch.Tensor):
            return pde_bc_residual
        elif isinstance(pde_bc_residual, tuple):
            return torch.cat(pde_bc_residual, axis=1)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")


    def apply_pre_training(self, **kwargs):
        n_data_f = kwargs.get("n_data_f", 0)
        n_data_x = kwargs.get("n_data_x", 0)

        if n_data_f > 0 or n_data_x > 0:
            self.data_sample = self.pde.make_data(n_data_x)

    def apply_post_training(self, **kwargs):
        pass

    
    def create_batch_data(self,**kwargs):
        n_collocation = kwargs.get("n_collocation_x", 1_000)
        n_data = kwargs.get("n_data_x", 0)
        if n_collocation == 0:
            m = self.input_t.size()[0]
        if n_data == 0:
            m = n_collocation
        if n_data > 0 and n_collocation > 0:
            m = min(self.input_t.size()[0], n_collocation)
        return m,torch.randperm(m)
    
    def evaluate_losses(self,epoch,step, **kwargs):
        n_simu = kwargs.get("n_simu", 10)
        n_collocation_x = kwargs.get("n_collocation_x", 200)
        n_bc_collocation_x = kwargs.get("n_bc_collocation_x", 0)

        if n_simu > 0 and n_collocation_x > 0:
            sample, f_loss, sample_bc, f_loss_bc = self.sampler.sampling(
                 n_collocation_x, n_simu
            )
            f_out = self.residual(sample, sample_bc, f_loss)
            zeros = torch.zeros_like(f_out)
            self.losses.update_residual_loss(
                self.losses.residual_f_loss(f_out, zeros)
            )

                    # TODO
                    # Check this part in case the BC are not hardly imposed
        if self.losses.bc_loss_bool:
            sample, f_loss, sample_bc, f_loss_bc = self.sampler.sampling(
                n_bc_collocation_x, n_simu
            )
            bc_out = self.bc_residual(sample, sample_bc, f_loss_bc)
            bc_zeros = torch.zeros_like(bc_out)
            self.losses.update_bc_loss(
                self.losses.bc_f_loss(bc_out, bc_zeros)
            )

        if self.losses.data_loss_bool:
            indices = self.permutation[step : step + self.batch_size]
            masked_sample = self.data_sample[indices]
            prediction = self.network.get_w(masked_sample)
            self.losses.update_data_loss(
                self.losses.data_f_loss(prediction, masked_sample)
            )

    def plot(self, random=False, n_visu=10000, reference_solution=None):
        import matplotlib.pyplot as plt

        if self.pde.dimension_x == 2:
            sample, f_loss, sample_bc, _ = self.sampler.sampling(n_visu, 1)

            x = sample.x_loss
            mu = sample.params
            x1, x2 = x.get_coordinates()

            parameter_string = ", ".join(
                [
                    f"{mu[0, i].detach().cpu():2.2f}"
                    for i in range(self.pde.nb_parameters)
                ]
            )

            if reference_solution is None:
                reference_solution = self.pde.reference_solution

            w_pred = self.network.setup_w_dict(x, mu, sample, sample_bc)
            w_ex = reference_solution(x, self.sampler.source_sampler.params)

            fig, ax = plt.subplots(2, 2, figsize=(15, 8))
            ax[1, 0] = self.losses.plot(ax[1, 0])

            im = ax[0, 0].scatter(
                x1.detach().cpu(),
                x2.detach().cpu(),
                s=3,
                c=w_pred["w"][:, 0].detach().cpu(),
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im, ax=ax[0, 0])
            ax[0, 0].set_title(f"prediction, parameters = {parameter_string}")
            ax[0, 0].legend()

            im2 = ax[0, 1].scatter(
                x1.detach().cpu(),
                x2.detach().cpu(),
                s=3,
                c=w_ex[:, 0].detach().cpu(),
                cmap="gist_ncar",
                label="u(x, y)",
            )
            fig.colorbar(im2, ax=ax[0, 1])
            ax[0, 1].set_title(f"solution, parameters = {parameter_string}")
            ax[0, 1].legend()

            error = torch.abs(w_pred["w"] - w_ex)

            im3 = ax[1, 1].scatter(
                x1.detach().cpu(),
                x2.detach().cpu(),
                s=3,
                c=error[:, 0].detach().cpu(),
                cmap="gist_ncar",
                label="$u_{\\theta}(x,y)-u(x, y)$",
            )
            fig.colorbar(im3, ax=ax[1, 1])
            ax[1, 1].set_title("prediction error")
            ax[1, 1].legend()

        else:
            _, ax = plt.subplots(1, 3, figsize=(15, 5))

            ax[0] = self.losses.plot(ax[0])

            n_visu = 500

            x_min = self.pde.space_domain.bound[0][0]
            x_max = self.pde.space_domain.bound[0][1]

            x = torch.linspace(x_min, x_max, n_visu)[:, None]

            shape = (n_visu, self.pde.nb_parameters)
            ones = torch.ones(shape)
            if random:
                mu = self.mu_sampler.sampling(1)
                mu = mu * ones
            else:
                mu = torch.mean(self.pde.parameter_domain, axis=1) * ones

            parameter_string = ", ".join(
                [f"{mu[0, i].cpu():2.2f}" for i in range(self.pde.nb_parameters)]
            )

            w_pred = self.network.get_w(x, mu)
            w_ex = self.pde.reference_solution(x, mu)

            ax[1].plot(x.cpu(), w_ex.detach().cpu(), label="exact")
            ax[1].plot(x.cpu(), w_pred.detach().cpu(), label="prediction")

            ax[1].set_title(f"prediction, parameters = {parameter_string}")
            ax[1].legend()

            error = torch.abs(w_pred - w_ex).detach().cpu()

            ax[2].plot(x.cpu(), error)
            ax[2].set_title("prediction error")
        plt.show()


# %%
