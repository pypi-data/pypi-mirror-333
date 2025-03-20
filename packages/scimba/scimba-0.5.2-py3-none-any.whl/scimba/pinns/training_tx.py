from pathlib import Path

import torch

from .. import sampling
from ..equations import pde_1d_heat
from ..equations.domain import SpaceTensor
from ..nets import training, training_tools
from . import pinn_tx
from .pinn_losses import PinnLossesData


class TrainerPINNSpaceTime(training.AbstractTrainer):
    """
    This class construct a trainer to solve a PINNs for time space PDE problem

    :param ode: the PDE considered
    :type network: AbstractPDEtx
    :param network: the network used
    :type network: nn.Module
    :param sampler: the sampler used
    :type sampler: AbstractSampling
    :param optimizers: the optimizers used
    :type optimizers: OptimizerData
    :param losses: the data class for the loss
    :type losses: PinnLossesData

    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param file_name: the name of the file to save the network
    :type file_name: str
    """

    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, **kwargs):
        self.pde = kwargs.get("pde", pde_1d_heat.HeatEquation())
        self.network = kwargs.get(
            "network",
            pinn_tx.PINNtx(pinn_tx.MLP_tx(pde=self.pde), self.pde),
        )
        sampler_for_x = sampling.sampling_pde.XSampler(self.pde)
        sampler_for_t = sampling.sampling_ode.TSampler(
            sampler=sampling.uniform_sampling.UniformSampling, ode=self.pde
        )
        sampler_for_mu = sampling.sampling_parameters.MuSampler(
            sampler=sampling.uniform_sampling.UniformSampling, model=self.pde
        )
        self.sampler = kwargs.get(
            "sampler",
            sampling.sampling_pde.PdeTXCartesianSampler(
                sampler_for_t, sampler_for_x, sampler_for_mu
            ),
        )
        self.optimizers = kwargs.get(
            "optimizers", training_tools.OptimizerData(**kwargs)
        )
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
        self.t_collocation = None
        self.x_collocation = None
        self.bc_x_collocation = None
        self.mu_collocation = None
        self.pre_training = True
        self.post_training = False
        self.used_batch = True

    def residual(
        self, t: torch.Tensor, x: SpaceTensor, mu: torch.Tensor, **kwargs: dict
    ) -> torch.Tensor:
        """Compute the PDE residual from sampled times, space points and parameters.

        This function
            #. evaluates the network at points x and mu
            #. computes its first derivatives at points x and mu
            #. if needed, computes its second derivatives at points x and mu
            #. uses this information to compute the PDE residual

        :param t: sampled times
        :type t: torch.Tensor
        :param x: sampled space points
        :type x: torch.Tensor
        :param mu: sampled parameters
        :type mu: torch.Tensor
        :return: the residual of the PDE at (t, x, mu)
        :rtype: torch.Tensor
        """

        # get the approximation of the unknown function
        w = self.network.setup_w_dict(t, x, mu)

        # computation of the first derivatives in time
        if self.pde.first_derivative_t:
            # compute dw / dt
            if (
                self.pde.force_compute_1st_derivatives_t_in_residual
                or self.pde.force_compute_2nd_derivatives_t_in_residual
            ):
                self.network.get_first_derivatives_t(w, t)

            # compute d(f_t(w)) / dt
            if not self.pde.f_t_is_identity:
                self.network.get_first_derivatives_f_t(w, t, x, mu, self.pde.f_t)

            if self.pde.cross_derivative:
                self.network.get_cross_derivatives_tx(w, x)

        # computation of the second derivatives in time
        if self.pde.second_derivative_t:
            # compute d^2w / dt^2
            if self.pde.force_compute_2nd_derivatives_t_in_residual:
                self.network.get_second_derivatives_t(w, t)

            # compute d^2(f_tt(w)) / dt^2
            if not self.pde.f_tt_is_identity:
                self.network.get_second_derivatives_f_t(w, t, x, mu, self.pde.f_tt)

        # computation of the first derivatives in space
        if self.pde.first_derivative_x:
            # compute dw / dx
            if (
                self.pde.force_compute_1st_derivatives_x_in_residual
                or self.pde.force_compute_2nd_derivatives_x_in_residual
            ):
                self.network.get_first_derivatives_x(w, x)

            # compute d(f_x(w)) / dx
            if not self.pde.f_x_is_identity:
                self.network.get_first_derivatives_f_x(w, t, x, mu, self.pde.f_x, "x")

            # compute d(f_y(w)) / dx
            if not self.pde.f_y_is_identity and self.pde.dimension_x > 1:
                self.network.get_first_derivatives_f_x(w, t, x, mu, self.pde.f_y, "y")

        # computation of the second derivatives in space
        if self.pde.second_derivative_x:
            # compute d^2w / dx^2
            if self.pde.force_compute_2nd_derivatives_x_in_residual:
                self.network.get_second_derivatives_x(w, x)

            # compute d^2(f_xx(w)) / dx^2
            if not self.pde.f_xx_is_identity:
                self.network.get_second_derivatives_f_x(
                    w, t, x, mu, self.pde.f_xx, "xx"
                )
            # compute d^2(f_xy(w)) / dxy
            if not self.pde.f_xy_is_identity and self.pde.dimension_x > 1:
                self.network.get_second_derivatives_f_x(
                    w, t, x, mu, self.pde.f_xy, "xy"
                )
            # compute d^2(f_yy(w)) / dy^2
            if not self.pde.f_yy_is_identity and self.pde.dimension_x > 1:
                self.network.get_second_derivatives_f_x(
                    w, t, x, mu, self.pde.f_yy, "yy"
                )

        # computation of the div(K * grad(w)) term
        if not self.pde.no_anisotropy_matrix:
            self.network.get_div_K_grad_w(w, t, x, mu, self.pde.anisotropy_matrix)

        # compute the PDE residual and concatenate it, if needed
        pde_residual = self.pde.residual(w, t, x, mu, **kwargs)
        if isinstance(pde_residual, torch.Tensor):
            return pde_residual
        elif isinstance(pde_residual, tuple):
            return torch.cat(pde_residual, axis=0)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def bc_residual(
        self, t: torch.Tensor, x: SpaceTensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """Compute the residual of the PDE at boundary points.

        :param t: sampled times
        :type t: torch.Tensor
        :param x: sampled boundary points
        :type x: torch.Tensor
        :param mu: sampled parameters
        :type mu: torch.Tensor
        :return: the boundary residual of the PDE at (t, x, mu)
        :rtype: torch.Tensor
        """

        # compute w and its derivatives
        w = self.network.setup_w_dict(t, x, mu)
        self.network.get_first_derivatives(w, t, x)

        # compute the PDE boundary residual and concatenate it, if needed
        pde_bc_residual = self.pde.bc_residual(w, t, x, mu, **kwargs)
        if isinstance(pde_bc_residual, torch.Tensor):
            return pde_bc_residual
        elif isinstance(pde_bc_residual, tuple):
            return torch.cat(pde_bc_residual, axis=1)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def apply_pre_training(self, **kwargs):
        n_data = kwargs.get("n_data", 0)

        if n_data > 0 and self.losses.data_loss_bool:
            if self.pde.data_construction == "sampled":
                self.input_t, self.input_x, self.input_mu = self.sampler.sampling(
                    n_data
                )
                self.output = self.pde.reference_solution(
                    self.input_t, self.input_x, self.input_mu
                )
            else:
                self.input_t, self.input_x, self.input_mu, self.output = (
                    self.pde.make_data(n_data)
                )

    def apply_post_training(self, **kwargs):
        pass

    def create_batch_data(self, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)
        n_data = kwargs.get("n_data", 0)
        if n_collocation == 0:
            m = self.input_t.size()[0]
        if n_data == 0:
            m = n_collocation
        if self.losses.data_loss_bool and n_data > 0 and n_collocation > 0:
            m = min(self.input_t.size()[0], n_collocation)
        return m, torch.randperm(m)

    def evaluate_losses(self, epoch, step, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)
        n_bc_collocation = kwargs.get("n_bc_collocation", 1_000)
        n_init_collocation = kwargs.get("n_init_collocation", 1_000)

        if n_collocation > 0:
            (
                self.t_collocation,
                self.x_collocation,
                self.mu_collocation,
            ) = self.sampler.sampling(n_collocation)

            f_out = self.residual(
                self.t_collocation,
                self.x_collocation,
                self.mu_collocation,
                **kwargs,
            )

            weights = self.sampler.density(
                self.t_collocation,
                self.x_collocation,
                self.mu_collocation,
            )

            zeros = torch.zeros_like(f_out)
            self.losses.update_residual_loss(
                self.losses.residual_f_loss(f_out / weights, zeros)
            )

        if self.losses.bc_loss_bool:
            batch_bc_t, batch_bc_x, batch_bc_mu = self.sampler.bc_sampling(
                n_bc_collocation
            )
            bc_out = self.bc_residual(
                batch_bc_t,
                batch_bc_x,
                batch_bc_mu,
                **kwargs,
            )
            bc_zeros = torch.zeros_like(bc_out)
            self.losses.update_bc_loss(self.losses.bc_f_loss(bc_out, bc_zeros))

        if self.losses.init_loss_bool:
            batch_bc_t, batch_bc_x, batch_bc_mu = self.sampler.sampling(
                n_init_collocation
            )
            batch_bc_t = batch_bc_t * 0.0
            w = self.network.setup_w_dict(batch_bc_t, batch_bc_x, batch_bc_mu)
            bi = self.pde.initial_condition(batch_bc_x, batch_bc_mu, **kwargs)

            if not self.pde.init_on_dt:
                res = self.losses.init_f_loss(w["w"], bi)
            else:
                self.network.get_first_derivatives(w, batch_bc_t, batch_bc_x)
                init_loss_on_w = self.losses.init_f_loss(w["w"], bi[0])
                init_loss_on_w_t = self.losses.init_f_loss(w["w_t"], bi[1])
                res = init_loss_on_w + init_loss_on_w_t
            self.losses.update_init_loss(res)

        if self.losses.data_loss_bool:
            indices = self.permutation[step : step + self.batch_size]
            batch_t, batch_x, batch_mu, batch_y = (
                self.input_t[indices],
                self.input_x[indices],
                self.input_mu[indices],
                self.output[indices],
            )
            prediction = self.network.get_w(batch_t, batch_x, batch_mu)
            self.losses.update_data_loss(self.losses.data_f_loss(prediction, batch_y))

    def plot(self, random=False, reference_solution=False, steady_solution=False):
        import matplotlib.pyplot as plt

        n_visu = 20000
        t = torch.ones(n_visu) * self.pde.t_max
        t = t[:, None]
        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        mu = torch.mean(self.pde.parameter_domain, axis=1) * ones

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu().numpy():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        w_pred = self.network.setup_w_dict(t, x, mu)
        if reference_solution:
            w_ex = self.pde.reference_solution(t, x, mu)
            if steady_solution:
                w_pred["w"] -= self.pde.steady_solution(x, mu)
                w_ex -= self.pde.steady_solution(x, mu)

        if self.pde.dimension_x == 1:
            _, ax = plt.subplots(1, 3, figsize=(15, 4))
            x = x.get_coordinates()
            ax[0] = self.losses.plot(ax[0])

            if reference_solution:
                ax[1].scatter(
                    x.detach().cpu().numpy(),
                    w_ex[:, 0].detach().cpu().numpy(),
                    s=5,
                    alpha=0.4,
                    label="exact solution",
                )
            ax[1].scatter(
                x.detach().cpu().numpy(),
                w_pred["w"][:, 0].detach().cpu().numpy(),
                s=4,
                label="prediction ",
            )

            ax[1].set_title(f"prediction, parameters = {parameter_string}")
            ax[1].legend()

            if reference_solution:
                error = torch.abs(w_pred["w"] - w_ex)[:, 0].detach().cpu()

                ax[2].scatter(
                    x.detach().cpu().numpy(),
                    error.detach().cpu().numpy(),
                    s=5,
                    label=" erreur ",
                )
                ax[2].set_title("prediction error")
                plt.show()

        if self.pde.dimension_x == 2:
            fig, ax = plt.subplots(2, 2, figsize=(15, 8))
            x1, x2 = x.get_coordinates()

            ax[0, 0] = self.losses.plot(ax[0, 0])

            im = ax[0, 1].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=10,
                c=w_pred["w"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label=r"w_{\theta}(t_{end}, x, y)",
            )
            fig.colorbar(im, ax=ax[0, 0])
            ax[0, 1].set_title(f"prediction, parameters = {parameter_string}")
            ax[0, 1].legend()

            if reference_solution:
                im2 = ax[1, 0].scatter(
                    x1.detach().cpu().numpy(),
                    x2.detach().cpu().numpy(),
                    s=10,
                    c=w_ex[:, 0].detach().cpu().numpy(),
                    cmap="gist_ncar",
                    label=r"w(t_{end}, x, y)",
                )
                fig.colorbar(im2, ax=ax[1, 0])
                ax[1, 0].set_title(f"solution, parameters = {parameter_string}")
                ax[1, 0].legend()

                error = torch.abs(w_pred["w"] - w_ex)

                im3 = ax[1, 1].scatter(
                    x1.detach().cpu().numpy(),
                    x2.detach().cpu().numpy(),
                    s=10,
                    c=error[:, 0].detach().cpu().numpy(),
                    cmap="gist_ncar",
                    label=r"w_{\theta}(t_{end}, x, y) - w(t_{end}, x, y)",
                )

                fig.colorbar(im3, ax=ax[1, 1])
                ax[1, 1].set_title("prediction error")
                ax[1, 1].legend()
        plt.show()
