import copy
from typing import Callable

import torch
from torch.func import functional_call, jacrev, vmap

from .. import device
from ..equations.domain import SpaceTensor
from ..sampling import sampling_pde_txv
from . import projector_training

# Here the network depend of space and physical parameters
# The weights of the network evolve in time,
# The class needs
# a PDE which gives the domain, the spatial and unknowns dimension
# a parametric model (call here networks)
# objects to sample space and parameters
# a type of initialization method
# a name of time scheme


class NeuralGalerkin_xv:
    FOLDER_FOR_SAVED_NETWORKS = "networks"
    DEFAULT_FILE_NAME = "network_NG.pth"

    def __init__(self, pde_xv, sampler_x, sampler_v, sampler_mu, network, **kwargs):
        self.pde = pde_xv
        self.sampler_x = sampler_x
        self.sampler_v = sampler_v
        self.sampler_mu = sampler_mu
        self.network = copy.deepcopy(network)
        # self.network_backup = copy.deepcopy(network)
        self.type_init = kwargs.get("type_init", 0)
        self.scheme = kwargs.get("scheme", "euler_ex")
        self.matrix_regularization = kwargs.get("matrix_regularization", 1e-5)
        self.ls_bool = kwargs.get("ls_bool", False)  # active the least square solver
        self.subsample = kwargs.get("subsample", 100)
        self.subsample_bool = kwargs.get("subsample_bool", False)

        self.nb_params = len(
            torch.nn.utils.parameters_to_vector(self.network.parameters())
        )
        print("/////////////// Neural Galerkin method ///////////////")
        print("///// Time scheme: ", self.scheme)
        print("///// Type of initilization: ", self.type_init)
        print(
            "///// Activation of the subsampling: ",
            self.subsample_bool,
            " and activation of Least Square solver",
            self.ls_bool,
        )
        print("///// The model used:", self.nb_params, " of parameters")

    def compute_initial_data(
        self,
        projector=None,
        w0=None,
        lr_init: int = 1e-2,
        epoch_init: int = 2000,
        n_collocation: int = 2000,
        file_name: str = DEFAULT_FILE_NAME,
    ):
        """
        3 ways of computing the initial data:
        - we gives a projector which gives explicitly the init weights
        - we make a learning step
        - we put the inital condition int the model with bc add (Hesthaven style);
        this requires storing the initial condition
        """
        if self.type_init == 0:
            projector(self.network)
        if self.type_init == 1:
            self.sampler = sampling_pde_txv.PdeXVCartesianSampler(
                self.sampler_x, self.sampler_v, self.sampler_mu
            )
            self.projector = projector_training.Projector_xv(
                self.network,
                self.sampler,
                w0=w0,
                file_name=file_name,
                learning_rate=lr_init,
            )
            self.projector.train(epochs=epoch_init, n_collocation=n_collocation)
        if self.type_init == 2:
            pass

    def sampling(self):
        """
        this method calls the sampling function of the two samplers,
        and saves the number of points
        """
        self.x = self.sampler_x.sampling(self.N)
        self.x_no_grad = copy.deepcopy(self.x.x)
        self.x_no_grad.requires_grad = False
        self.v = self.sampler_v.sampling(self.N)
        self.v_no_grad = copy.deepcopy(self.v)
        self.v_no_grad.requires_grad = False
        self.mu = self.sampler_mu.sampling(self.N)
        self.mu_no_grad = copy.deepcopy(self.mu)
        self.mu_no_grad.requires_grad = False

    def params_to_vect(self):
        """
        this function takes the current paramaters of the model,
        and concatenates them in the vector theta
        """
        self.theta = torch.nn.utils.parameters_to_vector(self.network.parameters())

    def vect_to_params(self, theta: torch.Tensor):
        """
        this function take a vector theta and put it in the paramaters models
        """
        torch.nn.utils.vector_to_parameters(theta, self.network.parameters())

    def jacobian(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        """
        this function compute the Jacobians of the model
        with respect to the weights at each (x,mu) of a tensor
        If we have n points, we have n jacobians J(\theta)(x,mu).
        """
        params = {k: v.detach() for k, v in self.network.named_parameters()}

        def fnet(theta, x, v, mu):
            return functional_call(
                self.network, theta, (x.unsqueeze(0), v.unsqueeze(0), mu.unsqueeze(0))
            ).squeeze(0)

        # (None, 0, 0) means that:
        #   - the first argument (params) is not batched
        #   - the second argument (x) is batched along the first dimension
        #   - the third argument (v) is batched along the first dimension
        #   - the fourth argument (mu) is batched along the first dimension
        jac = vmap(jacrev(fnet), (None, 0, 0, 0))(params, x, v, mu).values()

        # jac is a dict of jagged tensors, we want to:
        #   - first reshape each jagged tensor to (N, nb_unknowns, nb_params)
        #   - then concatenate them along the last dimension
        return torch.cat(
            [j.reshape((self.N, self.pde.nb_unknowns, -1)) for j in jac], axis=-1
        )

    def compute_model(self):
        """
        this function computes the mass matrix and the RHS of the Neural Galerkin method
        M(theta)=frac1/N sum (J(theta) otimes J(theta))(x,mu)
        F(theta)=frac1/N sum (J(theta) f(theta))(x,mu)
        """
        self.m_jac = self.jacobian(self.x_no_grad, self.v_no_grad, self.mu_no_grad)
        if not self.ls_bool:
            self.M = (
                torch.einsum("bjs,bjr->sr", self.m_jac, self.m_jac) / self.N
                + self.eye_matrix
            )

        w = self.network.setup_w_dict(self.x, self.v, self.mu)
        self.network.get_first_derivatives_x(w, self.x)
        self.network.get_first_derivatives_v(w, self.v)

        if self.pde.second_derivative_x:
            self.network.get_second_derivatives_x(w, self.x)
        if self.pde.second_derivative_v:
            self.network.get_second_derivatives_v(w, self.v)

        large_f = self.residual(w, self.x, self.v, self.mu)
        if not self.ls_bool:
            self.f = torch.einsum("bji,bj->i", self.m_jac, large_f) / self.N
        else:
            self.f = large_f

    def residual(
        self, w: torch.Tensor, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        """this function computes the PDE residual and concatenates it, if needed"""
        pde_residual = self.pde.residual(w, x, v, mu)
        if isinstance(pde_residual, torch.Tensor):
            return pde_residual
        elif isinstance(pde_residual, tuple):
            return torch.cat(pde_residual, axis=1)
        else:
            raise ValueError("pde_residual should be a tensor or a tuple of tensors")

    def compute_error_in_time(self, time, sol_exact):
        """this function computes the evolution of error of the solution in time"""
        N = 5000
        x = self.sampler_x.sampling(N)
        v = self.sampler_v.sampling(N)
        mu = self.sampler_mu.sampling(N)
        w_pred = self.network.setup_w_dict(x, v, mu)
        t = time * torch.ones(mu.shape[0], dtype=torch.double, device=device)
        t = t[:, None]
        w_exact = sol_exact(t, x, v, mu)
        err_abs = (
            torch.sum((w_pred["w"] - w_exact) ** 2, dim=0).detach().cpu() / N
        ) ** 0.5
        norm = (torch.sum(w_exact**2, dim=0).detach().cpu() / N) ** 0.5
        return err_abs / norm

    def time_step_matrix(self, dt):
        self.sampling()
        self.params_to_vect()
        if self.scheme == "euler_exp":
            self.euler_exp_matrix(dt)
        if self.scheme == "rk2":
            self.rk2_matrix(dt)
        self.list_theta.append(self.theta.detach())
        self.vect_to_params(self.theta)

    def time_step_ls(self, dt):
        self.sampling()
        self.params_to_vect()
        if self.scheme == "euler_exp":
            self.euler_exp_ls(dt)
        self.list_theta.append(self.theta.detach())
        self.vect_to_params(self.theta)

    def euler_exp_ls(self, dt):
        self.compute_model()
        J = torch.squeeze(self.m_jac)
        b = torch.squeeze(self.f)

        if self.subsample_bool:
            perm = torch.randperm(self.nb_params)
            S_t = perm[: self.subsample]
            # S_t =torch.sort(S_t).values.int()
            J = J[:, S_t]
        delta_t = torch.linalg.lstsq(J, b).solution
        if self.subsample_bool:
            self.theta[S_t] = self.list_theta[-1][S_t] + dt * delta_t
        else:
            self.theta = self.list_theta[-1] + dt * delta_t

    def euler_exp_matrix(self, dt):
        self.compute_model()
        b = self.f.flatten()
        if self.subsample_bool:
            perm = torch.randperm(self.nb_params)
            S_t = perm[: self.subsample]
            b = b[S_t]
            self.M = (self.M[:, S_t])[S_t, :]
        delta_t = torch.linalg.solve(self.M, b)
        if self.subsample_bool:
            self.theta[S_t] = self.list_theta[-1][S_t] + dt * delta_t
        else:
            self.theta = self.list_theta[-1] + dt * delta_t

    def rk2_matrix(self, dt):
        self.compute_model()
        # M = torch.linalg.cholesky(self.M)
        # update = torch.cholesky_solve(self.f[:, None], M)[:, 0]
        b = self.f.flatten()
        if self.subsample_bool:
            perm = torch.randperm(self.nb_params)
            S_t = perm[: self.subsample]
            b = b[S_t]
            self.M = (self.M[:, S_t])[S_t, :]
        delta_t = torch.linalg.solve(self.M, b)
        if self.subsample_bool:
            self.theta[S_t] = self.list_theta[-1][S_t] + 0.5 * dt * delta_t
        else:
            self.theta = self.list_theta[-1] + 0.5 * dt * delta_t

        self.vect_to_params(self.theta)
        self.compute_model()
        #M = torch.linalg.cholesky(self.M)
        #update = torch.cholesky_solve(self.f[:, None], M)[:, 0]
        b = self.f.flatten()
        if self.subsample_bool:
            b= b[S_t]
            self.M=(self.M[:,S_t])[S_t,:]
        delta_t = torch.linalg.solve(self.M, b)
        if self.subsample_bool:
            self.theta[S_t] = self.list_theta[-1][S_t] + dt * delta_t
        else:
            self.theta = self.list_theta[-1] + dt * delta_t


    def time_loop(
        self, dt: float = 1e-5, T: float = 0.1, sol_exact=None, n_collocation=2000
    ):
        self.N = n_collocation
        self.T = T
        nt = 0
        time = 0.0
        self.list_theta = []
        self.params_to_vect()

        self.eye_matrix = self.matrix_regularization * torch.eye(self.theta.shape[0])

        self.list_theta.append(self.theta)
        self.times = [0.0]
        self.errors = []

        while time < T:
            if time + dt > T:
                dt = T - time
            # if nt % 1 == 0:
            #     print("iteration ", nt, "error", self.list_err[nt])
            if self.ls_bool:
                self.time_step_ls(dt)
            else:
                self.time_step_matrix(dt)
            time = time + dt
            if sol_exact is not None:
                error = self.compute_error_in_time(time, sol_exact)
                self.errors.append(error)
                print("current iteration : ", nt, "error: ", error)
            else:
                print("current iteration :", nt)
                # self.list_err.append(err_abs)
            nt = nt + 1

            self.times.append(time)

    def plot(
        self, n_visu=20000, sol_exact=None, mu=None, v_given=torch.tensor([0.0, 0.0])
    ):
        import matplotlib.pyplot as plt

        t = torch.ones(n_visu, dtype=torch.double, device=device) * self.T
        t = t[:, None]
        x = self.sampler_x.sampling(n_visu)
        v = self.sampler_v.sampling(n_visu)
        shape = (n_visu, self.pde.nb_parameters)
        ones = torch.ones(shape)

        if self.pde.nb_parameters == 0:
            t_mu = torch.empty(x.size()[0], 0)
        else:
            if mu is None:
                t_mu = torch.mean(self.pde.parameter_domain, axis=1) * ones
            else:
                t_mu = mu * ones

        w_pred = self.network.setup_w_dict(x, v, t_mu)
        self.network.get_first_derivatives_x(w_pred, x)
        self.network.get_first_derivatives_v(w_pred, v)

        if self.pde.dimension_x == 1:
            if sol_exact is not None:
                w_exact = sol_exact(t, x, v, mu)
                print(
                    "erreur ",
                    torch.sum((w_pred["w"] - w_exact) ** 2).detach().cpu()
                    / (self.N**self.pde.dimension_x),
                )

            fig, ax = plt.subplots(2, 2, figsize=(15, 10))
            x = x.get_coordinates()
            im = ax[0, 0].scatter(
                x.detach().cpu().numpy(),
                v.detach().cpu().numpy(),
                s=4,
                c=w_pred["w"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="w_theta(x, y)",
            )
            fig.colorbar(im, ax=ax[0, 0])
            ax[0, 0].set_title("prediction")
            ax[0, 0].legend()

            if sol_exact is not None:
                im = ax[0, 1].scatter(
                    x.detach().cpu().numpy(),
                    v.detach().cpu().numpy(),
                    s=4,
                    c=w_exact[:, 0].detach().cpu().numpy(),
                    cmap="gist_ncar",
                    label="w_ref(x, y)",
                )
            fig.colorbar(im, ax=ax[0, 1])
            ax[0, 1].set_title(" reference")
            ax[0, 1].legend()

            im = ax[1, 0].scatter(
                x.detach().cpu().numpy(),
                v.detach().cpu().numpy(),
                s=10,
                c=w_pred["w_x"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="dx v_theta(x, y)",
            )
            fig.colorbar(im, ax=ax[1, 0])

            ax[1, 0].set_title("dx prediction")
            ax[1, 0].legend()

            im = ax[1, 1].scatter(
                x.detach().cpu().numpy(),
                v.detach().cpu().numpy(),
                s=10,
                c=w_pred["w_v1"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label=" dy w_theta(x, y)",
            )
            fig.colorbar(im, ax=ax[1, 1])
            ax[1, 1].set_title("dy prediction")
            ax[1, 1].legend()

        elif self.pde.dimension_x == 2:
            ones = torch.ones(n_visu, self.pde.dimension_v)
            v = ones * v_given[None, :]
            w_pred = self.network.setup_w_dict(x, v, t_mu)

            if sol_exact is not None:
                w_exact = sol_exact(t, x, v, mu)
                print(
                    "erreur ",
                    torch.sum((w_pred["w"] - w_exact) ** 2).detach().cpu()
                    / (self.N**self.pde.dimension_x),
                )

            fig, ax = plt.subplots(2, 2, figsize=(15, 8))
            x1, x2 = x.get_coordinates()
            im_sol = ax[0, 0].scatter(
                x1.detach().cpu().numpy(),
                x2.detach().cpu().numpy(),
                s=4,
                c=w_pred["w"][:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="w_theta(x, y)",
            )

            fig.colorbar(im_sol, ax=ax[0, 0])
            ax[0, 0].set_title("prediction")
            ax[0, 0].legend()

            integration_pts, integral = self.compute_integral_wrt_v(
                self.set_integral_data,
                n_v=5000,
                n_x=10000,
            )

            im_sol = ax[1, 0].scatter(
                integration_pts.x[:, 0].detach().cpu().numpy(),
                integration_pts.x[:, 1].detach().cpu().numpy(),
                s=4,
                c=integral[:, 0].detach().cpu().numpy(),
                cmap="gist_ncar",
                label="w_theta(x, y)",
            )

            fig.colorbar(im_sol, ax=ax[1, 0])
            ax[1, 0].set_title("Mean prediction")
            ax[1, 0].legend()

            if sol_exact is not None:
                im = ax[0, 1].scatter(
                    x1.detach().cpu().numpy(),
                    x2.detach().cpu().numpy(),
                    s=4,
                    c=w_exact[:, 0].detach().cpu().numpy(),
                    cmap="gist_ncar",
                    label="w_ref(x, y)",
                )
                fig.colorbar(im, ax=ax[0, 1])
                ax[0, 1].set_title("reference")
                ax[0, 1].legend()

                def set_integral_data_exact(x: torch.Tensor, v: torch.Tensor):
                    t = self.T * torch.ones(x.shape[0], 1)
                    return sol_exact(t, x, v, None)

                integration_pts, integral = self.compute_integral_wrt_v(
                    set_integral_data_exact,
                    n_v=5000,
                    n_x=10000,
                )

                im_sol = ax[1, 1].scatter(
                    integration_pts.x[:, 0].detach().cpu().numpy(),
                    integration_pts.x[:, 1].detach().cpu().numpy(),
                    s=4,
                    c=integral[:, 0].detach().cpu().numpy(),
                    cmap="gist_ncar",
                    label="w_theta(x, y)",
                )

                fig.colorbar(im_sol, ax=ax[1, 1])
                ax[1, 1].set_title("Mean reference")
                ax[1, 1].legend()

        plt.show()

    def set_integral_data(self, x: torch.Tensor, v: torch.Tensor):
        t_mu = torch.ones(x.shape[0], 1)
        return self.network.setup_w_dict(x, v, t_mu)["w"]

    def compute_integral_wrt_v(
        self,
        f: Callable[[torch.tensor, torch.tensor], torch.tensor],
        n_x: int = 200,
        n_v: int = 200,
    ):
        """Approximates F(x) = \int f(x, v) dv"""
        x = self.sampler_x.sampling(n_x)
        v = self.sampler_v.sampling(n_v)
        x_no_grad = copy.deepcopy(x.x)
        x_no_grad.requires_grad = False
        v_no_grad = copy.deepcopy(v)
        v_no_grad.requires_grad = False
        # t_mu is only used in set_integral_data

        shape_f = f(self.sampler_x.sampling(1), self.sampler_v.sampling(1)).shape[1:]
        ones = torch.ones_like(v_no_grad)

        integral = torch.zeros((n_x, *shape_f))

        for i, x_i in enumerate(x_no_grad):
            x_i_ = SpaceTensor(x_i * ones)
            integral[i, ...] = torch.mean(f(x_i_, v_no_grad), axis=0)

        return x, integral
