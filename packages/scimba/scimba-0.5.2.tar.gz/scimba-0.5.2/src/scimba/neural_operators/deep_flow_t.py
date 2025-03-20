import torch
from torch import nn

from ..nets import mlp, sympnet


class DiscreteFlow(nn.Module):
    def __init__(self, size: int, parameters_size: int, **kwargs):
        super().__init__()
        self.size = size
        self.parameters_size = parameters_size
        self.flowtype = kwargs.get("flowtype", "mlp")  ## sympnet, invnet etc
        self.rollout = kwargs.get("rollout", 1)
        if self.flowtype == "mlp":
            self.net = mlp.GenericMLP(
                self.size + self.parameters_size, self.size, **kwargs
            )
        if self.flowtype == "sympnet":
            self.net = sympnet.SympNet(self.size, self.parameters_size, **kwargs)

    def forward(self, inputs):
        mu = inputs[..., -self.parameters_size :]
        for i in range(0, self.rollout):
            outputs = self.net.forward(inputs)
            inputs = torch.cat((outputs, mu), dim=-1)
        return outputs

    def inference(self, inputs, N):
        trajectories = torch.zeros((N, inputs.shape[0], self.size))
        print(trajectories.shape)
        mu = inputs[..., -self.parameters_size :]
        for i in range(0, N):
            outputs = self.net.forward(inputs)
            inputs = torch.cat((outputs, mu), dim=-1)
            trajectories[i] = outputs
        return trajectories


class ContinuousFlow(nn.Module):
    def __int__(self, size, parameters_size, **kwargs):
        super().__init__()
        self.size = size
        self.parameters_size = parameters_size
        self.flowtype = kwargs.get("flowtype", "mlp")  ## sympnet, invnet etc
        if self.flowtype == "mlp":
            self.net = mlp.GenericMLP(
                self.size + self.parameters_size + 1, self.size, **kwargs
            )
        if self.flowtype == "sympnet":
            self.net = sympnet.SympNet(
                dim=self.size,
                p_dim=self.parameters_size + 1,
                parameters_scaling_number=-1,
                **kwargs,
            )

    def forward(self, t, x, mu):
        inputs = torch.cat((x, mu, t), dim=1)
        outputs = self.net.forward(inputs)
        return outputs
