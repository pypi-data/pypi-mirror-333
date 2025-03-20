import copy
from abc import ABC, abstractmethod
from pathlib import Path

import torch
from torch import nn

from .. import device
from . import mlp, training_tools


class MassLoss(nn.modules.loss._Loss):
    """A loss based whoch implement

    $$
        sum_i^H (inputs - target)
    $$

    Encode a general MLP architecture
    ---
    Imposed inputs parameters
    - size_average (int): input of the mother class _loss
    - reduce: input of the mother class _loss
    - reduced (str): choose sum or average
    """

    __constants__ = ["reduction"]

    def __init__(self, size_average=None, reduce=None, reduction: str = "mean") -> None:
        super().__init__(size_average, reduce, reduction)

    def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        if self.reduction == "mean":
            return torch.mean(input - target)
        else:
            return torch.sum(input - target)


class AbstractTrainer(ABC):
    """
    This class construct a trainer to solve a PINNs for time space PDE problem

    :param network: the network used
    :type network: nn.Module
    :param losses: the data class for the loss
    :type losses: class

    :param batch_size: the number of data in each batch
    :type batch_size: int
    :param file_name: the name of the file to save the network
    :type file_name: str
    """

    FOLDER_FOR_SAVED_NETWORKS = "networks"

    def __init__(self, network, losses, **kwargs):
        self.network = network
        self.optimizers = kwargs.get(
            "optimizers", training_tools.OptimizerData(**kwargs)
        )
        self.losses = losses
        self.nb_training = 1

        folder_for_saved_networks = Path.cwd() / Path(self.FOLDER_FOR_SAVED_NETWORKS)
        folder_for_saved_networks.mkdir(parents=True, exist_ok=True)

        file_name = kwargs.get("file_name", self.pde.file_name)
        self.file_name = folder_for_saved_networks / file_name

        self.batch_size = kwargs.get("batch_size", 1000)

        self.create_network()
        print(">> load network", self.file_name)
        self.load(self.file_name)

        self.to_be_trained = kwargs.get("to_be_trained", self.to_be_trained)
        self.pre_training = False
        self.post_training = False
        self.used_batch = True

    def create_network(self):
        """
        Create the neural network and associated optimizers.

        This function creates four elements:
            - self.net, the neural network
            - the optimizer data which init the onr or two optimizer and the
            parameters associated
        """
        self.net = self.network.to(device)
        self.optimizers.create_first_opt(self.net.parameters())

    def load(self, file_name: str):
        """Load the network and optimizers from a file.

        :params file_name: name of the .pth file containing the network, losses and optimizers
        :type file_name: str
        """
        try:
            try:
                checkpoint = torch.load(file_name)
            except RuntimeError:
                checkpoint = torch.load(file_name, map_location=torch.device("cpu"))

            self.net.load_state_dict(checkpoint["model_state_dict"])
            self.optimizers.load(self.net.parameters(), checkpoint)
            self.losses.load(checkpoint)

            self.to_be_trained = False
            print("network loaded")

        except FileNotFoundError:
            self.to_be_trained = True
            print("network was not loaded from file: training needed")

    def save(
        self,
        file_name: str,
        epoch: int,
        net_state: dict,
        loss: torch.Tensor,
    ):
        """Save the network and optimizers to a file."""
        dic1 = {epoch: epoch, "model_state_dict": net_state}
        dic2 = self.optimizers.dict_for_save()
        dic3 = self.losses.dict_for_save(loss)
        dic1.update(dic2)
        dic1.update(dic3)
        torch.save(dic1, file_name)

    @abstractmethod
    def evaluate_losses(self, epoch, step, **kwargs):
        pass

    @abstractmethod
    def create_batch_data(self, **kwargs):
        pass

    @abstractmethod
    def apply_pre_training(self, **kwargs):
        pass

    @abstractmethod
    def apply_post_training(self, **kwargs):
        pass

    def train(self, **kwargs):
        epochs = kwargs.get("epochs", 500)

        try:
            best_loss_value = self.losses.loss.item()
        except AttributeError:
            best_loss_value = 1e10

        for i_training in range(0, self.nb_training):
            if self.pre_training:
                self.apply_pre_training(**kwargs)

            epoch = 0

            for epoch in range(epochs):
                m, self.permutation = self.create_batch_data(**kwargs)
                for i in range(0, m, self.batch_size):

                    def closure():
                        if self.optimizers.second_opt_activated:
                            self.optimizers.second_opt.zero_grad()
                        else:
                            self.optimizers.first_opt.zero_grad()

                        self.losses.init_losses()

                        self.evaluate_losses(epoch=epoch, step=i, **kwargs)

                        self.losses.compute_full_loss(self.optimizers, epoch)
                        self.losses.loss.backward(retain_graph=True)
                        return self.losses.loss

                    if self.optimizers.second_opt_activated:
                        self.optimizers.second_opt.step(closure)
                    else:
                        closure()
                        self.optimizers.first_opt.step()
                        self.optimizers.scheduler.step()

                self.losses.update_histories()

                if epoch % 500 == 0:
                    print(
                        f"epoch {epoch: 5d}: current loss = {self.losses.loss_history[-1]:5.2e}"
                    )

                if (self.losses.loss_history[-1] < best_loss_value) | (epoch == 0):
                    string = f"epoch {epoch: 5d}: best loss = {self.losses.loss_history[-1]:5.2e}"
                    if self.optimizers.second_opt_activated:
                        string += "; LBFGS activated"
                    print(string)

                    best_loss = self.losses.loss.clone()
                    best_loss_value = self.losses.loss_history[-1]
                    best_net = copy.deepcopy(self.net.state_dict())
                    self.optimizers.update_best_opt()

                if epoch == 0:
                    initial_loss = self.losses.loss.item()
                else:
                    self.optimizers.test_activation_second_opt(
                        self.net.parameters(),
                        self.losses.loss_history,
                        self.losses.loss.item(),
                        initial_loss,
                        epoch=epoch,
                    )

            print(
                f"epoch {epoch: 5d}: current loss = {self.losses.loss_history[-1]:5.2e}"
            )

            try:
                self.save(
                    self.file_name,
                    epoch,
                    best_net,
                    best_loss,
                )
                print("load network:", self.file_name)
                self.load(self.file_name)
            except UnboundLocalError:
                print("save not work")
                pass

            if self.post_training:
                self.apply_post_training()


