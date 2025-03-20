import torch
from torch import nn
from .sympnet import GradPotential



# Parameter size could be made lazy to seemlessly merge with non-parametric implementation.
# Currently, this still works with `p_dim = 0` (despite a zero-size warning), so perhaps it could already be merged.
class HenonLayer(nn.Module):
    def __init__(self, y_dim, p_dim, **kwargs):
        super().__init__()
        width = kwargs.get('width', 5)
        self.grad_potential = GradPotential(y_dim, p_dim, width)
        self.shift = kwargs.get('shift', nn.Linear(p_dim, y_dim))
        self.parameters_scaling =kwargs.get('parameters_scaling', False)
        self.parameters_scaling_number =kwargs.get('parameters_scaling_number', 0)

    def forward(self, x, y, p):
        c = p[:, self.parameters_scaling_number, None]if self.parameters_scaling else 1.0
        x, y = y + c * self.shift(p), -x + c * self.grad_potential(y, p) # 1st iteration
        x, y = y + c * self.shift(p), -x + c * self.grad_potential(y, p) # 2nd iteration
        x, y = y + c * self.shift(p), -x + c * self.grad_potential(y, p) # 3rd iteration
        x, y = y + c * self.shift(p), -x + c * self.grad_potential(y, p) # 4th iteration
        return x, y


class HenonNet(nn.Module):
    def __init__(self, y_dim, p_dim, widths = [12] * 20, **kwargs):
        super().__init__()
        self.y_dim = y_dim
        self.p_dim = p_dim
        self.layers = nn.ModuleList([HenonLayer(y_dim, p_dim, width=w, **kwargs) for w in widths])

    def forward(self, inputs: torch.Tensor):
        x, y, p = inputs.tensor_split((self.y_dim, 2*self.y_dim, ), dim=1)
        for layer in self.layers:
            x, y = layer(x, y, p)
        return torch.cat((x, y), dim=1)