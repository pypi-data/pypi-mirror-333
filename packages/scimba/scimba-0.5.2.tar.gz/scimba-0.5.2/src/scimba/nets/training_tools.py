import copy
from abc import ABC, abstractmethod

import torch


class OptimizerData:
    """
    Class to store and create the Optimizer parameters

    :param learning_rate: value of the learning rate
    :type learning_rate: float
    :param decay: value of the decay for the learning rate
    :type decay: float
    :param step_size: number of gradient step between two decay
    :type step_size: int

    """

    def __init__(self, **kwargs):
        self.learning_rate = kwargs.get("learning_rate", 1e-3)
        self.decay = kwargs.get("decay", 0.99)
        self.step_size = kwargs.get("step_size", 20)

        self.switch_to_LBFGS = kwargs.get("switch_to_LBFGS", False)
        self.switch_to_LBFGS_at = kwargs.get("switch_to_LBFGS_at", 1e10)
        self.LBFGS_history_size = kwargs.get("LBFGS_history_size", 15)
        self.LBFGS_max_iter = kwargs.get("LBFGS_max_iter", 5)
        self.LBFGS_switch_ratio = kwargs.get("LBFGS_switch_ratio", 500)
        self.LBFGS_switch_plateau = kwargs.get(
            "LBFGS_switch_plateau", [50, 10]
        )  # check for a plateau after 50 iterations, on the last 10 iterations

    def create_second_opt(self, parameters: list[torch.nn.Parameter]):
        """
        create the second optimizer using the parameters of the network.
        This second optimize can replace the first one during the training

        :params parameters: the parameters of the network
        :type parameters: list[Parameter]
        """
        self.second_opt = torch.optim.LBFGS(
            parameters,
            history_size=self.LBFGS_history_size,
            max_iter=self.LBFGS_max_iter,
            line_search_fn="strong_wolfe",
        )
        self.second_opt_activated = True

    def create_first_opt(self, parameters: list[torch.nn.Parameter]):
        """
        create the main optimizer using the parameters of the network.

        :params parameters: the parameters of the network
        :type parameters: list[Parameter]
        """
        self.first_opt = torch.optim.Adam(parameters, lr=self.learning_rate)
        self.scheduler = torch.optim.lr_scheduler.StepLR(
            self.first_opt, step_size=self.step_size, gamma=self.decay
        )
        self.second_opt = None
        self.second_opt_activated = False

    def load(self, parameters: list[torch.nn.Parameter], checkpoint: str):
        """
        Load the network and optimizers from a file.

        :params parameters: the parameters of the network
        :type parameters: list[Parameter]
        :params checkpoint: the file containing the saved data
        :type checkpoint: str
        """

        try:
            self.first_opt.load_state_dict(checkpoint["first_optimizer_state_dict"])
            self.scheduler.load_state_dict(checkpoint["scheduler_state_dict"])

            if checkpoint["second_optimizer_state_dict"] is not None:
                self.create_second_opt(parameters)
                self.second_opt.load_state_dict(
                    checkpoint["second_optimizer_state_dict"]
                )
        except FileNotFoundError:
            print("optimizer was not loaded from file: training needed")

    def test_activation_second_opt(
        self,
        parameters: list[torch.nn.Parameter],
        loss_history: list,
        loss_value: torch.Tensor,
        init_loss: torch.Tensor,
        epoch: int = None,
    ):
        """
        Decide to activate or the not the second optimize and
        if yes create the second optimizer

        :params parameters: the parameters of the network
        :type parameters: list[Parameter]
        :params loss_history: the list of the loss value
        :type loss_history: list
        :params loss_value: the current value of the loss
        :type loss_value: torch.Tensor
        :params init_loss: the initial value of the loss
        :type init_loss: torch.Tensor
        :params epoch: the current epoch (optional)
        :type epoch: int
        """
        LBFGS_activated = self.second_opt_activated

        # auto-detect the epoch if no epoch is provided

        if epoch is None:
            epoch = len(loss_history)

        # detects whether a plateau has been reached

        n1, n2 = self.LBFGS_switch_plateau

        if self.switch_to_LBFGS and not LBFGS_activated and epoch > n1:
            if LBFGS_activated := (
                (loss_value < init_loss / self.LBFGS_switch_ratio)
                and (sum(loss_history[-n2:-1]) - sum(loss_history[-n1 : -n1 + n2]) > 0)
            ):
                self.create_second_opt(parameters)

        # detect whether a given number of iterations has been reached

        if (
            self.switch_to_LBFGS
            and not LBFGS_activated
            and epoch == self.switch_to_LBFGS_at
        ):
            self.create_second_opt(parameters)
            LBFGS_activated = self.second_opt_activated

    def update_best_opt(self):
        """
        Update the best optimizer value
        """
        self.best_first_optimizer = copy.deepcopy(self.first_opt.state_dict())
        self.best_scheduler = copy.deepcopy(self.scheduler.state_dict())

        if self.second_opt_activated:
            self.best_second_optimizer = copy.deepcopy(self.second_opt.state_dict())
        else:
            self.best_second_optimizer = None

    def dict_for_save(self) -> dict:
        """
        Save the network and optimizers to a file.

        :return: the dictionary of best optimizer values for save
        :rtype: dict
        """
        return {
            "first_optimizer_state_dict": self.best_first_optimizer,
            "scheduler_state_dict": self.best_scheduler,
            "second_optimizer_state_dict": self.best_second_optimizer,
        }

    def get_first_opt_gradients(self) -> torch.Tensor:
        """
        Get the gradients of the network parameters
        """
        grads = torch.tensor([])
        for p in self.first_opt.param_groups[0]["params"]:
            if p.grad is not None:
                grads = torch.cat((grads, p.grad.flatten()[:, None]), 0)
        return grads


