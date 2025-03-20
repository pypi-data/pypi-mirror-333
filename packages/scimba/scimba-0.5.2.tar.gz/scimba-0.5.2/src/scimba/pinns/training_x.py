from pathlib import Path

import torch
from torch.autograd import grad

from ..equations import pde_1d_laplacian
from ..equations.domain import Id_domain, SpaceTensor
from ..nets import training, training_tools
from ..sampling import sampling_parameters, sampling_pde, uniform_sampling
from . import pinn_x
from .pinn_losses import PinnLossesData


class TrainerPINNSpace(training.AbstractTrainer):
    """
    This class construct a trainer to solve a PINNs for spatial PDE problem

    :param ode: the ODE considered
    :type network: AbstractPDEx
    :param network: the network used
    :type network: nn.Module
    :param network: the sampler used
    :type network: AbstractSampling
    :param losses: the data class for the loss
    :type losses: PinnLossesData

    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param file_name: the name of the file to save the network
    :type file_name: str
    """

    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, **kwargs):
        self.pde = kwargs.get("pde", pde_1d_laplacian.LaplacianSine(k=1))
        self.network = kwargs.get(
            "network",
            pinn_x.PINNx(pinn_x.MLP_x(pde=self.pde), self.pde),
        )
        sampler_for_x = sampling_pde.XSampler(self.pde)
        sampler_for_mu = sampling_parameters.MuSampler(
            sampler=uniform_sampling.UniformSampling, model=self.pde
        )
        self.sampler = kwargs.get(
            "sampler",
            sampling_pde.PdeXCartesianSampler(sampler_for_x, sampler_for_mu),
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
        self.x_collocation = None
        self.bc_x_collocation = None
        self.mu_collocation = None
        self.pre_training = True
        self.post_training = False
        self.used_batch = True

    def residual(
        self, x: SpaceTensor, mu: torch.Tensor, **kwargs: dict
    ) -> torch.Tensor:
        """Compute the PDE residual from sampled space points and parameters.

        This function
            #. evaluates the network at points x and mu
            #. computes its first derivatives at points x and mu
            #. if needed, computes its second derivatives at points x and mu
            #. uses this information to compute the PDE residual

        :param x: sampled space points
        :type x: torch.Tensor
        :param mu: sampled parameters
        :type mu: torch.Tensor
        :return: the residual of the PDE at (x, mu)
        :rtype: torch.Tensor
        """

        # get the approximation of the unknown function
        w = self.network.setup_w_dict(x, mu)

        # computation of the first derivatives
        if self.pde.first_derivative:
            # compute dw / dx
            if (
                self.pde.force_compute_1st_derivatives_in_residual
                or self.pde.force_compute_2nd_derivatives_in_residual
            ):
                self.network.get_first_derivatives(w, x)

            # compute d(f_x(w)) / dx
            if not self.pde.f_x_is_identity:
                self.network.get_first_derivatives_f(w, x, mu, self.pde.f_x, "x")

            # compute d(f_y(w)) / dx
            if not self.pde.f_y_is_identity and self.pde.dimension_x > 1:
                self.network.get_first_derivatives_f(w, x, mu, self.pde.f_y, "y")

        # computation of the second derivatives
        if self.pde.second_derivative:
            # compute d^2w / dx^2
            if self.pde.force_compute_2nd_derivatives_in_residual:
                self.network.get_second_derivatives(w, x)

            # compute d^2(f_xx(w)) / dx^2
            if not self.pde.f_xx_is_identity:
                self.network.get_second_derivatives_f(w, x, mu, self.pde.f_xx, "xx")
            # compute d^2(f_xy(w)) / dxy
            if not self.pde.f_xy_is_identity and self.pde.dimension_x > 1:
                self.network.get_second_derivatives_f(w, x, mu, self.pde.f_xy, "xy")
            # compute d^2(f_yy(w)) / dy^2
            if not self.pde.f_yy_is_identity and self.pde.dimension_x > 1:
                self.network.get_second_derivatives_f(w, x, mu, self.pde.f_yy, "yy")

        # computation of the div(K * grad(w)) term
        if not self.pde.no_anisotropy_matrix:
            self.network.get_div_K_grad_w(w, x, mu, self.pde.anisotropy_matrix)

        # compute third derivatives
        if self.pde.third_derivative:
            self.network.get_third_derivatives(w, x)

        # compute third derivatives
        if self.pde.derivatives_wrt_mu:
            self.network.get_mu_derivatives(w, mu)

        # compute the PDE residual and concatenate it, if needed
        pde_residual = self.pde.residual(w, x, mu, **kwargs)
        if isinstance(pde_residual, torch.Tensor):
            return pde_residual
        elif isinstance(pde_residual, tuple):
            return torch.cat(pde_residual, axis=0)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def bc_residual(
        self, x: torch.Tensor, mu: torch.Tensor, **kwargs: dict
    ) -> torch.Tensor:
        """Compute the residual of the PDE at boundary points.

        :param x: sampled boundary points
        :type x: torch.Tensor
        :param mu: sampled parameters
        :type mu: torch.Tensor
        :return: the boundary residual of the PDE at (x, mu)
        :rtype: torch.Tensor
        """

        # compute w and its derivative
        w = self.network.setup_w_dict(x, mu)
        if self.pde.first_derivative:
            self.network.get_first_derivatives(w, x)

        # compute the PDE boundary residual and concatenate it, if needed
        pde_bc_residual = self.pde.bc_residual(w, x, mu, **kwargs)
        if isinstance(pde_bc_residual, torch.Tensor):
            return pde_bc_residual
        elif isinstance(pde_bc_residual, tuple):
            return torch.cat(pde_bc_residual, axis=1)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def apply_pre_training(self, **kwargs):
        n_data = kwargs.get("n_data", 0)

        if self.losses.data_loss_bool and n_data > 0:
            if self.pde.data_construction == "sampled":
                self.input_x, self.input_mu = self.sampler.sampling(n_data)
                self.output = self.pde.reference_solution(self.input_x, self.input_mu)
            else:
                self.input_x, self.input_mu, self.output = self.pde.make_data(n_data)

    def apply_post_training(self, **kwargs):
        pass

    def create_batch_data(self, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)
        n_data = kwargs.get("n_data", 0)

        if n_collocation == 0:
            m = self.input_x.shape[0]
        if not self.losses.data_loss_bool:
            m = n_collocation
        if self.losses.data_loss_bool and n_data > 0 and n_collocation > 0:
            m = min(self.input_x.shape[0], n_collocation)

        return m, torch.randperm(m)

    def evaluate_losses(self, epoch: int, step: int, **kwargs):
        """
        Main training loop.

        This function computes the values of the loss function
        (made of data, PDE, and boudary losses),
        and uses automatic differentiation to optimize
        the parameters of the neural network.

        :params epochs: the number of epochs
        :type epochs: int
        :params step: the step with which the data is batched
        :type step: int
        """
        n_bc_collocation = kwargs.get("n_bc_collocation", 0)
        n_collocation = kwargs.get("n_collocation", 1_000)

        if n_collocation > 0:
            self.x_collocation, self.mu_collocation = self.sampler.sampling(
                n_collocation
            )
            f_out = self.residual(
                self.x_collocation,
                self.mu_collocation,
                **kwargs,
            )
            weights = self.sampler.density(
                self.x_collocation,
                self.mu_collocation,
            )
            zeros = torch.zeros_like(f_out)
            self.losses.update_residual_loss(
                self.losses.residual_f_loss(f_out / weights, zeros)
            )

        if self.losses.bc_loss_bool:
            batch_bc_x, batch_bc_mu = self.sampler.bc_sampling(n_bc_collocation)
            bc_out = self.bc_residual(
                batch_bc_x,
                batch_bc_mu,
                **kwargs,
            )
            zeros = torch.zeros_like(bc_out)
            self.losses.update_bc_loss(self.losses.bc_f_loss(bc_out, zeros))

        if self.losses.data_loss_bool:
            indices = self.permutation[step : step + self.batch_size]
            batch_x, batch_mu, batch_y = (
                self.input_x[indices],
                self.input_mu[indices],
                self.output[indices],
            )
            prediction = self.network.get_w(batch_x, batch_mu)
            self.losses.update_data_loss(self.losses.data_f_loss(prediction, batch_y))

    def plot(
        self, n_visu=100000, random=False, reference_solution=False, filename=None
    ):
        import matplotlib.pyplot as plt

        sampler = self.sampler

        x = sampler.sampling_x(n_visu)
        # x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        mu = ones
        if self.pde.nb_parameters > 0:
            if random:
                _, mu0 = self.sampler.sampling(1)
                mu *= mu0
            else:
                mu *= torch.mean(self.pde.parameter_domain, axis=1)

        parameter_string = ", ".join(
            [f"{mu[0, i].detach().cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        w_pred = self.network.setup_w_dict(x, mu)
        self.network.get_first_derivatives(w_pred, x)
        self.network.get_second_derivatives(w_pred, x)
        if reference_solution:
            w_ex = self.pde.reference_solution(x, mu)

        if self.pde.dimension_x == 1:
            _, ax = plt.subplots(1, 3, figsize=(15, 4))
            ax[0] = self.losses.plot(ax[0])

            x = x.get_coordinates()
            if reference_solution:
                ax[1].scatter(
                    x.detach().cpu(),
                    w_ex.detach().cpu(),
                    s=5,
                    alpha=0.4,
                    label="exact solution",
                )
            ax[1].scatter(
                x.detach().cpu(),
                w_pred["w"].detach().cpu(),
                s=4,
                label="prediction ",
            )

            ax[1].set_title(f"prediction, parameters = {parameter_string}")
            ax[1].legend()

            if reference_solution:
                error = torch.abs(w_pred["w"] - w_ex).detach().cpu()

                ax[2].scatter(
                    x.detach().cpu(),
                    error.detach().cpu(),
                    s=5,
                    label=" erreur ",
                )
                ax[2].set_title("prediction error")

                err_abs = (
                    torch.sum((error) ** 2, dim=0).detach().cpu() / n_visu
                ) ** 0.5
                norm = (torch.sum(w_ex**2, dim=0).detach().cpu() / n_visu) ** 0.5
                print("Error ", err_abs / norm)

        elif self.pde.dimension_x == 2:
            fig, ax = plt.subplots(
                1 + reference_solution, 2, figsize=(15, 4 * (1 + reference_solution))
            )
            top_left = (0, 0) if reference_solution else (0,)
            top_right = (0, 1) if reference_solution else (1,)

            ax[top_left] = self.losses.plot(ax[top_left])

            # x_bc = sampler.bc_sampling_x(n_visu)
            # x1_bc, x2_bc = x_bc.get_coordinates()
            # w_pred_bc = self.network.setup_w_dict(x_bc, mu)

            x1, x2 = x.get_coordinates()
            im = ax[top_right].scatter(
                x1.detach().cpu(),
                x2.detach().cpu(),
                s=3,
                c=w_pred["w"][:, 0].detach().cpu(),
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im, ax=ax[top_right])
            ax[top_right].set_title(f"prediction, parameters = {parameter_string}")
            ax[top_right].legend()

            if reference_solution:
                im2 = ax[1, 0].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=w_ex[:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="u(x, y)",
                )
                fig.colorbar(im2, ax=ax[1, 0])
                ax[1, 0].set_title(f"solution, parameters = {parameter_string}")
                ax[1, 0].legend()

                error = w_pred["w"] - w_ex
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

                err_abs = (
                    torch.sum((error) ** 2, dim=0).detach().cpu() / n_visu
                ) ** 0.5
                norm = (torch.sum(w_ex**2, dim=0).detach().cpu() / n_visu) ** 0.5
                print("Error ", err_abs / norm)
        else:
            fig, ax = plt.subplots(1 + reference_solution, 2, figsize=(12, 6))
            top_left = (0, 0) if reference_solution else (0,)
            top_right = (0, 1) if reference_solution else (1,)

            ax[top_left] = self.losses.plot(ax[top_left])

            x1, x2, x3 = x.get_coordinates()
            ax[top_right] = fig.add_subplot(2, 2, 2, projection="3d")
            im = ax[top_right].scatter(
                x1.detach().cpu(),
                x2.detach().cpu(),
                x3.detach().cpu(),
                s=3,
                c=w_pred["w"][:, 0].detach().cpu(),
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im, ax=ax[top_right])
            ax[top_right].set_title(f"prediction, parameters = {parameter_string}")
            ax[top_right].legend()

            if reference_solution:
                ax[1, 0] = fig.add_subplot(2, 2, 3, projection="3d")
                im2 = ax[1, 0].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    x3.detach().cpu(),
                    s=3,
                    c=w_ex[:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="u(x, y)",
                )
                fig.colorbar(im2, ax=ax[1, 0])
                ax[1, 0].set_title(f"solution, parameters = {parameter_string}")
                ax[1, 0].legend()

                error = torch.abs(w_pred["w"] - w_ex)

                ax[1, 1] = fig.add_subplot(2, 2, 4, projection="3d")
                im3 = ax[1, 1].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    x3.detach().cpu(),
                    s=3,
                    c=error[:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="$u_{\\theta}(x,y)-u(x, y)$",
                )
                fig.colorbar(im3, ax=ax[1, 1])
                ax[1, 1].set_title("prediction error")
                ax[1, 1].legend()

                err_abs = (
                    torch.sum((error) ** 2, dim=0).detach().cpu() / n_visu
                ) ** 0.5
                norm = (torch.sum(w_ex**2, dim=0).detach().cpu() / n_visu) ** 0.5
                print("Error ", err_abs / norm)

        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()

    def plot_second_derivative_x(self, filename, n_visu=1000, random: bool = False):
        import matplotlib.pyplot as plt

        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        if self.pde.nb_parameters != 0:
            mu = torch.mean(self.pde.parameter_domain, axis=1) * ones
        else:
            mu = torch.tensor([])

        parameter_string = ", ".join(
            [f"{mu[0, i].detach().cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        # get second derivatives of w_pred
        w_pred = self.network.setup_w_dict(x, mu)
        self.network.get_first_derivatives(w_pred, x)
        self.network.get_second_derivatives(w_pred, x)
        dw_dx = w_pred["w_xx"]
        dw_dy = w_pred["w_yy"]

        # get second derivatives of w_ex
        w_ex = self.pde.reference_solution(x, mu)
        ones = torch.ones_like(mu[:, 0, None])

        first_derivatives = torch.cat(
            [
                grad(w_ex[:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.pde.nb_unknowns)
            ],
            axis=-1,
        )

        ones = torch.ones_like(mu[:, 0, None])
        second_derivatives_x = grad(
            first_derivatives[0][:, None], x, ones, create_graph=True
        )[0].T
        second_derivatives_y = grad(
            first_derivatives[1][:, None], x, ones, create_graph=True
        )[0].T

        # second_derivatives_y =

        dwex_dx = second_derivatives_x[0][:, None]
        dwex_dy = second_derivatives_y[1][:, None]

        if self.pde.dimension_x == 1:
            pass
        elif self.pde.dimension_x == 2:
            fig, ax = plt.subplots(2, 3, figsize=(15, 8))

            error_x = torch.abs(dw_dx - dwex_dx).detach().cpu()
            error_y = torch.abs(dw_dy - dwex_dy).detach().cpu()
            dw_dx = dw_dx.detach().cpu()
            dw_dy = dw_dy.detach().cpu()
            dwex_dx = dwex_dx.detach().cpu()
            dwex_dy = dwex_dy.detach().cpu()

            im = ax[0, 0].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dw_dx[:, 0],
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )

            fig.colorbar(im, ax=ax[0, 0])

            ax[0, 0].set_title(f"prediction, parameters = {parameter_string}")
            ax[0, 0].legend()

            im2 = ax[0, 1].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dwex_dx[:, 0],
                cmap="gist_ncar",
                label="u(x, y)",
            )

            fig.colorbar(im2, ax=ax[0, 1])
            ax[0, 1].set_title(f"solution, parameters = {parameter_string}")
            ax[0, 1].legend()

            im3 = ax[0, 2].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=error_x[:, 0],
                cmap="gist_ncar",
                label="$u_{\\theta}(x,y)-u(x, y)$",
            )

            fig.colorbar(im3, ax=ax[0, 2])
            ax[0, 2].set_title("prediction error")
            ax[0, 2].legend()

            im4 = ax[1, 0].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dw_dy[:, 0],
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )

            fig.colorbar(im4, ax=ax[1, 0])
            ax[1, 0].set_title(f"prediction, parameters = {parameter_string}")
            ax[1, 0].legend()

            im5 = ax[1, 1].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dwex_dy[:, 0],
                cmap="gist_ncar",
                label="u(x, y)",
            )

            fig.colorbar(im5, ax=ax[1, 1])
            ax[1, 1].set_title(f"solution, parameters = {parameter_string}")
            ax[1, 1].legend()

            im6 = ax[1, 2].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=error_y[:, 0],
                cmap="gist_ncar",
                label="$u_{\\theta}(x,y)-u(x, y)$",
            )

            fig.colorbar(im6, ax=ax[1, 2])
            ax[1, 2].set_title("prediction error")

        plt.savefig(filename)

    def plot_mul_derivatives_x(self, filename, n_visu=1000, random: bool = False):
        import matplotlib.pyplot as plt

        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        if self.pde.nb_parameters != 0:
            mu = torch.mean(self.pde.parameter_domain, axis=1) * ones
        else:
            mu = torch.tensor([])

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        # get first derivatives of phi
        phi = self.pde.get_mul(x)

        ones = torch.ones_like(mu[:, 0, None])
        first_derivatives = torch.cat(
            [
                grad(phi, x, ones, create_graph=True)[0].T
                for i in range(self.pde.nb_unknowns)
            ],
            axis=-1,
        )
        dphi_dx = first_derivatives[0].detach().cpu()[:, None]
        dphi_dy = first_derivatives[1].detach().cpu()[:, None]

        # print("Enlever les grosses valeurs :")
        # max_dphi_dx = np.max(dphi_dx)
        # print(np.sum(np.abs(dphi_dx)> max_dphi_dx/2))
        # ind_true = np.where(np.abs(dphi_dx) > max_dphi_dx/2)
        # print(ind_true,x[ind_true])

        ones = torch.ones_like(mu[:, 0, None])
        second_derivatives_x = grad(
            first_derivatives[0][:, None], x, ones, create_graph=True
        )[0].T
        second_derivatives_y = grad(
            first_derivatives[1][:, None], x, ones, create_graph=True
        )[0].T

        dphi_dxx = second_derivatives_x[0].detach().cpu()[:, None]
        dphi_dyy = second_derivatives_y[1].detach().cpu()[:, None]

        if self.pde.dimension_x == 1:
            pass
        elif self.pde.dimension_x == 2:
            fig, ax = plt.subplots(2, 3, figsize=(15, 8))

            im0 = ax[0, 0].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=phi.detach().cpu()[:, 0],
                cmap="gist_ncar",
                # label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im0, ax=ax[0, 0])
            ax[0, 0].set_title(f"phi, parameters = {parameter_string}")
            # ax[0, 0].legend()

            im = ax[0, 1].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dphi_dx[:, 0],
                cmap="gist_ncar",
                # label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im, ax=ax[0, 1])
            ax[0, 1].set_title(f"dphi_dx, parameters = {parameter_string}")
            # ax[0, 1].legend()

            im2 = ax[0, 2].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dphi_dy[:, 0],
                cmap="gist_ncar",
                # label="u(x, y)",
            )
            fig.colorbar(im2, ax=ax[0, 2])
            ax[0, 2].set_title(f"dphi_dy, parameters = {parameter_string}")
            # ax[0, 2].legend()

            im3 = ax[1, 1].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dphi_dxx[:, 0],
                cmap="gist_ncar",
                # label="$u_{\\theta}(x, y)$",
            )

            fig.colorbar(im3, ax=ax[1, 1])
            ax[1, 1].set_title(f"dphi_dxx, parameters = {parameter_string}")
            # ax[1, 1].legend()

            im4 = ax[1, 2].scatter(
                x[:, 0].detach().cpu(),
                x[:, 1].detach().cpu(),
                s=3,
                c=dphi_dyy[:, 0],
                cmap="gist_ncar",
                # label="u(x, y)",
            )

            fig.colorbar(im4, ax=ax[1, 2])
            ax[1, 2].set_title(f"dphi_dyy, parameters = {parameter_string}")
            # ax[1, 2].legend()

        plt.savefig(filename)

    def plot_derivative_mu(self, n_visu=1000, random: bool = False):
        """Plotting derivatives of function; uses matplotlib.

        Plots the value of the prediction of the derivatives w.r.t the
        parameters mu of the PDE solution, compared with a reference solution.
        """

        import matplotlib.pyplot as plt

        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        mu = torch.mean(self.pde.parameter_domain, axis=1) * ones

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        # Calculate the derivatives of the predicted solution w.r.t mu_i
        mu.requires_grad = True
        w = self.network.setup_w_dict(x, mu)
        self.network.get_mu_derivatives(w, mu)
        dw_mu_pred = []
        for i in range(self.pde.nb_parameters):
            dw_mu_pred.append(w[f"w_mu{i + 1}"])

        # Calculate the derivatives of the analytical solution w.r.t mu_i
        w_ex = self.pde.reference_solution(x, mu)
        ones = torch.ones_like(mu[:, 0, None])
        first_derivatives = torch.cat(
            [
                grad(w_ex[:, i, None], mu, ones, create_graph=True)[0].T
                for i in range(self.pde.nb_unknowns)
            ],
            axis=-1,
        )

        dw_mu_ex = []
        shape = (self.pde.nb_unknowns, mu.shape[0])
        if self.pde.nb_parameters == 1:
            dw_mu_ex = first_derivatives.reshape(shape).T
        elif self.pde.nb_parameters >= 2:
            for i in range(self.pde.nb_parameters):
                dw_mu_ex.append(first_derivatives[i].reshape(shape).T)

        if self.pde.dimension_x == 1:
            _, ax = plt.subplots(self.pde.nb_parameters, 2, figsize=(15, 12))

            if self.pde.nb_parameters == 1:
                ax[0].scatter(
                    x.detach().cpu(),
                    dw_mu_ex.detach().cpu(),
                    s=5,
                    alpha=0.4,
                    label="d$u$(x, y)/d$\\mu$",
                )
                ax[0].scatter(
                    x.detach().cpu(),
                    dw_mu_pred[0].detach().cpu(),
                    s=4,
                    label="d$u_{\\theta}$(x, y)/d$\\mu$",
                )

                ax[0].set_title(f"prediction, parameters $\\mu$ = {parameter_string}")
                ax[0].legend()

                error = torch.abs(dw_mu_pred[0] - dw_mu_ex).detach().cpu()

                ax[1].scatter(
                    x.detach().cpu(),
                    error.detach().cpu(),
                    s=5,
                    label=" erreur ",
                )
                ax[1].set_title("prediction error")

            elif self.pde.nb_parameters > 1:
                for i in range(self.pde.nb_parameters):
                    ax[i, 0].scatter(
                        x.detach().cpu(),
                        dw_mu_ex[i].detach().cpu(),
                        s=5,
                        alpha=0.4,
                        label="d$u$(x, y)/d$\\mu$",
                    )
                    ax[i, 0].scatter(
                        x.detach().cpu(),
                        dw_mu_pred[i].detach().cpu(),
                        s=4,
                        label="d$u_{\\theta}$(x, y)/d$\\mu$",
                    )

                    parameter = mu[0, i].detach().cpu()
                    ax[i, 0].set_title(
                        f"prediction, parameters $\\mu_{i+1}$ = {parameter:2.2f}"
                    )
                    ax[i, 0].legend()

                    error = torch.abs(dw_mu_pred[i] - dw_mu_ex[i]).detach().cpu()

                    ax[i, 1].scatter(
                        x.detach().cpu(),
                        error.detach().cpu(),
                        s=5,
                        label=" erreur ",
                    )
                    ax[i, 1].set_title("prediction error")

        elif self.pde.dimension_x == 2:
            fig, ax = plt.subplots(self.pde.nb_parameters, 3, figsize=(15, 4))
            x1, x2 = x.get_coordinates()

            if self.pde.nb_parameters == 1:
                im = ax[0].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=dw_mu_pred[0].detach().cpu(),
                    cmap="gist_ncar",
                    label="d$u_{\\theta}$(x, y)/d$\\mu$",
                )
                fig.colorbar(im, ax=ax[0])
                ax[0].set_title(f"prediction, parameters $\\mu$ = {parameter_string}")
                ax[0].legend()

                im2 = ax[1].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=dw_mu_ex.detach().cpu(),
                    cmap="gist_ncar",
                    label="du(x, y)/d$\\mu$",
                )
                fig.colorbar(im2, ax=ax[1])
                ax[1].set_title(f"solution, parameters $\\mu$ = {parameter_string}")
                ax[1].legend()

                error = torch.abs(dw_mu_pred[0] - dw_mu_ex)

                im3 = ax[2].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=error[:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="d$u_{\\theta}$(x,y)/d$\\mu$-du(x, y)/d$\\mu$",
                )
                fig.colorbar(im3, ax=ax[2])
                ax[2].set_title("prediction error")
                ax[2].legend()

            elif self.pde.nb_parameters >= 2:
                for i in range(self.pde.nb_parameters):
                    im = ax[i, 0].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=dw_mu_pred[i][:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="d$u_{\\theta}$(x, y)/d$\\mu$",
                    )
                    fig.colorbar(im, ax=ax[i, 0])
                    ax[i, 0].set_title(
                        f"prediction, parameters $\\mu_{i+1}$ = {parameter_string}"
                    )
                    ax[i, 0].legend()

                    im2 = ax[i, 1].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=dw_mu_ex[i][:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="du(x, y)/d$\\mu$",
                    )
                    fig.colorbar(im2, ax=ax[i, 1])
                    ax[i, 1].set_title(
                        f"solution, parameters $\\mu_{i+1}$ = {parameter_string}"
                    )
                    ax[i, 1].legend()

                    error = torch.abs(dw_mu_pred[i][:, 0] - dw_mu_ex[i][:, 0])

                    im3 = ax[i, 2].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=error.detach().cpu(),
                        cmap="gist_ncar",
                        label="d$u_{\\theta}$(x,y)/d$\\mu$-du(x, y)/d$\\mu$",
                    )
                    fig.colorbar(im3, ax=ax[i, 2])
                    ax[i, 2].set_title("prediction error")
                    ax[i, 2].legend()

    def plot_derivative_xmu(
        self, n_visu=1000, random: bool = False, reference_solution=False
    ):
        """Plotting derivatives of function; uses matplotlib.

        Plots the value of the prediction of the cross derivatives w.r.t the
        coordinates x and the parameters mu of the PDE solution,
        compared with a reference solution.
        """

        import matplotlib.pyplot as plt

        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones_mu = torch.ones(shape)
        mu = torch.mean(self.pde.parameter_domain, axis=1) * ones_mu

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        # Calculate the cross derivatives of the predicted solution w.r.t the
        # coordinate x and then the parameters mu_i
        mu.requires_grad = True
        w = self.network.setup_w_dict(x, mu)
        self.network.get_first_derivatives(w, x)
        self.network.get_second_derivatives_xmu(w, x, mu)
        # Allocate the predicted derivatives based on the dimension of the
        # solution w_pred (2nd dimension) and
        # the number of parameters mu_i (3rd dimension)
        dw_xmu_pred = torch.empty(
            size=(n_visu, self.pde.nb_unknowns, self.pde.nb_parameters)
        )
        dw_ymu_pred = torch.empty(
            size=(n_visu, self.pde.nb_unknowns, self.pde.nb_parameters)
        )

        if self.pde.dimension_x == 1:
            for i in range(self.pde.nb_parameters):
                dw_xmu_pred[:, :, i] = w[f"w_xmu{i + 1}"]
        elif self.pde.dimension_x == 2:
            for i in range(self.pde.nb_parameters):
                dw_xmu_pred[:, :, i] = w[f"w_xmu{i + 1}"]
                dw_ymu_pred[:, :, i] = w[f"w_ymu{i + 1}"]
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not implemented in PINNx.get_second_derivatives"
            )

        # Calculate the cross derivatives of the reference solution w.r.t the
        # coordinate x and then the parameters mu_i
        if reference_solution:
            w_ex = self.pde.reference_solution(x, mu)
            ones = torch.ones_like(mu[:, 0, None])
            first_derivatives_x = torch.cat(
                [
                    grad(w_ex[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.pde.nb_unknowns)
                ],
                axis=-1,
            )

            shape = (self.pde.nb_unknowns, x.shape[0])
            if self.pde.dimension_x == 1:
                dw_x_ex = first_derivatives_x.reshape(shape).T
            elif self.pde.dimension_x == 2:
                dw_x_ex = first_derivatives_x[0].reshape(shape).T
                dw_y_ex = first_derivatives_x[1].reshape(shape).T
            else:
                raise NotImplementedError(
                    "PDE dimension > 2 not implemented in PINNx.get_second_derivatives"
                )

            second_derivatives_xmu = torch.cat(
                [
                    grad(dw_x_ex[:, i, None], mu, ones, create_graph=True)[0].T
                    for i in range(self.pde.nb_unknowns)
                ],
                axis=-1,
            )

            dw_xmu_ex = torch.empty(
                size=(n_visu, self.pde.nb_unknowns, self.pde.nb_parameters)
            )
            if self.pde.nb_parameters == 1:
                dw_xmu_ex[:, :, i] = second_derivatives_xmu.reshape(shape).T
            elif self.pde.nb_parameters >= 2:
                dw_xmu_ex = torch.empty(
                    size=(n_visu, self.pde.nb_unknowns, self.pde.nb_parameters)
                )
                for i in range(self.pde.nb_parameters):
                    dw_xmu_ex[:, :, i] = second_derivatives_xmu[i].reshape(shape).T

            if self.pde.dimension_x == 2:
                second_derivatives_ymu = torch.cat(
                    [
                        grad(dw_y_ex[:, i, None], mu, ones, create_graph=True)[0].T
                        for i in range(self.pde.nb_unknowns)
                    ],
                    axis=-1,
                )

                dw_ymu_ex = torch.empty(
                    size=(n_visu, self.pde.nb_unknowns, self.pde.nb_parameters)
                )
                if self.pde.nb_parameters == 1:
                    dw_ymu_ex[:, :, i] = second_derivatives_ymu.reshape(shape).T
                elif self.pde.nb_parameters >= 2:
                    for i in range(self.pde.nb_parameters):
                        dw_ymu_ex[:, :, i] = second_derivatives_ymu[i].reshape(shape).T

            if self.pde.dimension_x == 1:
                _, ax = plt.subplots(self.pde.nb_parameters, 2, figsize=(15, 5))

                if self.pde.nb_parameters == 1:
                    ax[0].scatter(
                        x.detach().cpu(),
                        dw_xmu_ex.detach().cpu(),
                        s=5,
                        alpha=0.4,
                        label="$d^2u$(x, y)/$dxd\\mu$",
                    )
                    ax[0].scatter(
                        x.detach().cpu(),
                        dw_xmu_pred.detach().cpu(),
                        s=4,
                        label="$d^2u_{\\theta}$(x, y)/$dxd\\mu$",
                    )

                    ax[0].set_title(
                        f"prediction, parameters $\\mu$ = {parameter_string}"
                    )
                    ax[0].legend()

                    error = torch.abs(dw_xmu_pred - dw_xmu_ex).detach().cpu()

                    ax[1].scatter(
                        x.detach().cpu(),
                        error.detach().cpu(),
                        s=5,
                        label=" erreur ",
                    )
                    ax[1].set_title("prediction error")

                elif self.pde.nb_parameters > 1:
                    for i in range(self.pde.nb_parameters):
                        ax[i, 0].scatter(
                            x.detach().cpu(),
                            dw_xmu_ex[..., i].detach().cpu(),
                            s=5,
                            alpha=0.4,
                            label="$d^2u$(x, y)/$dxd\\mu",
                        )
                        ax[i, 0].scatter(
                            x.detach().cpu(),
                            dw_xmu_pred[..., i].detach().cpu(),
                            s=4,
                            label="$d^2u_{\\theta}$(x, y)/$dxd\\mu$",
                        )

                        ax[i, 0].set_title(
                            f"prediction, parameters $\\mu_{i+1}$ = {parameter_string}"
                        )
                        ax[i, 0].legend()

                        error = (
                            torch.abs(dw_xmu_pred[..., i] - dw_xmu_ex[..., i])
                            .detach()
                            .cpu()
                        )

                        ax[i, 1].scatter(
                            x.detach().cpu(),
                            error.detach().cpu(),
                            s=5,
                            label=" erreur ",
                        )
                        ax[i, 1].set_title("prediction error")

        elif self.pde.dimension_x == 2:
            fig, ax = plt.subplots(self.pde.nb_parameters * 2, 3, figsize=(15, 6))
            for i in range(self.pde.nb_parameters):
                # Plot the cross derivatives w.r.t x and mu_i
                k = 2 * i
                x1, x2 = x.get_coordinates()
                im = ax[k, 0].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=dw_xmu_pred[:, :, i][:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="$d^2u_{\\theta}$(x, y)/$dxd\\mu$",
                )
                fig.colorbar(im, ax=ax[k, 0])
                ax[k, 0].set_title(
                    f"prediction, parameters $\\mu_{i+1}$ = {parameter_string}"
                )
                ax[k, 0].legend()

                if reference_solution:
                    im2 = ax[k, 1].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=dw_xmu_ex[:, :, i][:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="$d^2u(x, y)/dxd\\mu$",
                    )
                    fig.colorbar(im2, ax=ax[k, 1])
                    ax[k, 1].set_title(
                        f"solution, parameters $\\mu_{i+1}$ = {parameter_string}"
                    )
                    ax[k, 1].legend()

                    error = torch.abs(dw_xmu_pred[:, :, i] - dw_xmu_ex[:, :, i])

                    im3 = ax[k, 2].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=error[:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="$d^2u_{\\theta}$(x, y)/$dxd\\mu$-$d^2u(x, y)/dxd\\mu$",
                    )
                    fig.colorbar(im3, ax=ax[k, 2])
                    ax[k, 2].set_title("prediction error")
                    ax[k, 2].legend()
                #

                # Plot the cross derivatives w.r.t y and mu_i
                k = 2 * i + 1
                im4 = ax[k, 0].scatter(
                    x1.detach().cpu(),
                    x2.detach().cpu(),
                    s=3,
                    c=dw_ymu_pred[:, :, i][:, 0].detach().cpu(),
                    cmap="gist_ncar",
                    label="$d^2u_{\\theta}$(x, y)/$dyd\\mu$",
                )
                fig.colorbar(im4, ax=ax[k, 0])
                ax[k, 0].set_title(
                    f"prediction, parameters $\\mu_{i+1}$ = {parameter_string}"
                )
                ax[k, 0].legend()

                if reference_solution:
                    im5 = ax[k, 1].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=dw_ymu_ex[:, :, i][:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="$d^2u$(x, y)/dyd\\mu$",
                    )
                    fig.colorbar(im5, ax=ax[k, 1])
                    ax[k, 1].set_title(
                        f"solution, parameters $\\mu_{i+1}$ = {parameter_string}"
                    )
                    ax[k, 1].legend()

                    error = torch.abs(dw_ymu_pred[:, :, i] - dw_ymu_ex[:, :, i])

                    im6 = ax[k, 2].scatter(
                        x1.detach().cpu(),
                        x2.detach().cpu(),
                        s=3,
                        c=error[:, 0].detach().cpu(),
                        cmap="gist_ncar",
                        label="$d^2u_{\\theta}$(x, y)/$dyd\\mu$-$d^2u(x, y)/dyd\\mu$",
                    )
                    fig.colorbar(im6, ax=ax[k, 2])
                    ax[k, 2].set_title("prediction error")
                    ax[k, 2].legend()

    def plot_2d_contourf(
        self,
        n_visu=768,
        n_contour=250,
        random=False,
        colormap=None,
        draw_contours=False,
        n_drawn_contours=10,
        error=False,
        residual=False,
        seed=None,
        limit_res=1,
        save_plot=False,
        file_name=None,
    ):
        import matplotlib.pyplot as plt
        import numpy as np

        if seed is not None:
            torch.manual_seed(seed)

        if error and residual:
            raise ValueError("error and residual cannot be True at the same time")

        def make_colormap():
            colors = np.empty((8, 3))

            colors[0] = np.array((0.278431372549, 0.278431372549, 0.858823529412))
            colors[1] = np.array((0.000000000000, 0.000000000000, 0.360784313725))
            colors[2] = np.array((0.000000000000, 1.000000000000, 1.000000000000))
            colors[3] = np.array((0.000000000000, 0.501960784314, 0.000000000000))
            colors[4] = np.array((1.000000000000, 1.000000000000, 0.000000000000))
            colors[5] = np.array((1.000000000000, 0.380392156863, 0.000000000000))
            colors[6] = np.array((0.419607843137, 0.000000000000, 0.000000000000))
            colors[7] = np.array((0.878431372549, 0.301960784314, 0.301960784314))

            opacities = np.arange(8) / 7

            list_for_colormap = [(opacities[i], colors[i]) for i in range(8)]

            from matplotlib.colors import LinearSegmentedColormap

            return LinearSegmentedColormap.from_list(
                "rainbow desaturated", list_for_colormap
            )

        # compute bounding box

        pde_domain = self.pde.space_domain.large_domain

        if pde_domain.type == "square_based":
            x1_min, x1_max = pde_domain.bound[0]
            x2_min, x2_max = pde_domain.bound[1]
        elif pde_domain.type == "disk_based":
            if pde_domain.mapping == Id_domain:
                x1_min = pde_domain.center[0] - pde_domain.radius
                x1_max = pde_domain.center[0] + pde_domain.radius
                x2_min = pde_domain.center[1] - pde_domain.radius
                x2_max = pde_domain.center[1] + pde_domain.radius
            else:
                n_pts = 1_000
                r = pde_domain.radius
                theta = torch.linspace(0, 2 * np.pi, n_pts)[:, None]
                x = pde_domain.center[0] + r * torch.cos(theta)
                y = pde_domain.center[1] + r * torch.sin(theta)
                boundary_points = pde_domain.mapping(torch.cat([x, y], axis=1))
                x1_min = boundary_points[:, 0].min().item()
                x1_max = boundary_points[:, 0].max().item()
                x2_min = boundary_points[:, 1].min().item()
                x2_max = boundary_points[:, 1].max().item()
        else:
            print(f"plot_2d_contourf not implemented with {pde_domain.type} domain")
            return

        # extend the domain a bit
        lx1 = x1_max - x1_min
        lx2 = x2_max - x2_min
        x1_max += 0.025 * max(lx1, lx2)
        x1_min -= 0.025 * max(lx1, lx2)
        x2_max += 0.025 * max(lx1, lx2)
        x2_min -= 0.025 * max(lx1, lx2)

        # compute mesh
        x1 = torch.linspace(x1_min, x1_max, n_visu)
        x2 = torch.linspace(x2_min, x2_max, n_visu)
        x = SpaceTensor(
            torch.cat(
                (
                    torch.tile(x1, (n_visu,))[:, None],
                    torch.repeat_interleave(x2, n_visu)[:, None],
                ),
                1,
            ),
            labels=torch.zeros(n_visu**2, dtype=int),
        )

        shape = (n_visu**2, self.pde.nb_parameters)
        ones = torch.ones(shape)

        if self.pde.nb_parameters > 0:
            if random:
                _, mu = self.sampler.sampling(1)
                mu = mu * ones
            else:
                mu = torch.mean(self.pde.parameter_domain, axis=1) * ones

            parameter_string = ", parameters = " + ", ".join(
                [
                    f"{mu[0, i].detach().cpu():2.2f}"
                    for i in range(self.pde.nb_parameters)
                ]
            )

        else:
            mu = ones
            parameter_string = ""

        if residual:
            x.x.requires_grad_()
            w = self.residual(x, mu).detach().cpu().reshape((n_visu, n_visu)) ** 2
            title = "residual"
        else:
            w_pred = self.network.setup_w_dict(x, mu)
            w = w_pred["w"][:, 0].detach().cpu().reshape((n_visu, n_visu))
            title = "prediction"
            if error:
                w_exact = self.pde.reference_solution(x, mu)
                w_exact = w_exact.detach().cpu().reshape((n_visu, n_visu))
                w = torch.abs(w - w_exact)
                title = "error"

        x1, x2 = np.meshgrid(x1.detach().cpu(), x2.detach().cpu())

        if pde_domain.type == "square_based":
            mask = None
        elif pde_domain.type == "disk_based":
            if pde_domain.mapping == Id_domain:
                distance_to_x1 = (x1 - pde_domain.center[0]) ** 2
                distance_to_x2 = (x2 - pde_domain.center[1]) ** 2
                mask = distance_to_x1 + distance_to_x2 > pde_domain.radius**2
            else:
                # remove points out of the mapped disk
                x = torch.tensor([x1.flatten(), x2.flatten()]).T
                x_inv = pde_domain.inverse(x)
                x1_inv, x2_inv = x_inv[:, 0].detach().cpu(), x_inv[:, 1].detach().cpu()
                distance_to_x1 = (x1_inv - pde_domain.center[0]) ** 2
                distance_to_x2 = (x2_inv - pde_domain.center[1]) ** 2
                mask = distance_to_x1 + distance_to_x2 > pde_domain.radius**2

                # remove points in potential holes
                x = SpaceTensor(x)
                for hole in self.pde.space_domain.list_holes:
                    outside = hole.is_inside(x)[:, 0].detach().cpu()
                    mask = mask | outside
        else:
            print(f"plot_2d_contourf not implemented with {pde_domain.type} domain")
            return

        w = np.ma.array(w, mask=mask)

        fig, ax = plt.subplots(1, 1, figsize=(10 * lx1 / lx2, 10 * lx2 / lx1))

        if colormap == "custom":
            colormap = make_colormap()

        vmax = w.max() * limit_res if residual else None

        im = ax.contourf(
            x1,
            x2,
            w,
            n_contour,
            vmax=vmax,
            cmap="turbo" if colormap is None else colormap,
            zorder=-9,
        )
        if draw_contours:
            ax.contour(
                im,
                levels=im.levels[:: n_contour // n_drawn_contours],
                zorder=-9,
                colors="white",
                alpha=0.5,
                linewidths=0.8,
            )
        fig.colorbar(im, ax=ax)
        ax.set_title(f"{title}{parameter_string}")

        ax.set_aspect("equal")
        plt.gca().set_rasterization_zorder(-1)

        if save_plot:
            plt.savefig(file_name, bbox_inches="tight")

        plt.show()

        return fig, ax
