from pathlib import Path

import torch

from ..equations import ode_basic
from ..nets.training import AbstractTrainer
from ..nets.training_tools import OptimizerData
from ..pinns.pinn_losses import PinnLossesData
from ..sampling import (
    sampling_functions,
    sampling_ode,
    sampling_parameters,
    uniform_sampling,
)
from ..sampling.data_sampling_ode import ode_data


class TrainerPINOTime(AbstractTrainer):
    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, **kwargs):
        self.ode = kwargs.get("ode", ode_basic.SimpleOdeWithSource())

        self.network = kwargs.get("network", None)
        if self.network is None:
            raise ValueError("network must be provided to TrainerDeepONetTime")

        self.sampler = kwargs.get("sampler", None)

        if self.sampler is None:
            t_usampler = sampling_ode.TSampler(
                sampler=uniform_sampling.UniformSampling, ode=self.ode
            )
            mu_usampler = sampling_parameters.MuSampler(
                sampler=uniform_sampling.UniformSampling, model=self.ode
            )
            w_initial_usampler = uniform_sampling.UniformSampling(1, [[0.0, 1.0]])
            self.sampler = ode_data(
                sampler_t=t_usampler,
                sampler_params=mu_usampler,
                sampler_initial_condition=w_initial_usampler,
                source=sampling_functions.Default_ParametricFunction_t(),
                n_sensor=70,
                resample_sensors=False,
            )

        self.optimizers = kwargs.get("optimizers", OptimizerData(**kwargs))
        self.losses = kwargs.get("losses", PinnLossesData(**kwargs))
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.ode.file_name)
        self.file_name = folder_for_saved_networks / file_name
        self.batch_size = kwargs.get("batch_size", 1000)

        self.create_network()
        print(">> load network", self.file_name)
        self.load(self.file_name)

        self.to_be_trained = kwargs.get("to_be_trained", self.to_be_trained)
        self.pre_training = True
        self.post_training = False

    def residual(self, sample: ode_data, f: torch.Tensor) -> torch.Tensor:
        t, mu = sample.t_loss, sample.params

        w = self.network.setup_w_dict(t, mu, sample)
        self.network.get_first_derivatives(w, t)

        if self.ode.second_derivative:
            self.network.get_second_derivatives(w, t)

        # compute the ODE residual and concatenate it, if needed
        ode_residual = self.ode.residual(w, t, mu, f=f)
        if isinstance(ode_residual, torch.Tensor):
            return ode_residual
        elif isinstance(ode_residual, tuple):
            return torch.cat(ode_residual, axis=0)
        else:
            raise ValueError("ode_residual should be a tensor or a tuple of tensors")

    def apply_pre_training(self, **kwargs):
        n_data_f = kwargs.get("n_data_f", 0)
        n_data_t = kwargs.get("n_data_t", 0)

        if n_data_f > 0 or n_data_t > 0:
            self.data_sample = self.ode.make_data(n_data_t)

    def apply_post_training(self, **kwargs):
        pass

    def create_batch_data(self, **kwargs):
        n_collocation = kwargs.get("n_collocation_t", 1_000)
        n_data = kwargs.get("n_data_t", 0)
        if n_collocation == 0:
            m = self.input_t.size()[0]
        if n_data == 0:
            m = n_collocation
        if n_data > 0 and n_collocation > 0:
            m = min(self.input_t.size()[0], n_collocation)
        return m, torch.randperm(m)

    def evaluate_losses(self, epoch, step, **kwargs):
        n_simu = kwargs.get("n_simu", 10)
        n_collocation_t = kwargs.get("n_collocation_t", 200)
        n_collocation_init = kwargs.get("n_collocation_init", 200)

        if n_simu > 0 and n_collocation_t > 0:
            sample, f_loss = self.sampler.sampling(n_collocation_t, n_simu)
            f_out = self.residual(sample, f_loss)
            zeros = torch.zeros_like(f_out)
            self.losses.update_residual_loss(self.losses.residual_f_loss(f_out, zeros))

        if self.losses.init_loss_bool:
            sample, f_loss = self.sampler.sampling(n_collocation_init, n_simu)

            t = 0 * sample.t_loss
            mu = sample.params
            w = self.network.setup_w_dict(t, mu, sample)
            w_init = sample.w_initial

            if not self.ode.second_derivative:
                res = self.losses.init_f_loss(w["w"], w_init)
            else:
                self.network.get_first_derivatives(w, t)
                init_loss_on_w = self.losses.init_f_loss(w["w"], w_init[0])
                init_loss_on_w_t = self.losses.init_f_loss(w["w_t"], w_init[1])
                res = init_loss_on_w + init_loss_on_w_t
            self.losses.update_init_loss(res)

        if self.losses.data_loss_bool:
            indices = self.permutation[step : step + self.batch_size]
            masked_sample = self.data_sample[indices]
            prediction = self.network.get_w(masked_sample)
            self.losses.update_data_loss(
                self.losses.data_f_loss(prediction, masked_sample)
            )

    # def plot(self, random=False):
    #     import matplotlib.pyplot as plt

    #     _, ax = plt.subplots(1, 3, figsize=(15, 5))
    #     ax[0].semilogy(self.loss_history, label="total loss")
    #     ax[0].semilogy(self.data_loss_history, label="data")
    #     ax[0].semilogy(self.residual_loss_history, label="residual")
    #     ax[0].set_title("loss history")
    #     ax[0].legend()

    #     n_visu = 500

    #     t = torch.linspace(
    #         self.ode.t_min, self.ode.t_max, n_visu, dtype=torch.double, device=device
    #     )[:, None]

    #     shape = (n_visu, self.ode.nb_parameters)
    #     ones = torch.ones(shape)
    #     if random:
    #         mu = self.mu_sampler.sampling(1)
    #         mu = mu * ones
    #     else:
    #         mu = torch.mean(self.ode.parameter_domain, axis=1) * ones

    #     parameter_string = ", ".join(
    #         [f"{mu[0, i].cpu().numpy():2.2f}" for i in range(self.ode.nb_parameters)]
    #     )

    #     v_pred = self.network.get_w(t, mu)
    #     v_ex = self.ode.reference_solution(t, mu)

    #     ax[1].plot(t.cpu(), v_ex.detach().cpu(), label="exact")
    #     ax[1].plot(t.cpu(), v_pred.detach().cpu(), label="prediction")

    #     ax[1].set_title(f"prediction, parameters = {parameter_string}")
    #     ax[1].legend()

    #     error = torch.abs(v_pred - v_ex).detach().cpu()

    #     ax[2].plot(t.cpu(), error)
    #     ax[2].set_title("prediction error")


# %%
