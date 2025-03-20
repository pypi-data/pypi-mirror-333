from pathlib import Path

import torch

from ..nets import training_tools
from ..nets.training import AbstractTrainer


def zero_projector(x, mu, u):
    return torch.zeros_like(u)


def zero_projector_xv(x, v, mu, u):
    return torch.zeros_like(u)


class Projector_x(AbstractTrainer):
    """
    This class construct a trainer to solve a classical supervised problem`

    :param in_size: dimension of the inputs x
    :type out_size: int
    :param in_data: the sample of the inputs data
    :type in_data: torch.Tensor
    :param out_size: dimension of the outputs data y
    :type out_size: int
    :param output_data: the sample of the inputs data y
    :type output_data: torch.Tensor
    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param network: the network used
    :type network: nn.Module
    :param file_name: the name of the file to save the network
    :type file_name: str
    :param optimizers: the optimizers used
    :type optimizers: OptimizerData
    :param losses: the data class for the loss
    :type losses: PinnLossesData
    """

    DEFAULT_FILE_NAME = "network.pth"
    FOLDER_FOR_SAVED_NETWORKS = "networks"
    DEFAULT_BATCH_SIZE = 128

    def __init__(
        self,
        net,
        sampler,
        **kwargs,
    ):
        self.network = net
        self.sampler = sampler
        self.f = kwargs.get("w0", zero_projector)
        self.df = kwargs.get("dw0", None)
        self.optimizers = kwargs.get(
            "optimizers", training_tools.OptimizerData(**kwargs)
        )
        self.losses = kwargs.get(
            "losses", training_tools.SupervisedLossesData(**kwargs)
        )
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.DEFAULT_FILE_NAME)
        self.file_name = folder_for_saved_networks / file_name

        self.batch_size = kwargs.get("batch_size", 1000)

        print("file_name :", file_name)
        self.create_network()
        self.load(self.file_name)
        self.pre_training = True
        self.post_training = False

    def create_batch_data(self, **kwargs):
        return 1, []

    def apply_pre_training(self, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)

        self.x_collocation, self.mu_collocation = self.sampler.sampling(n_collocation)
        self.y = self.f(self.x_collocation, self.mu_collocation)
        if self.df is not None:
            self.dy = self.df(self.x_collocation, self.mu_collocation)

    def apply_post_training(self, **kwargs):
        pass

    def evaluate_losses(self, epoch: int, step: int, **kwargs):
        """
        Function to train the model

        :param epochs: the number of epoch
        :type: int
        """
        y_pred = self.network.setup_w_dict(self.x_collocation, self.mu_collocation)
        self.losses.update_data_loss(self.losses.data_f_loss(y_pred["w"], self.y))

        if self.df is not None:
            self.network.get_first_derivatives(y_pred, self.x_collocation)

            grad_y_pred = y_pred["w_x"]
            if self.sampler.x_sampler.dim == 2:
                grad_y_pred_y = y_pred["w_y"]
                grad_y_pred = torch.cat([grad_y_pred, grad_y_pred_y], dim=1)
            if self.sampler.x_sampler.dim == 3:
                grad_y_pred_z = y_pred["w_z"]
                grad_y_pred = torch.cat([grad_y_pred, grad_y_pred_z], dim=1)

            self.losses.update_grad_data_loss(
                self.losses.data_grad_f_loss(grad_y_pred, self.dy)
            )


class Projector_xv(AbstractTrainer):
    """
    This class construct a trainer to solve a classical supervised problem`

    :param in_size: dimension of the inputs x
    :type out_size: int
    :param in_data: the sample of the inputs data
    :type in_data: torch.Tensor
    :param out_size: dimension of the outputs data y
    :type out_size: int
    :param output_data: the sample of the inputs data y
    :type output_data: torch.Tensor
    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param network: the network used
    :type network: nn.Module
    :param file_name: the name of the file to save the network
    :type file_name: str
    :param optimizers: the optimizers used
    :type optimizers: OptimizerData
    :param losses: the data class for the loss
    :type losses: PinnLossesData
    """

    DEFAULT_FILE_NAME = "network.pth"
    FOLDER_FOR_SAVED_NETWORKS = "networks"
    DEFAULT_BATCH_SIZE = 128

    def __init__(
        self,
        net,
        sampler,
        **kwargs,
    ):
        self.network = net
        self.sampler = sampler
        self.f = kwargs.get("w0", zero_projector_xv)
        self.df = kwargs.get("dw0", zero_projector_xv)
        self.optimizers = kwargs.get(
            "optimizers", training_tools.OptimizerData(**kwargs)
        )
        self.losses = kwargs.get(
            "losses", training_tools.SupervisedLossesData(**kwargs)
        )
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.DEFAULT_FILE_NAME)
        self.file_name = folder_for_saved_networks / file_name

        self.batch_size = kwargs.get("batch_size", 1000)

        print("mmmmm", self.optimizers.learning_rate)

        self.create_network()
        self.load(self.file_name)
        self.pre_training = True
        self.post_training = False

    def create_batch_data(self, **kwargs):
        return 1, []

    def apply_pre_training(self, **kwargs):
        n_collocation = kwargs.get("n_collocation", 1_000)
        print(n_collocation)

        self.x_collocation, self.v_collocation, self.mu_collocation = (
            self.sampler.sampling(n_collocation)
        )
        self.y = self.f(self.x_collocation, self.v_collocation, self.mu_collocation)
        pass

    def apply_post_training(self, **kwargs):
        pass

    def evaluate_losses(self, epoch: int, step: int, **kwargs):
        """
        Function to train the model

        :param epochs: the number of epoch
        :type: int
        """
        y_pred = self.network.get_w(
            self.x_collocation, self.v_collocation, self.mu_collocation
        )

        self.losses.update_data_loss(self.losses.data_f_loss(y_pred, self.y))
