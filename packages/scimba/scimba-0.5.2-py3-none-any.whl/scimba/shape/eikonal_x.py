"""
Create a PINNs model solving the eikonal equation to construct signed distance function
"""

import torch

from ..equations import domain, pdes
from ..pinns import pinn_x
from ..sampling import sampling_parameters, sampling_pde, uniform_sampling


class EikonalLap2D(pdes.AbstractPDEx):
    """
    Eikonal equation in 2D with Penalization term on the Laplacian
    """

    def __init__(self, space_domain):
        super().__init__(
            nb_unknowns=1,
            space_domain=space_domain,
            nb_parameters=0,
            parameter_domain=[],
        )

        self.first_derivative = True
        self.second_derivative = True

    def eik_residual(
        self, w: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """
        Residual of the Eikonal equation

        :param w: Tensor of variables
        :type w:  torch.Tensor
        :param x: Tensor of coordinates
        :type x: torch.Tensor
        :param mu: Tensor of parameters
        :type mu: torch.Tensor
        :return: Residual of the Eikonal equation
        :rtype: torch.Tensor
        """
        u_x = self.get_variables(w, "w_x")
        u_y = self.get_variables(w, "w_y")
        gradu = torch.stack([u_x, u_y])
        norm_gradu = torch.norm(gradu, dim=0)
        return 1.0 - norm_gradu

    def dirichlet_residual(
        self, w: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """
        Boundary conditions residual (Dirichlet) to impose zero at the SDF on the boundary points

        :param w: Tensor of variables
        :type w:  torch.Tensor
        :param x: Tensor of coordinates
        :type x: torch.Tensor
        :param mu: Tensor of parameters
        :type mu: torch.Tensor
        :return: Residual of the Eikonal equation
        :rtype: torch.Tensor
        """
        u = self.get_variables(w, "w")
        return u

    def neumann_residual(
        self,
        w: torch.Tensor,
        x: torch.Tensor,
        n: torch.Tensor,
        mu: torch.Tensor,
        **kwargs,
    ) -> torch.Tensor:
        """
        Boundary conditions residual (Neumann) to impose thata the gradient of the SDF function
        fit the normal to the boundary point

        :param w: Tensor of variables
        :type w:  torch.Tensor
        :param x: Tensor of coordinates
        :type x: torch.Tensor
        :param mu: Tensor of parameters
        :type mu: torch.Tensor
        :return: Residual of the Eikonal equation
        :rtype: torch.Tensor
        """
        u_x = self.get_variables(w, "w_x")
        u_y = self.get_variables(w, "w_y")
        grad_u = (torch.stack([u_x, u_y])[:, :, 0]).transpose(0, 1)

        elementwise_product = torch.mul(n, grad_u)
        dot = torch.sum(elementwise_product, dim=1)
        den = torch.norm(n, dim=1) * torch.norm(grad_u, dim=1)

        neumann = (1.0 - dot / den)[:, None]

        return neumann

    def bc_residual(
        self, w: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        pass

    def lap_residual(
        self, w: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        """
        Penalization term on the Laplacian to obtain regular SDF

        :param w: Tensor of variables
        :type w:  torch.Tensor
        :param x: Tensor of coordinates
        :type x: torch.Tensor
        :param mu: Tensor of parameters
        :type mu: torch.Tensor
        :return: Residual of the Eikonal equation
        :rtype: torch.Tensor
        """
        u_xx = self.get_variables(w, "w_xx")
        u_yy = self.get_variables(w, "w_yy")
        lap = u_xx + u_yy
        return lap

    def residual(
        self, w: torch.Tensor, x: torch.Tensor, mu: torch.Tensor, **kwargs
    ) -> torch.Tensor:
        pass


# bc_points = set of 2D boundary points
# bc_normals = set of 2D normals at the boundary points
def EikonalPINNx(net, **kwargs):
    class EikonalPINNx(torch.nn.Module):
        """
        Class to solve the Eikonal equation with PINNs and compute the SDF

        :params dim: spatial dimension
        :type dim: int
        :params bound: the bound of the square domain where we solve the eikonal equation
        :type bound: int
        :params bc_points: the tensor of the points at the boundary
        :type bc_points: int
        :params bc_normals: the tensor of the normals at the boundary
        :type bc_normals: int
        :params net: the class of the network
        :type net: class
        """

        def __init__(
            self, dim: int, bound: int, bc_points: int, bc_normals: int, **kwargs
        ):
            super().__init__()
            self.xdomain = domain.SpaceDomain(dim, domain.SquareDomain(dim, bound))

            # Eikonal PDE (with penalization term on the Laplacian)
            self.pde = EikonalLap2D(self.xdomain)

            # Sampling on the box domain
            x_sampler = sampling_pde.XSampler(self.pde)
            mu_sampler = sampling_parameters.MuSampler(
                sampler=uniform_sampling.UniformSampling, model=self.pde
            )
            self.sampler = sampling_pde.PdeXCartesianSampler(x_sampler, mu_sampler)

            # PINN
            self.layer_sizes = kwargs.get("layer_sizes", 6 * [32])
            self.activation_type = kwargs.get("activation_type", "sine")

            self.network = net(
                pde=self.pde,
                layer_sizes=self.layer_sizes,
                activation_type=self.activation_type,
            )
            print(self.network)
            self.PINN = pinn_x.PINNx(self.network, self.pde)

            # Boundary points and normals
            self.bc_points = bc_points
            self.bc_normals = bc_normals
            assert self.bc_points.shape[0] == self.bc_normals.shape[0]
            self.n_bc_collocation = bc_points.shape[0]

        def __call__(self, x, mu):
            return self.PINN.get_w(x, mu)

    return EikonalPINNx(**kwargs)
