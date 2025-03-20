from pathlib import Path

import torch
from torch.distributions import MultivariateNormal

from .. import device
from ..nets import mlp, training, training_tools
from . import generativelosses, normalizingflows, simpleflows


class TrainerLikelihood(training.AbstractTrainer):
    """
    This class construct a trainer to optimize likehihood
    associated to a targer distribution :math:`p(y)` or :math:`p(y\mid x)`

    :param out_size: dimension of the distribution data y
    :type out_size: int
    :param output_data: the sample of the target distribution  y
    :type output_data: torch.Tensor
    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param conditional: if there is or not conditional data
    :type conditiona: boolean
    :param cond_size: dimension of the conditional data x
    :type cond_size: int
    :param cond_data: the sample of the conditiona distribution x
    :type cond_data: torch.Tensor

    """

    DEFAULT_FILE_NAME = "normalizingflow.pth"
    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, out_size, output_data, **kwargs):
        self.out_size = out_size
        self.output_data = output_data.to(device)
        self.batch_size = kwargs.get("batch_size", 100)
        self.conditional = kwargs.get("conditional", False)
        self.cond_size = kwargs.get("cond_size", 0)
        self.cond_data = kwargs.get("cond_data", torch.zeros(0, 0))

        prior = MultivariateNormal(torch.zeros(out_size), torch.eye(out_size))
        flows = [
            simpleflows.AffineConstantFlow(
                net=mlp.GenericMLP, dim=out_size, dim_conditional=self.cond_size
            )
            for _ in range(4)
        ]
        normalizingflow = normalizingflows.NormalizingFlow(prior, flows)
        self.network = kwargs.get("network", normalizingflow)

        self.optimizers = kwargs.get(
            "optimizers", training_tools.OptimizerData(**kwargs)
        )
        self.losses = kwargs.get(
            "losses", generativelosses.GenerativeLossesData(**kwargs)
        )
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.DEFAULT_FILE_NAME)
        self.file_name = folder_for_saved_networks / file_name

        self.create_network()
        self.load(self.file_name)

        self.to_be_trained = kwargs.get("to_be_trained", self.to_be_trained)
        self.pre_training = False
        self.post_training = False

    def apply_pre_training(self, **kwargs):
        pass

    def apply_post_training(self, **kwargs):
        pass

    def create_batch_data(self, **kwargs):
        return self.output_data.shape[0], torch.randperm(self.output_data.shape[0])

    def evaluate_losses(self, epoch: int, step: int, **kwargs):
        """
        Function to train the model

        :param epochs: the number of epoch
        :type: int
        """

        indices = self.permutation[step : step + self.batch_size].to(device)
        if self.conditional:
            batch_x, batch_y = (
                self.cond_data[indices],
                self.output_data[indices],
            )
        else:
            batch_y = self.output_data[indices]
            batch_x = torch.zeros((self.batch_size, 0))

        prediction = self.network.forward(
            batch_y, batch_x
        )  ## gives the log of the probability
        self.losses.update_likelihood_loss(prediction)