class TrainerSupervised(AbstractTrainer):
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
        in_size: int,
        input_data: torch.Tensor,
        out_size: int,
        output_data: torch.Tensor,
        **kwargs,
    ):
        self.in_size = in_size
        self.input_data = input_data
        self.out_size = out_size
        self.output_data = output_data
        self.batch_size = kwargs.get("batch_size", self.DEFAULT_BATCH_SIZE)

        self.network = kwargs.get(
            "network",
            mlp.GenericMLP(
                in_size=self.input_data.shape[1], out_size=self.output_data.shape[1]
            ),
        )
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

        self.create_network()
        self.load(self.file_name)
        self.pre_training = False
        self.post_training = False

    def create_batch_data(self, **kwargs):
        return self.input_data.shape[0], torch.randperm(self.input_data.shape[0])

    def apply_pre_training(self, **kwargs):
        pass

    def apply_post_training(self, **kwargs):
        pass

    def evaluate_losses(self, epoch: int, step: int, **kwargs):
        """
        Function to train the model

        :param epochs: the number of epoch
        :type: int
        """
        indices = self.permutation[step : step + self.batch_size]

        batch_x, batch_y = self.input_data[indices], self.output_data[indices]

        prediction = self.network.forward(batch_x)
        res = self.losses.data_f_loss(prediction, batch_y)
        self.losses.update_data_loss(res)