class AbstractLoss(ABC):
    @abstractmethod
    def init_losses(self):
        pass

    @abstractmethod
    def compute_full_loss(self, optimizers: OptimizerData, epoch: int):
        pass

    @abstractmethod
    def update_histories(self):
        pass

    @abstractmethod
    def dict_for_save(self, best_loss: torch.Tensor) -> dict:
        pass

    @abstractmethod
    def load(self, checkpoint: str):
        pass

    @abstractmethod
    def plot(self, ax):
        pass


class SupervisedLossesData(AbstractLoss):
    DEFAULT_W_DATA = 1.0
    DEFAULT_W_GRAD_DATA = 1.0
    DEFAULT_W_CONSTRAINTS = 1.0
    """
        Class to create optimize and store the Losses for supervised training

        :param constrains_loss_bool: activate or not loww on weights constraints
        :type constraints_loss_bool: bool


        :param data_f_loss: the loss used to compute the data error (exemple MSE)
        :type data_loss_bool: torch.nn._Loss
        :param constraints_f_loss: the loss used to compute the constraints (exemple MSE)
        :type constraints_loss_bool: torch.nn._Loss

        :param w_data: weights for the data loss
        :type w_data: float
        :param w_constraints: weights for the constraints loss
        :type w_constraints: float

        :param adaptive_weights: whether to adapt the weights
        :type adaptive_weights: Union[str, None]
        :param epochs_adapt: epoch between two adaptation
        :type epochs_adapt: int
    """

    def __init__(self, **kwargs):
        self.data_loss_bool = True
        self.constraints_loss_bool = kwargs.get("constraints_loss_bool", False)
        self.data_grad_loss_bool = kwargs.get("data_grad_loss_bool ", False)
        self.data_f_loss = kwargs.get("data_f_loss", torch.nn.MSELoss())
        self.data_grad_f_loss = kwargs.get("data_grad_f_loss", torch.nn.MSELoss())
        self.constraints_f_loss = kwargs.get("constraints_f_loss", None)

        self.adaptive_weights = kwargs.get("adaptive_weights", None)
        self.epochs_adapt = kwargs.get("epochs_adapt", 20)
        self.w_data = kwargs.get("w_data", self.DEFAULT_W_DATA)
        self.w_constraints = kwargs.get(
            "w_constraints", self.DEFAULT_W_CONSTRAINTS * self.constraints_loss_bool
        )
        self.w_grad_data = kwargs.get(
            "w_grad_data", self.DEFAULT_W_GRAD_DATA * self.data_grad_loss_bool
        )

        self.alpha_lr_annealing = kwargs.get("alpha_lr_annealing", 0.9)
        self.epochs_adapt = kwargs.get("epochs_adapt", 10)
        if self.adaptive_weights is not None:
            self.w_data_history = [self.w_data]
            self.w_grad_data_history = [self.w_grad_data]
            self.w_constraints_history = [self.w_constraints]

        self.loss_history = []
        self.data_loss_history = []
        self.data_grad_loss_history = []
        self.constraints_loss_history = []
        self.loss_factor = 1.0

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
        self.data_loss_history = self.try_to_load(checkpoint, "data_loss_history")
        self.data_grad_loss_history = self.try_to_load(
            checkpoint, "data_grad_loss_history"
        )
        self.constraints_loss_history = self.try_to_load(
            checkpoint, "constraints_loss_history"
        )

    def init_losses(self):
        """
        initialize all the sublosses at zero
        """
        self.loss = torch.tensor(0.0)
        self.data_loss = torch.tensor(0.0)
        self.data_grad_loss = torch.tensor(0.0)
        self.constraints_loss = torch.tensor(0.0)

    def learning_rate_annealing(self, optimizers: OptimizerData):
        """
        Annealing of the learning rate
        """
        self.data_loss.backward(create_graph=False, retain_graph=True)
        grad_data = optimizers.get_first_opt_gradients()
        max_grad_data = torch.max(torch.abs(grad_data))
        self.w_data = 1.0

        if self.data_grad_loss_bool:
            self.data_grad_loss.backward(create_graph=False, retain_graph=True)
            grad_data_grad = optimizers.get_first_opt_gradients()
            mean_grad_data_grad = torch.mean(torch.abs(grad_data_grad))
            self.w_grad_data = (
                self.alpha_lr_annealing * max_grad_data / mean_grad_data_grad
                + (1 - self.alpha_lr_annealing) * self.w_grad_data
            )
            self.w_grad_data_history.append(self.w_grad_data)

        if self.constraints_loss_bool:
            self.constraints_loss.backward(create_graph=False, retain_graph=True)
            grad_constraints = optimizers.get_first_opt_gradients()
            mean_grad_constraints = torch.mean(torch.abs(grad_constraints))
            self.w_constraints = (
                self.alpha_lr_annealing * max_grad_data / mean_grad_constraints
                + (1 - self.alpha_lr_annealing) * self.w_constraints
            )
            self.w_constraints_history.append(self.w_constraints)

        self.alpha_lr_annealing *= 0.999

    def update_data_loss(self, value: torch.Tensor):
        """
        update the value fo the data loss

        :param value: the current value of the data loss
        :type value: torch.Tensor
        """
        self.data_loss = value

    def update_grad_data_loss(self, value: torch.Tensor):
        """
        update the value fo the constraints loss

        :param value: the current value of the constraints loss
        :type value: torch.Tensor
        """
        self.data_grad_loss = value

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
        if (self.adaptive_weights is not None) and (epoch % self.epochs_adapt):
            if self.adaptive_weights == "annealing":
                self.learning_rate_annealing(optimizers)
            else:
                raise ValueError(
                    f"adaptive_weights {self.adaptive_weights} not recognized"
                )

        self.loss = (
            self.w_data * self.data_loss
            + self.w_grad_data * self.data_grad_loss
            + self.w_constraints * self.constraints_loss
        )

    def update_histories(self):
        """
        Add all the current loss values in the histories
        """
        self.loss_history.append(self.loss.item() * self.loss_factor)
        self.data_loss_history.append(self.data_loss.item() * self.loss_factor)
        if self.constraints_loss_bool:
            self.constraints_loss_history.append(
                self.constraints_loss.item() * self.loss_factor
            )
        if self.data_grad_loss_bool:
            self.data_grad_loss_history.append(
                self.data_grad_loss.item() * self.loss_factor
            )

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
            "data_loss_history": self.data_loss_history,
        }
        if self.data_grad_loss_bool:
            dic["data_grad_loss_history"] = self.data_grad_loss_history
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
        ax.semilogy(self.data_loss_history, label="data")
        if self.data_grad_loss_bool:
            ax.semilogy(self.data_grad_loss_history, label="data_grad")
        if self.constraints_loss_bool:
            ax.semilogy(self.constraints_loss_history, label="contrains")
        ax.set_title("loss history")
        ax.legend()
        return ax
