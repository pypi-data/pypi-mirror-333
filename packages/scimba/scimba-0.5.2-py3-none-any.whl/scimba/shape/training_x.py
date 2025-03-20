from pathlib import Path

import numpy as np
import torch

from .. import device
from ..equations.domain import SpaceTensor
from ..nets.training import AbstractTrainer
from ..nets.training_tools import OptimizerData
from ..shape.eikonal_losses import EikonalLossesData
from ..shape.eikonal_x import EikonalPINNx


class TrainerEikonal(AbstractTrainer):
    FOLDER_FOR_SAVED_NETWORKS = "networks"
    """
        Class to train the PINN on eikonal equation and compute SDF

        :params eik: the PINN for eikonal equation
        :type eik: EikonalPINNx
    """

    def __init__(self, eik: EikonalPINNx, **kwargs):
        self.eik = eik
        self.network = eik.PINN
        self.pde = eik.pde
        self.sampler = eik.sampler

        self.optimizers = kwargs.get("optimizers", OptimizerData(**kwargs))
        self.losses = kwargs.get("losses", EikonalLossesData(**kwargs))
        self.nb_training = 1
        self.FOLDER_FOR_SAVED_NETWORKS = kwargs.get(
            "FOLDER_FOR_SAVED_NETWORKS", self.FOLDER_FOR_SAVED_NETWORKS
        )

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
        self.mu_collocation = None
        self.pre_training = False
        self.post_training = False

    def eik_residual(
        self, x: torch.Tensor, mu: torch.Tensor, **kwargs: dict
    ) -> torch.Tensor:
        """
        Compute the Eikonal residual from sampled space points and parameters.

        This function
            #. evaluates the network at points x and mu
            #. computes its first derivatives at points x and mu
            #. if needed, computes its second derivatives at points x and mu
            #. uses this information to compute the PDE residual

        :params x: the tensor of spatial variables
        :type x: torch.Tensor
        :params mu: the tensor of spatial variables
        :type mu: torch.Tensor
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

        # computation of the second derivatives
        if self.pde.second_derivative:
            # compute d^2w / dx^2
            if self.pde.force_compute_2nd_derivatives_in_residual:
                self.network.get_second_derivatives(w, x)

        return self.pde.eik_residual(w, x, mu, **kwargs)

    def dirichlet_residual(self, x: torch.Tensor, mu: torch.Tensor, **kwargs):
        # get the approximation of the unknown function
        w = self.network.setup_w_dict(x, mu)
        return self.pde.dirichlet_residual(w, x, mu, **kwargs)

    def neumann_residual(
        self, x: torch.Tensor, n: torch.Tensor, mu: torch.Tensor, **kwargs
    ):
        # get the approximation of the unknown function
        w = self.network.setup_w_dict(x, mu)

        # computation of the first derivatives
        if self.pde.first_derivative:
            self.network.get_first_derivatives(w, x)

        return self.pde.neumann_residual(w, x, n, mu, **kwargs)

    def lap_residual(self, x, mu, **kwargs):
        # get the approximation of the unknown function
        w = self.network.setup_w_dict(x, mu)

        # computation of the first derivatives
        if self.pde.first_derivative:
            # compute dw / dx
            self.network.get_first_derivatives(w, x)

        # computation of the second derivatives
        if self.pde.second_derivative:
            # compute d^2w / dx^2
            if self.pde.force_compute_2nd_derivatives_in_residual:
                self.network.get_second_derivatives(w, x)

        return self.pde.lap_residual(w, x, mu, **kwargs)

    def apply_pre_training(self, **kwargs):
        pass

    def apply_post_training(self, **kwargs):
        pass

    def create_batch_data(self, **kwargs):
        return 1, None

    def evaluate_losses(self, epoch, step, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)
        n_bc_collocation = self.eik.n_bc_collocation

        if n_collocation > 0:
            self.x_collocation, self.mu_collocation = self.sampler.sampling(
                n_collocation
            )

            eik_out = self.eik_residual(
                self.x_collocation,
                self.mu_collocation,
                **kwargs,
            )

            zeros = torch.zeros_like(eik_out)
            self.losses.update_eikonal_loss(self.losses.eikonal_f_loss(eik_out, zeros))
            lap_out = self.lap_residual(
                self.x_collocation,
                self.mu_collocation,
                **kwargs,
            )
            self.losses.update_reg_loss(self.losses.reg_f_loss(lap_out, zeros))

        if n_bc_collocation > 0:
            batch_bc_x, batch_bc_mu = self.sampler.bc_sampling(n_bc_collocation)
            batch_bc_x = self.eik.bc_points
            batch_bc_x = SpaceTensor(
                batch_bc_x, torch.zeros_like(batch_bc_x, dtype=int)
            )
            batch_bc_n = self.eik.bc_normals

            dirichlet_out = self.dirichlet_residual(
                batch_bc_x,
                batch_bc_mu,
                **kwargs,
            )
            zeros = torch.zeros_like(dirichlet_out)
            self.losses.update_dirichlet_loss(
                self.losses.dirichlet_f_loss(dirichlet_out, zeros)
            )

            neumann_out = self.neumann_residual(
                batch_bc_x,
                batch_bc_n,
                batch_bc_mu,
                **kwargs,
            )
            self.losses.update_neumann_loss(
                self.losses.neumann_f_loss(neumann_out, zeros)
            )

    def plot(self, n_visu=100000, random=False, sampler=None, filename=None):
        import matplotlib.pyplot as plt

        if sampler is None:
            sampler = self.sampler

        # points in the box
        x = sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        if self.pde.nb_parameters != 0:
            mu = torch.mean(self.pde.parameter_domain, axis=1) * ones
        else:
            mu = torch.tensor([])

        # points on the boundary
        x_bc = self.eik.bc_points
        x_bc = SpaceTensor(x_bc, torch.zeros_like(x_bc, dtype=int))
        # normals = self.eik.bc_normals
        shape = (self.eik.bc_points.shape[0], self.pde.nb_parameters)
        if self.pde.nb_parameters == 0:
            mu_bc = torch.zeros(shape)
        else:
            ones = torch.ones(shape)
            mu_bc = (torch.mean(self.pde.parameter_domain, axis=1) * ones).to(device)

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu().numpy():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        w_pred = self.network.setup_w_dict(x, mu)
        x1, x2 = x.get_coordinates()
        if self.pde.dimension_x == 2:
            fig, ax = plt.subplots(2, 2, figsize=(15, 8))

            # plot loss history
            ax[1, 0] = self.losses.plot(ax[1, 0])

            # plot solution
            im = ax[0, 0].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=w_pred["w"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )
            ax[0, 0].scatter(
                self.eik.bc_points[:, 0].detach().cpu().numpy(),
                self.eik.bc_points[:, 1].detach().cpu().numpy(),
                s=3,
                c="white",
                label="bc",
            )
            fig.colorbar(im, ax=ax[0, 0])
            ax[0, 0].set_title(f"u, parameters = {parameter_string}")
            ax[0, 0].legend()

            # plot solution where u<0
            sol = w_pred["w"][:, 0].detach().cpu().numpy()
            sol[sol > 0.0] = None

            im2 = ax[0, 1].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=sol,
                cmap="gist_ncar",
                label="u(x, y)",
            )
            fig.colorbar(im2, ax=ax[0, 1])
            ax[0, 1].set_title(f"u<0, parameters = {parameter_string}")
            ax[0, 1].legend()

            # plot boundary results
            sdf_bc_dict = self.network.setup_w_dict(x_bc, mu_bc)
            sdf_bc = sdf_bc_dict["w"][:, 0].cpu().detach().numpy()

            x_bc1, x_bc2 = x_bc.get_coordinates()
            im = ax[1, 1].scatter(  # plot dirichlet
                x_bc1.detach().cpu().numpy(),
                x_bc2.detach().cpu().numpy(),
                s=3,
                c=abs(sdf_bc),
                cmap="gist_ncar",
                label="$u_{\\theta}(x, y)$",
            )
            fig.colorbar(im, ax=ax[1, 1])

            # self.network.get_first_derivatives(sdf_bc_dict, x_bc)
            # u_x = self.eik.pde.get_variables(sdf_bc_dict, "w_x")
            # u_y = self.eik.pde.get_variables(sdf_bc_dict, "w_y")
            # grad_u = torch.stack([u_x, u_y])[:,:,0].T

            # ax[1, 1].quiver( # plot neumann
            #     x_bc[::10,0].detach().cpu().numpy(),
            #     x_bc[::10,1].detach().cpu().numpy(),
            #     normals[::10,0].detach().cpu().numpy(),
            #     normals[::10,1].detach().cpu().numpy(),
            #     color="red",
            #     label="normals"
            # )
            # ax[1, 1].quiver(
            #     x_bc[::10,0].detach().cpu().numpy(),
            #     x_bc[::10,1].detach().cpu().numpy(),
            #     grad_u[::10,0].detach().cpu().numpy(),
            #     grad_u[::10,1].detach().cpu().numpy(),
            #     color="blue",
            #     label="grad u"
            # )

            ax[1, 1].set_title(
                f"dirichlet : max = {np.max(np.abs(sdf_bc)):.2e} ; mean = {np.mean(np.abs(sdf_bc)):.2e}"
            )
            ax[1, 1].legend()
            bound_box = self.eik.xdomain.large_domain.bound
            ax[1, 1].set_xlim(bound_box[0][0], bound_box[0][1])
            ax[1, 1].set_ylim(bound_box[1][0], bound_box[1][1])

        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()

    def plot_derivatives(self, n_visu=100000, filename=None):
        import matplotlib.pyplot as plt

        x = self.sampler.sampling_x(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)
        if self.pde.nb_parameters != 0:
            mu = torch.mean(self.pde.parameter_domain, axis=1) * ones
        else:
            mu = torch.tensor([])

        parameter_string = ", ".join(
            [f"{mu[0, i].cpu().numpy():2.2f}" for i in range(self.pde.nb_parameters)]
        )

        w_pred = self.network.setup_w_dict(x, mu)
        self.network.get_first_derivatives(w_pred, x)
        self.network.get_second_derivatives(w_pred, x)

        u_x = self.pde.get_variables(w_pred, "w_x")
        u_y = self.pde.get_variables(w_pred, "w_y")

        u_xx = self.pde.get_variables(w_pred, "w_xx")
        u_yy = self.pde.get_variables(w_pred, "w_yy")

        x1, x2 = x.get_coordinates()
        if self.pde.dimension_x == 2:
            fig, ax = plt.subplots(2, 2, figsize=(15, 8))

            im = ax[0, 0].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=u_x[:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="du_dx",
            )
            fig.colorbar(im, ax=ax[0, 0])
            ax[0, 0].set_title(f"du_dx, parameters = {parameter_string}")
            ax[0, 0].legend()

            im2 = ax[0, 1].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=u_y[:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="du_dy",
            )
            fig.colorbar(im2, ax=ax[0, 1])
            ax[0, 1].set_title(f"du_dy, parameters = {parameter_string}")
            ax[0, 1].legend()

            im3 = ax[1, 0].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=u_xx[:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="d2u_dx2",
            )
            fig.colorbar(im3, ax=ax[1, 0])
            ax[1, 0].set_title("d2u_dx2, parameters = {parameter_string}")
            ax[1, 0].legend()

            im4 = ax[1, 1].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=3,
                c=u_yy[:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="d2u_dy2",
            )
            fig.colorbar(im4, ax=ax[1, 1])
            ax[1, 1].set_title("d2u_dy2, parameters = {parameter_string}")
            ax[1, 1].legend()

            for i in range(2):
                for j in range(2):
                    ax[i, j].scatter(
                        self.eik.bc_points[:, 0].detach().cpu().numpy(),
                        self.eik.bc_points[:, 1].detach().cpu().numpy(),
                        s=3,
                        c="white",
                        label="bc",
                    )

        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()
