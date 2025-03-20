import copy
from typing import Callable, List

import torch
from torch import nn
from torch.autograd import grad

from ..equations import pdes
from ..equations.domain import SpaceTensor
from ..nets import activation, mlp, rbfnet, siren
from ..sampling import abstract_sampling


def identity(x, mu, w):
    return w


class PINNx(nn.Module):
    def __init__(self, net, pde: pdes.AbstractPDEx, init_net_bool=False):
        super().__init__()
        self.net = net
        self.nb_unknowns = pde.nb_unknowns
        self.nb_parameters = pde.nb_parameters
        self.pde_dimension_x = pde.dimension_x
        self.init_net_bool = init_net_bool

        self.pde_first_derivative = pde.first_derivative
        self.pde_second_derivative = pde.second_derivative
        self.pde_third_derivative = pde.third_derivative

        try:
            self.post_processing = pde.post_processing
        except AttributeError:
            self.post_processing = identity

        if self.init_net_bool:
            self.net0 = copy.deepcopy(self.net)

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        return self.net.forward(x, mu)

    def get_w(self, data: SpaceTensor, mu: torch.Tensor) -> torch.Tensor:
        x = data.x
        if self.init_net_bool:
            w = self(x, mu) - self.net0.forward(x, mu)
        else:
            w = self(x, mu)
        wp = self.post_processing(data, mu, w)
        return wp

    def setup_w_dict(self, x: SpaceTensor, mu: torch.Tensor) -> dict:
        return {
            "w": self.get_w(x, mu),
            "w_x": None,
            "w_y": None,
            "w_z": None,
            "w_xx": None,
            "w_yy": None,
            "w_zz": None,
            "w_xy": None,
            "w_xz": None,
            "w_yz": None,
            "labels": x.labels,
        }

    def get_first_derivatives(self, w: dict, data: SpaceTensor):
        x = data.x
        ones = torch.ones_like(w["w"][:, 0, None])

        first_derivatives = torch.cat(
            [
                grad(w["w"][:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if self.pde_dimension_x == 1:
            w["w_x"] = first_derivatives.reshape(shape).T
        elif self.pde_dimension_x == 2:
            w["w_x"] = first_derivatives[0].reshape(shape).T
            w["w_y"] = first_derivatives[1].reshape(shape).T
        elif self.pde_dimension_x == 3:
            w["w_x"] = first_derivatives[0].reshape(shape).T
            w["w_y"] = first_derivatives[1].reshape(shape).T
            w["w_z"] = first_derivatives[2].reshape(shape).T
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not implemented in PINNx.get_first_derivatives"
            )

    def get_second_derivatives(self, w: dict, data: SpaceTensor):
        x = data.x
        ones = torch.ones_like(w["w_x"][:, 0, None])

        second_derivatives_x = torch.cat(
            [
                grad(w["w_x"][:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if self.pde_dimension_x == 1:
            w["w_xx"] = second_derivatives_x.reshape(shape).T
        elif self.pde_dimension_x > 1:
            w["w_xx"] = second_derivatives_x[0].reshape(shape).T
            w["w_xy"] = second_derivatives_x[1].reshape(shape).T

            second_derivatives_y = torch.cat(
                [
                    grad(w["w_y"][:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            w["w_yy"] = second_derivatives_y[1].reshape(shape).T

            if self.pde_dimension_x == 3:
                w["w_xz"] = second_derivatives_x[2].reshape(shape).T
                w["w_yz"] = second_derivatives_y[2].reshape(shape).T

                second_derivatives_z = torch.cat(
                    [
                        grad(w["w_z"][:, i, None], x, ones, create_graph=True)[0].T
                        for i in range(self.nb_unknowns)
                    ],
                    axis=-1,
                )

                w["w_zz"] = second_derivatives_z[2].reshape(shape).T

        else:
            raise NotImplementedError(
                "PDE dimension > 3 not implemented in PINNx.get_second_derivatives"
            )

    def get_third_derivatives(self, w: dict, data: SpaceTensor):
        x = data.x
        ones = torch.ones_like(w["w_xx"][:, 0, None])

        third_derivatives_x = torch.cat(
            [
                grad(w["w_xx"][:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if self.pde_dimension_x == 1:
            w["w_xxx"] = third_derivatives_x.reshape(shape).T
        elif self.pde_dimension_x == 2:
            w["w_xxx"] = third_derivatives_x[0].reshape(shape).T
            w["w_xxy"] = third_derivatives_x[1].reshape(shape).T

            third_derivatives_y = torch.cat(
                [
                    grad(w["w_yy"][:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            w["w_xyy"] = third_derivatives_y[0].reshape(shape).T
            w["w_yyy"] = third_derivatives_y[1].reshape(shape).T
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not implemented in PINNx.get_third_derivatives"
            )

    def get_mu_derivatives(self, w: dict, mu: torch.Tensor):
        def compute_derivative(name: str):
            return torch.cat(
                [
                    grad(w[name][:, i, None], mu, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

        def fill_dictionary(derivative: torch.Tensor, name: str):
            if self.nb_parameters == 1:
                w[f"{name}1"] = derivative.reshape(shape).T
            elif self.nb_parameters >= 2:
                for i in range(self.nb_parameters):
                    w[f"{name}{i + 1}"] = derivative[i].reshape(shape).T

        ones = torch.ones_like(mu[:, 0, None])
        shape = (self.nb_unknowns, mu.shape[0])

        fill_dictionary(compute_derivative("w"), "w_mu")

        if self.pde_first_derivative:
            fill_dictionary(compute_derivative("w_x"), "w_x_mu")
            fill_dictionary(compute_derivative("w_y"), "w_y_mu")

        if self.pde_second_derivative:
            fill_dictionary(compute_derivative("w_xx"), "w_xx_mu")
            fill_dictionary(compute_derivative("w_xy"), "w_xy_mu")
            fill_dictionary(compute_derivative("w_yy"), "w_yy_mu")

        if self.pde_third_derivative:
            fill_dictionary(compute_derivative("w_xxx"), "w_xxx_mu")
            fill_dictionary(compute_derivative("w_xxy"), "w_xxy_mu")
            fill_dictionary(compute_derivative("w_xyy"), "w_xyy_mu")
            fill_dictionary(compute_derivative("w_yyy"), "w_yyy_mu")

    def get_second_derivatives_xmu(self, w: dict, data: SpaceTensor, mu: torch.Tensor):
        x = data.x
        ones = torch.ones_like(w["w_x"][:, 0, None])

        second_derivatives_xmu = torch.cat(
            [
                grad(w["w_x"][:, i, None], mu, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if self.pde_dimension_x == 1:
            if self.nb_parameters == 1:
                w["w_xmu1"] = second_derivatives_xmu.reshape(shape).T
            elif self.nb_parameters >= 2:
                for i in range(self.nb_parameters):
                    w[f"w_xmu{i + 1}"] = second_derivatives_xmu[i].reshape(shape).T
        elif self.pde_dimension_x == 2:
            if self.nb_parameters == 1:
                w["w_xmu1"] = second_derivatives_xmu.reshape(shape).T
            elif self.nb_parameters >= 2:
                for i in range(self.nb_parameters):
                    w[f"w_xmu{i + 1}"] = second_derivatives_xmu[i].reshape(shape).T

            second_derivatives_ymu = torch.cat(
                [
                    grad(w["w_y"][:, i, None], mu, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            if self.nb_parameters == 1:
                w["w_ymu1"] = second_derivatives_ymu.reshape(shape).T
            elif self.nb_parameters >= 2:
                for i in range(self.nb_parameters):
                    w[f"w_ymu{i + 1}"] = second_derivatives_ymu[i].reshape(shape).T

        else:
            raise NotImplementedError(
                "PDE dimension > 2 not implemented in PINNx.get_second_derivatives"
            )

    def get_first_derivatives_f(
        self,
        w: dict,
        data: SpaceTensor,
        mu: torch.Tensor,
        f: Callable[[torch.Tensor, torch.Tensor, torch.Tensor], torch.Tensor],
        dim: str,
    ):
        """
        Compute the first derivatives of f(w) with respect to x.

        Args:
            w: dictionary containing the solution w
            x: tensor of batched space coordinates
            mu: tensor of batched parameters
            f: function f to be applied to w
            dim: "x" or "y", the dimension with respect to which the derivative is taken
        """
        possible_dims = ["x", "y"]
        assert (
            dim in possible_dims
        ), f"in get_first_derivatives_f, dim must be 'x' or 'y', got {dim}"

        x = data.x
        ones = torch.ones_like(w["w"][:, 0, None])

        first_derivatives = torch.cat(
            [
                grad(f(w, data, mu)[:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if dim == "x":
            if self.pde_dimension_x == 1:
                w["f_w_x"] = first_derivatives.reshape(shape).T
            elif self.pde_dimension_x == 2:
                w["f_w_x"] = first_derivatives[0].reshape(shape).T
        elif dim == "y":
            assert self.pde_dimension_x > 1, "dim == 'y' but pde_dimension_x < 2"
            w["f_w_y"] = first_derivatives[1].reshape(shape).T

    def get_second_derivatives_f(
        self,
        w: dict,
        data: SpaceTensor,
        mu: torch.Tensor,
        f: Callable[[torch.Tensor, torch.Tensor, torch.Tensor], torch.Tensor],
        dim: str,
    ):
        """
        Compute the second derivatives of f(w) with respect to x.

        Args:
            w: dictionary containing the solution w
            x: tensor of batched space coordinates
            mu: tensor of batched parameters
            f: function f to be applied to w
            dim: "x" or "y", the dimension with respect to which the derivative is taken
        """
        possible_dims = ["xx", "xy", "yy"]
        assert (
            dim in possible_dims
        ), f"in get_first_derivatives_f, dim must be 'x' or 'y', got {dim}"

        x = data.x
        ones = torch.ones_like(w["w"][:, 0, None])

        first_derivatives = torch.cat(
            [
                grad(f(w, data, mu)[:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, x.shape[0])

        if "x" in dim:
            if self.pde_dimension_x == 1:
                f_w_x = first_derivatives.reshape(shape).T
            elif self.pde_dimension_x == 2:
                f_w_x = first_derivatives[0].reshape(shape).T
        elif dim == "yy":
            assert self.pde_dimension_x > 1, "dim == 'yy' but pde_dimension_x < 2"
            f_w_y = first_derivatives[1].reshape(shape).T

        if "x" in dim:
            second_derivatives = torch.cat(
                [
                    grad(f_w_x[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            if self.pde_dimension_x == 1 and dim == "xx":
                w["f_w_xx"] = second_derivatives.reshape(shape).T
            elif self.pde_dimension_x == 2:
                if dim == "xx":
                    w["f_w_xx"] = second_derivatives[0].reshape(shape).T
                elif dim == "xy":
                    w["f_w_xy"] = second_derivatives[1].reshape(shape).T

        elif dim == "yy":
            second_derivatives = torch.cat(
                [
                    grad(f_w_y[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            w["f_w_yy"] = second_derivatives[1].reshape(shape).T

    def get_div_K_grad_w(
        self,
        w: dict,
        data: SpaceTensor,
        mu: torch.Tensor,
        anisotropy_matrix: Callable[
            [torch.Tensor, torch.Tensor, torch.Tensor], torch.Tensor
        ],
    ):
        """
        Compute the second derivatives of f(w) with respect to x.

        Args:
            w: dictionary containing the solution w
            x: tensor of batched space coordinates
            mu: tensor of batched parameters
            f: function f to be applied to w
        """
        assert self.pde_dimension_x in [
            1,
            2,
        ], "get_div_K_grad_w only implemented for 1D and 2D"

        x = data.x
        ones = torch.ones_like(w["w"][:, 0, None])
        shape = (self.nb_unknowns, x.shape[0])

        first_derivatives = torch.cat(
            [
                grad(w["w"][:, i, None], x, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        if self.pde_dimension_x == 1:
            w_x = first_derivatives.reshape(shape).T

            K = anisotropy_matrix(w, data, mu)
            K_w_x = K * w_x

            second_derivatives_x = torch.cat(
                [
                    grad(K_w_x[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            w["div_K_grad_w"] = second_derivatives_x.reshape(shape).T

        else:
            w_x = first_derivatives[0].reshape(shape).T
            w_y = first_derivatives[1].reshape(shape).T

            grad_w = torch.cat([w_x, w_y], axis=1)

            K = anisotropy_matrix(w, data, mu).reshape((-1, 2, 2))
            K_grad_w = torch.einsum("bij,bj->bi", K, grad_w)
            K_grad_w_1 = K_grad_w[:, 0, None]
            K_grad_w_2 = K_grad_w[:, 1, None]

            second_derivatives_x = torch.cat(
                [
                    grad(K_grad_w_1[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            second_derivatives_y = torch.cat(
                [
                    grad(K_grad_w_2[:, i, None], x, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            div_K_grad_w_1 = second_derivatives_x[0].reshape(shape).T
            div_K_grad_w_2 = second_derivatives_y[1].reshape(shape).T

            w["div_K_grad_w"] = div_K_grad_w_1 + div_K_grad_w_2


class MLP_x(nn.Module):
    def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.GenericMLP(
            in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        return self.net.forward(inputs)


class MMLP_x(nn.Module):
    def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.GenericMMLP(
            in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        return self.net.forward(inputs)


# class MMLP_x(nn.Module):
#     """
#     class representing a Multiplicative Multi-Layer Perceptron architecture

#     :param in_size: dimension of inputs
#     :type in_size: int
#     :param out_size: dimension of outputs
#     :type out_size: int

#     :Keyword Arguments:
#     * *activation_type* (``string``) --
#       the type of activation function
#     * *activation_output* (``string``) --
#       the type of activation function for the output
#     * *layer_sizes* (``list[int]``) --
#       the list of neural networks for each layer

#     :Learnable Parameters:
#     * *hidden_layers* (``list[LinearLayer]``)
#         the list of hidden of linear layer
#     * *output_layer* (``LinearLayer``)
#         the last linear layer
#     """

#     def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
#         super().__init__()

#         activation_type = kwargs.get("activation_type", "tanh")
#         activation_output = kwargs.get("activation_output", "id")
#         layer_sizes = kwargs.get("layer_sizes", [10, 20, 20, 20, 5])

#         self.inputs_size = kwargs.get(
#             "inputs_size", pde.dimension_x + pde.nb_parameters
#         )
#         self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

#         self.layer_sizes = [self.inputs_size] + layer_sizes + [self.outputs_size]
#         self.hidden_layers = []
#         self.hidden_layers_mult = []

#         for l1, l2 in zip(self.layer_sizes[:-2], self.layer_sizes[+1:-1]):
#             self.hidden_layers.append(nn.Linear(l1, l2))
#         self.hidden_layers = nn.ModuleList(self.hidden_layers)

#         for layer_size in self.layer_sizes[+1:-1]:
#             self.hidden_layers_mult.append(nn.Linear(self.inputs_size, layer_size))
#         self.hidden_layers_mult = nn.ModuleList(self.hidden_layers_mult)

#         self.output_layer = nn.Linear(self.layer_sizes[-2], self.layer_sizes[-1])
#         self.activation = []

#         for _ in range(len(self.layer_sizes) - 1):
#             self.activation.append(
#                 activation.ActivationFunction(
#                     activation_type, in_size=self.inputs_size, **kwargs
#                 )
#             )

#         self.activation_output = activation.ActivationFunction(
#             activation_output, in_size=self.inputs_size, **kwargs
#         )

#     def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
#         """
#         Apply the network to the inputs .

#         :param inputs: input tensor
#         :type inputs: torch.Tensor
#         :return: the result of the network
#         :rtype: torch.Tensor
#         """
#         inputs = torch.cat([x, mu], axis=1)
#         inputs_mult = torch.cat([x, mu], axis=1)
#         for hidden_layer, hidden_layer_mult, activation_function in zip(
#             self.hidden_layers, self.hidden_layers_mult, self.activation
#         ):
#             inputs = activation_function(hidden_layer(inputs))
#             inputs *= activation_function(hidden_layer_mult(inputs_mult))

#         return self.activation_output(self.output_layer(inputs))

#     def __str__(self):
#         return f"MLP network, with {self.layer_sizes} layers"


class DisMLP_x(nn.Module):
    def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.DiscontinuousMLP(
            in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        return self.net.forward(inputs)


class RBFNet_x(nn.Module):
    def __init__(
        self,
        pde: pdes.AbstractPDEx,
        sampler: abstract_sampling.AbstractSampling,
        nb_func: int = 1,
        **kwargs,
    ):
        super().__init__()
        self.inputs_size = self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)
        self.nb_func = nb_func
        x, mu = sampler.sampling(self.nb_func)
        x_no_grad = x.x.detach()
        mu_no_grad = mu.detach()
        self.net = rbfnet.RBFLayer(
            in_size=self.inputs_size,
            out_size=self.outputs_size,
            points=torch.cat([x_no_grad, mu_no_grad], dim=1),
            **kwargs,
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        return self.net.forward(inputs)


class RBFNet_x_keops(nn.Module):
    def __init__(
        self,
        pde: pdes.AbstractPDEx,
        sampler: abstract_sampling.AbstractSampling,
        nb_func: int = 1,
        **kwargs,
    ):
        super().__init__()
        self.inputs_size = self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)
        self.nb_func = nb_func
        x, mu = sampler.sampling(self.nb_func)
        x_no_grad = x.x.detach()
        mu_no_grad = mu.detach()
        self.net = rbfnet.RBFLayer_keops(
            in_size=self.inputs_size,
            out_size=self.outputs_size,
            points=torch.cat([x_no_grad, mu_no_grad], dim=1),
            **kwargs,
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        return self.net.forward(inputs)


class Fourier_x(nn.Module):
    """Class which create a PINNs for ode based on MLP network enhanced with feature like Fourier
     The network is:
     $$
         MLP(t,x ;theta)
     $$

    -----
    Inputs Parameters:
    - ode (AbstractOde): the ode associated to the problem
    - kwargs for the optional parameters

    Optional Parameters:
    - nb_features (int): number of features added
    - type_feature (str): the name of feature (Fourier, Wavelet etc)
    - bool_feature_mu (bool): a boolean to decide if we compute feature on mu also
    - inputs_size (int): pby defaut it is 1 (time) + nb_parameters. However we can change it (useful for neural operator).
    - outputs_size (int): pby defaut nb_unknowns of the ODE. However we can change it (useful for neural operator).

    """

    def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
        super().__init__()
        self.nb_features = kwargs.get("nb_features", 1)
        self.type_feature = kwargs.get("type_feature", "fourier")
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)
        self.discontinuous = kwargs.get("discontinuous", False)
        self.list_type_features = kwargs.get(
            "list_type_features",
            {
                "x": True,
                "mu": False,
                "xmu": False,
            },
        )
        self.mean_features = kwargs.get(
            "mean_features",
            {
                "x": 0.0,
                "mu": 0.0,
                "xmu": 0.0,
            },
        )
        self.std_features = kwargs.get(
            "std_features",
            {
                "x": 1.0,
                "mu": 0.0,
                "xmu": 0.0,
            },
        )

        de_inputs_size = pde.dimension_x + pde.nb_parameters
        if self.list_type_features["x"]:
            self.features_x = mlp.EnhancedFeatureNet(
                in_size=pde.dimension_x,
                mean=self.mean_features["x"],
                std=self.std_features["x"],
                **kwargs,
            )
            de_inputs_size = de_inputs_size + self.features_x.enhanced_dim
        if self.list_type_features["mu"]:
            self.features_mu = mlp.EnhancedFeatureNet(
                in_size=pde.nb_parameters,
                mean=self.mean_features["mu"],
                std=self.std_features["mu"],
                **kwargs,
            )
            de_inputs_size = de_inputs_size + self.features_mu.enhanced_dim
        if self.list_type_features["xmu"]:
            self.features_xmu = mlp.EnhancedFeatureNet(
                in_size=pde.dimension_x + pde.nb_parameters,
                mean=self.mean_features["xmu"],
                std=self.std_features["xmu"],
                **kwargs,
            )
            de_inputs_size = de_inputs_size + self.features_xmu.enhanced_dim

        self.inputs_size = kwargs.get("inputs_size", de_inputs_size)
        if self.discontinuous:
            self.net = mlp.DiscontinuousMLP(
                in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
            )
        else:
            self.net = mlp.GenericMLP(
                in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
            )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        """
        Function: Forward of the Fourier_t which:
            - create the Fourier feature in x
            - create (if the option is true) the Fourier feature in mu
            - concatenate x, mu and the Fourier feature and call the forward of the MLP

        In practice we can use other features than Fourier
        -----
        Inputs Parameters:
            - x (tensor): sampled time point
            - mu (tensor): sampled ode parameters point
        """
        full_features = torch.zeros((x.shape[0], 0))
        if self.list_type_features["x"]:
            features = self.features_x.forward(x)
            full_features = torch.cat([features, full_features], axis=1)
        if self.list_type_features["mu"]:
            features = self.features_mu.forward(mu)
            full_features = torch.cat([features, full_features], axis=1)
        if self.list_type_features["xmu"]:
            features = self.features_xmu.forward(torch.cat([x, mu], axis=1))
            full_features = torch.cat([features, full_features], axis=1)

        inputs = torch.cat([x, mu, full_features], axis=1)
        return self.net.forward(inputs)


class ModFourier_x:
    pass


class HighwayFourier_x:
    pass


class MultiScale_Fourier_x(nn.Module):
    def __init__(
        self, pde: pdes.AbstractPDEx, means: List[float], stds: List[float], **kwargs
    ):
        super().__init__()
        self.pde = pde
        self.output_size = pde.nb_unknowns
        self.means = means
        self.stds = stds
        self.nb_features = kwargs.get("nb_features", 1)
        self.type_feature = kwargs.get("type_feature", "fourier")
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.Ws = [
            torch.normal(
                self.means[i],
                self.stds[i],
                size=(self.pde.dimension_x, self.nb_features),
            )
            for i in range(0, len(self.stds))
        ]
        self.mods = []
        for i in range(0, len(self.stds)):
            print(self.means[i], " ", self.stds[i])
            self.mods.append(
                mlp.EnhancedFeatureNet(
                    in_size=pde.dimension_x,
                    mean=self.means[i],
                    std=self.stds[i],
                    **kwargs,
                )
            )
        self.mods = nn.ModuleList(self.mods)

        self.nets = []
        for std in self.stds:
            self.nets.append(
                mlp.GenericMLP(
                    2 * self.nb_features + pde.nb_parameters,
                    out_size=self.outputs_size,
                    **kwargs,
                )
            )
        self.nets = nn.ModuleList(self.nets)

        self.last_layer = nn.Linear(
            len(self.stds) * self.outputs_size, self.output_size
        )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        H = []
        for mod, net in zip(self.mods[0:], self.nets[0:]):
            H.append(net.forward(torch.cat([mod.forward(x), mu], axis=1)))
        H = torch.cat(H, axis=1)
        return self.last_layer.forward(H)


class Siren_x(nn.Module):
    def __init__(self, pde: pdes.AbstractPDEx, **kwargs):
        super().__init__()
        self.in_size = pde.dimension_x + pde.nb_parameters
        self.out_size = pde.nb_unknowns

        self.net = siren.SirenNet(self.in_size, self.out_size, **kwargs)

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        y = torch.cat([x, mu], axis=1)
        return self.net.forward(y)


class DGM_x:
    pass


class RBFEnhancedMLP(nn.Module):
    def __init__(
        self,
        pde: pdes.AbstractPDEx,
        sampler: abstract_sampling.AbstractSampling,
        nb_gaussian: int,
        **kwargs,
    ):
        super().__init__()
        self.in_size = pde.dimension_x + pde.nb_parameters
        self.in_size_g = pde.dimension_x
        self.out_size = pde.nb_unknowns
        self.sampler = sampler

        self.nb_func = nb_gaussian
        self.type_g = kwargs.get("type_g", "isotropic")
        self.type_rbf = kwargs.get("type_rbf", "gaussian")
        self.norm = kwargs.get("norm", 2)
        self.points = sampler.sampling_x(nb_gaussian).x

        self.net = mlp.GenericMLP(
            in_size=self.nb_func + self.in_size, out_size=self.out_size, **kwargs
        )

        if self.type_g == "isotropic":
            self.activation = nn.ParameterList(
                [
                    activation.IsotropicRadial(
                        in_size=self.in_size_g, m=self.points[i], **kwargs
                    )
                    for i in range(self.nb_func)
                ]
            )
        else:
            self.activation = nn.ParameterList(
                [
                    activation.AnisotropicRadial(
                        in_size=self.in_size_g, m=self.points[i], **kwargs
                    )
                    for i in range(self.nb_func)
                ]
            )

    def forward(self, x: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
        gaussian_list = self.activation[0](x)
        for i in range(1, self.nb_func):
            gaussian_list = torch.cat((gaussian_list, self.activation[i](x)), dim=1)
        res = self.net.forward(torch.cat([x, mu, gaussian_list], axis=1))
        return res
