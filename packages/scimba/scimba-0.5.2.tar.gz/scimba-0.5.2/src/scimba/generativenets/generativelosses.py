from pathlib import Path

import torch
from torch import nn
from .. import device

from ..nets.training_tools import AbstractLoss
from ..nets.training_tools import OptimizerData

class GenerativeLossesData(AbstractLoss):
    DEFAULT_W_LIKELIHOOD = 1.0
    DEFAULT_W_CONSTRAINTS = 1.0
    """
        Class to create optimize and store the Losses for supervised training

        :param likelihood_loss_bool: activate or not likelihood loss
        :type constraints_loss_bool: bool
        :param constrains_loss_bool: activate or not loss on weights constraints
        :type constraints_loss_bool: bool


        :param w_like: weight for the likelihood loss
        :type w_like: float
        :param w_constraints: weights for the constraints loss
        :type w_constraints: float
    """

    def __init__(self, **kwargs):
        self.likelihood_loss_bool = kwargs.get("likelihood_loss_bool", True)
        self.constraints_loss_bool = kwargs.get("constraints_loss_bool", False)
        self.constraints_f_loss = kwargs.get("constraints_f_loss", None)

        self.w_like = kwargs.get("w_data", self.DEFAULT_W_LIKELIHOOD )
        self.w_constraints = kwargs.get(
            "w_constraints", self.DEFAULT_W_CONSTRAINTS * self.constraints_loss_bool
        )

        self.loss_history = []
        self.likelihood_loss_history = []
        self.constraints_loss_history = []

    def try_to_load(self, checkpoint, string):
        try:
            return checkpoint[string]
        except KeyError:
            return None

    def load(self, checkpoint):
        """
        Load the losses history of a file.

        :param checkpoint: name of the .pth file containing the losses history
        :type checkpoint: str
        """
        self.loss = self.try_to_load(checkpoint, "loss")
        self.loss_history = self.try_to_load(checkpoint, "loss_history")
        self.likelihood_loss_history = self.try_to_load(checkpoint, "likelihood_loss_history")
        self.constraints_loss_history = self.try_to_load(
            checkpoint, "constraints_loss_history"
        )

    def init_losses(self):
        """
        initialize all the sublosses at zero
        """
        self.loss = torch.tensor(0.0)
        self.likelihood_loss = torch.tensor(0.0)
        self.constraints_loss = torch.tensor(0.0)


    def update_likelihood_loss(self, value: torch.Tensor):
        """
        update the value fo the likelihood loss

        :param value: the current value of the likelihood loss
        :type value: torch.Tensor
        """
        self.likelihood_loss = value

    def update_constraints_loss(self, value: torch.Tensor):
        """
        update the value fo the constraints loss

        :param value: the current value of the constraints loss
        :type value: torch.Tensor
        """
        self.contrains_loss = value

    def compute_full_loss(self, optimizers: OptimizerData, epoch: int):
        """
        compute the full loss as the combination of all the losses
        """
    

        self.loss = (
            +self.w_like * self.likelihood_loss + self.w_constraints * self.constraints_loss
        )

    def update_histories(self):
        """
        Add all the current loss values in the histories
        """
        self.loss_history.append(self.loss.item())
        if self.likelihood_loss_bool:
            self.likelihood_loss_history.append(self.likelihood_loss.item())
        if self.constraints_loss_bool:
            self.constraints_loss_history.append(self.constraints_loss.item())

    def dict_for_save(self, best_loss: torch.Tensor) -> dict:
        """
        Compute the dictionary for the losses which will be save by the trainer

        :param best_loss: the current value of best full loss
        :type value: torch.Tensor
        :return: dictionary of all data svaed for the losses
        :rtype: dict
        """
        dic = {
            "loss": best_loss,
            "loss_history": self.loss_history,
            
        }
        if self.likelihood_loss_bool:
            dic["likelihood_loss_history"] = self.likelihood_loss_history
        if self.constraints_loss_bool:
            dic["constraints_loss_history"] = self.constraints_loss_history
        return dic

    def plot(self, ax):
        """
        Gives the axe contains the plot of the loss histories

        :params ax: the axe which containts the plot
        :type ax: plt.Axes
        :return: the axe which containts the plot
        :type ax: plt.Axes
        """

        ax.semilogy(self.loss_history, label="total loss")
        if self.likelihood_loss_bool:
            ax.semilogy(self.likelihood_loss_history, label="data")
        if self.constraints_loss_bool:
            ax.semilogy(self.constraints_loss_history, label="contrains")
        ax.set_title("loss history")
        ax.legend()
        return ax