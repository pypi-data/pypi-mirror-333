import copy

import torch
from torch import nn
from torch.autograd import grad

from ..equations import pdes
from ..equations.domain import SpaceTensor
from ..nets import mlp, rbfnet
from ..sampling import sampling_pde_txv
from ..sampling import abstract_sampling 

def identity_xv(x, v, mu, w):
    return w


class PINNxv(nn.Module):
    def __init__(self, net, pde: pdes.AbstractPDExv, **kwargs):
        super().__init__()
        self.net = net
        self.nb_unknowns = pde.nb_unknowns
        self.nb_parameters = pde.nb_parameters
        self.pde_dimension_x = pde.dimension_x
        self.pde_dimension_v = pde.dimension_v
        self.init_net_bool = kwargs.get("init_net_bool", False)
        self.moment_sampler = kwargs.get(
            "moment_sampler", sampling_pde_txv.VSampler(pde)
        )

        try:
            self.post_processing = pde.post_processing
        except AttributeError:
            self.post_processing = identity_xv

        if self.init_net_bool:
            self.net0 = copy.deepcopy(self.net)

    def forward(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        return self.net.forward(x, v, mu)

    def get_w(
        self, data: SpaceTensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        x = data.x
        if self.init_net_bool:
            w = self(x, v, mu) - self.net0.forward(x, v, mu)  ### put t at zeo

        else:
            w = self(x, v, mu)
        wp = self.post_processing(data, v, mu, w)
        return wp

    def get_moments(
        self, x: torch.Tensor, mu: torch.Tensor, index: list
    ) -> torch.Tensor:
        # todo
        pass

    def setup_w_dict(
        self, x: SpaceTensor, v: torch.Tensor, mu: torch.Tensor
    ) -> dict:
        return {
            "w": self.get_w(x, v, mu),
            "w_x": None,
            "w_y": None,
            "w_xx": None,
            "w_yy": None,
            "w_v1": None,
            "w_v2": None,
            "w_v1v1": None,
            "w_v2v2": None,
            "labels": x.labels,
        }

    def get_first_derivatives_x(self, w: torch.Tensor, data: SpaceTensor):
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
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not yet implemented in Trainer.get_first_derivatives"
            )

    def get_first_derivatives_v(self, w: torch.Tensor, v: torch.Tensor):
        ones = torch.ones_like(w["w"][:, 0, None])

        first_derivatives = torch.cat(
            [
                grad(w["w"][:, i, None], v, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, v.shape[0])

        if self.pde_dimension_v == 1:
            w["w_v1"] = first_derivatives.reshape(shape).T
        elif self.pde_dimension_v == 2:
            w["w_v1"] = first_derivatives[0].reshape(shape).T
            w["w_v2"] = first_derivatives[1].reshape(shape).T
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not yet implemented in Trainer.get_first_derivatives"
            )

    def get_second_derivatives_x(self, w: torch.Tensor, data: SpaceTensor):
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
        elif self.pde_dimension_x == 2:
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
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not yet implemented in Trainer.get_second_derivatives"
            )

    def get_second_derivatives_v(self, w: torch.Tensor, v: torch.Tensor):
        ones = torch.ones_like(w["w_v1"][:, 0, None])

        second_derivatives_v1 = torch.cat(
            [
                grad(w["w_v1"][:, i, None], v, ones, create_graph=True)[0].T
                for i in range(self.nb_unknowns)
            ],
            axis=-1,
        )

        shape = (self.nb_unknowns, v.shape[0])

        if self.pde_dimension_v == 1:
            w["w_v1v1"] = second_derivatives_v1.reshape(shape).T
        elif self.pde_dimension_v == 2:
            w["w_v1v1"] = second_derivatives_v1[0].reshape(shape).T
            w["w_v1v2"] = second_derivatives_v1[1].reshape(shape).T

            second_derivatives_v2 = torch.cat(
                [
                    grad(w["w_v2"][:, i, None], v, ones, create_graph=True)[0].T
                    for i in range(self.nb_unknowns)
                ],
                axis=-1,
            )

            w["w_v2v2"] = second_derivatives_v2[1].reshape(shape).T
        else:
            raise NotImplementedError(
                "PDE dimension > 2 not yet implemented in Trainer.get_second_derivatives"
            )


class MLP_xv(nn.Module):
    def __init__(self, pde: pdes.AbstractPDExv, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.dimension_v + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.GenericMLP(
            in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
        )

    def forward(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        inputs = torch.cat([x, v, mu], axis=1)
        return self.net.forward(inputs)


class DisMLP_xv(nn.Module):
    def __init__(self, pde, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.dimension_v + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.DiscontinuousMLP(
            in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
        )

    def forward(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        inputs = torch.cat([x, v, mu], axis=1)
        return self.net.forward(inputs)


class RBFNet_xv(nn.Module):
    def __init__(self, 
                 pde: pdes.AbstractPDExv,
                 sampler: abstract_sampling.AbstractSampling, 
                 nb_func:int=1,
                 **kwargs):
        super().__init__()
        self.inputs_size = self.inputs_size = kwargs.get(
            "inputs_size", pde.dimension_x + pde.dimension_v  + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)
        self.nb_func = nb_func
        x,v,mu = sampler.sampling(self.nb_func)
        x_no_grad= x.x.detach()
        v_no_grad = v.detach()
        mu_no_grad=mu.detach()
        self.net = rbfnet.RBFLayer(
            in_size=self.inputs_size, 
            out_size=self.outputs_size,
            points= torch.cat([x_no_grad,v_no_grad,mu_no_grad],dim=1),
            nb_func = self.nb_func,
            **kwargs
        )

    def forward(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        inputs = torch.cat([x, v, mu], axis=1)
        return self.net.forward(inputs)
    

class Fourier_xv(nn.Module):
    """Class which create a PINNs for ode based on MLP network enhanced with feature like Fourier
     The network is:
     $$
         MLP(t,x ;theta)
     $$

    -----
    Inputs Parameters:
    - pde (AbstractPdexv): the ode associated to the problem
    - kwargs for the optional parameters

    Optional Parameters:
    - nb_features (int): number of features added
    - type_feature (str): the name of feature (Fourier, Wavelet etc)
    - inputs_size (int): pby defaut it is 1 (time) + nb_parameters. However we can change it (useful for neural operator).
    - outputs_size (int): pby defaut nb_unknowns of the ODE. However we can change it (useful for neural operator).

    """

    def __init__(self, pde: pdes.AbstractPDExv, **kwargs):
        super().__init__()
        self.nb_features = kwargs.get("nb_features", 1)
        self.type_feature = kwargs.get("type_feature", "fourier")
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)
        self.discontinuous = kwargs.get("discontinuous", False)
        self.list_type_features = kwargs.get(
            "list_type_features",
            {
                "x": True,
                "v": True,
                "xv": False,
                "mu": False,
                "xvmu":False,
            },
        )
        self.mean_features = kwargs.get(
            "mean_features",
            {
                "x": 0.0,
                "v": 0.0,
                "xv": 0.0,
                "mu": 0.0,
                "xvmu": 0.0,
            },
        )
        self.std_features = kwargs.get(
            "std_features",
            {
                "x": 1.0,
                "v": 1.0,
                "xv": 0.0,
                "mu": 0.0,
                "xvmu": 0.0,
            },
        )


        de_inputs_size = pde.dimension_x + pde.dimension_v + pde.nb_parameters
        if self.list_type_features["x"]:
            self.features_x = mlp.EnhancedFeatureNet(
                in_size=pde.dimension_x,
                mean = self.mean_features["x"],
                std = self.std_features["x"],
                **kwargs)
            de_inputs_size = de_inputs_size + self.features_x.enhanced_dim
        if self.list_type_features["v"]:
            self.features_v = mlp.EnhancedFeatureNet(
                in_size=pde.dimension_v,
                mean = self.mean_features["v"],
                std = self.std_features["v"],
                **kwargs)
            de_inputs_size = de_inputs_size + self.features_v.enhanced_dim
        if self.list_type_features["xv"]:
            self.features_xv = mlp.EnhancedFeatureNet(
                in_size=pde.dimension_x + pde.dimension_v,
                mean = self.mean_features["xv"],
                std = self.std_features["xv"],
                **kwargs)
            de_inputs_size = de_inputs_size + self.features_xv.enhanced_dim
        if self.list_type_features["mu"]:
            self.features_mu = mlp.EnhancedFeatureNet(
                in_size= pde.nb_parameters,
                mean = self.mean_features["mu"],
                std = self.std_features["mu"],
                **kwargs)
            de_inputs_size = de_inputs_size + self.features_mu.enhanced_dim
        if self.list_type_features["xvmu"]:
            self.features_xvmu = mlp.EnhancedFeatureNet(
                in_size= pde.dimension_x + pde.dimension_v + pde.nb_parameters,
                mean = self.mean_features["xvmu"],
                std = self.std_features["xvmu"],
                **kwargs)
            de_inputs_size = de_inputs_size + self.features_xvmu.enhanced_dim

        self.inputs_size = kwargs.get("inputs_size", de_inputs_size)
        if self.discontinuous:
            self.net = mlp.DiscontinuousMLP(
                in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
            )
        else:
            self.net = mlp.GenericMLP(
                in_size=self.inputs_size, out_size=self.outputs_size, **kwargs
            )

    def forward(self, x: torch.Tensor, v: torch.Tensor,mu: torch.Tensor) -> torch.Tensor:
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
        if self.list_type_features["v"]:
            features = self.features_v.forward(v)
            full_features = torch.cat([features, full_features], axis=1)
        if self.list_type_features["xv"]:
            features = self.features_xv.forward(torch.cat([x, v], axis=1))
            full_features = torch.cat([features, full_features], axis=1)
        if self.list_type_features["mu"]:
            features = self.features_mu.forward(mu)
            full_features = torch.cat([features, full_features], axis=1)
        if self.list_type_features["xvmu"]:
            features = self.features_xvmu.forward(torch.cat([x, v,mu], axis=1))
            full_features = torch.cat([features, full_features], axis=1)

        inputs = torch.cat([x, v, mu, full_features], axis=1)
        return self.net.forward(inputs)

class MLPxmu_2momentv(nn.Module):
    def __init__(self, pde: pdes.AbstractPDExv, **kwargs):
        super().__init__()
        self.inputs_size = kwargs.get(
            "inputs_size",  pde.dimension_x + pde.dimension_v + pde.nb_parameters
        )
        self.outputs_size = kwargs.get("outputs_size", pde.nb_unknowns)

        self.net = mlp.GenericMLP(
            in_size= pde.dimension_x + pde.nb_parameters, out_size=1+ pde.dimension_v, **kwargs
        )

    def forward(
        self, x: torch.Tensor, v: torch.Tensor, mu: torch.Tensor
    ) -> torch.Tensor:
        inputs = torch.cat([x, mu], axis=1)
        moments = self.net.forward(inputs)
        return moments[:,0]+torch.einsum("bi,bi->b",moments[:,1:],v)