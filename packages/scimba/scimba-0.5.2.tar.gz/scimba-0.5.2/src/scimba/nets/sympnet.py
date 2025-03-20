import torch
from torch import nn


class GradPotential(nn.Module):
    def __init__(self, y_dim, p_dim, width, **kwargs):
        super().__init__()
        self.linear_y = nn.Linear(y_dim, width, bias=False)
        self.linear_p = nn.Linear(p_dim, width)
        self.activation = kwargs.get("activation", nn.Tanh())
        self.scaling = nn.Linear(p_dim, width)

    def forward(self, y, p):
        z = self.activation(self.linear_y(y) + self.linear_p(p))
        return (self.scaling(p) * z) @ self.linear_y.weight


# Parameter size could be made lazy to seemlessly merge with non-parametric implementation.
# Currently, this still works with `p_dim = 0` (despite a zero-size warning), so perhaps it could already be merged.
class SympLayer(nn.Module):
    def __init__(self, y_dim, p_dim, **kwargs):
        super().__init__()
        width = kwargs.get("width", 5)
        self.grad_potential1 = GradPotential(y_dim, p_dim, width)
        self.grad_potential2 = GradPotential(y_dim, p_dim, width)
        self.parameters_scaling = kwargs.get("parameters_scaling", False)
        self.parameters_scaling_number = kwargs.get("parameters_scaling_number", 0)

    def forward(self, x, y, p, sign=1):
        c = (
            p[:, self.parameters_scaling_number, None]
            if self.parameters_scaling
            else 1.0
        )

        if sign == 1:
            x, y = x, y + c * self.grad_potential1(x, p)
            x, y = x + c * self.grad_potential2(y, p), y
        else:
            x, y = x - c * self.grad_potential2(y, p), y
            x, y = x, y - c * self.grad_potential1(x, p)
        return x, y


class SympNet(nn.Module):
    def __init__(self, dim, p_dim, widths=[12] * 20, **kwargs):
        super().__init__()
        self.dim = dim
        self.y_dim = dim // 2
        self.p_dim = p_dim

        self.layers = nn.ModuleList(
            [SympLayer(self.y_dim, p_dim, width=w, **kwargs) for w in widths]
        )

    def forward(self, inputs: torch.Tensor):
        x, y, p = inputs.tensor_split(
            (
                self.y_dim,
                2 * self.y_dim,
            ),
            dim=1,
        )

        for layer in self.layers:
            x, y = layer(x, y, p)

        return torch.cat((x, y), dim=1)

    def inverse(self, inputs: torch.Tensor):
        x, y, p = inputs.tensor_split(
            (
                self.y_dim,
                2 * self.y_dim,
            ),
            dim=1,
        )

        for layer in reversed(self.layers):
            x, y = layer(x, y, p, sign=-1)

        return torch.cat((x, y), dim=1)
