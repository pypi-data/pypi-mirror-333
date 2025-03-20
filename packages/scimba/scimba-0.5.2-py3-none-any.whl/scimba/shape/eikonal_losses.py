import torch

from ..nets.training_tools import OptimizerData


class EikonalLossesData:
    """
    Class to create optimize and store the Losses of PINNs for Eikonal equation.
    This class is used to learn approximated signed distance function

    :param reg_loss_bool: activate or not the loss to regularize the sdf
    :type reg_loss_bool: bool

    :param eikonal_f_loss: the loss used to compute the residue of the eikonal equation (exemple MSE)
    :type eikonal_loss_bool: torch.nn._Loss
    :param dirichlet_f_loss: the loss used to compute the dirichlet term (exemple MSE)
    :typec dirichlet_loss_bool: torch.nn._Loss
    :param neumann_f_loss: the loss usde to compute Neumann term (gradient of sdf is equal to the normal) (exemple MSE)
    :type neumann_loss_bool: torch.nn._Loss
    :param reg_f_loss: the loss used to compute the regularization (exemple MSE)
    :type reg_loss_bool: torch.nn._Loss

    :param w_eik: weights for the eikonal loss
    :type w_eik: float
    :param w_dir: weights for the dirichlet loss
    :type w_dir: float
    :param w_neu: weights for the neumann loss
    :type w_neu: float
    :param w_reg: weights for the regularization loss
    :type w_reg: float

    :param adaptive_weights: boolean to decide if we adapt the weights
    :type adaptive_weights: bool
    """

    def __init__(self, **kwargs):
        self.reg_loss_bool = kwargs.get("reg_loss_bool", False)

        self.eikonal_f_loss = kwargs.get("eik_f_loss", torch.nn.MSELoss())
        self.dirichlet_f_loss = kwargs.get("dirichlet_f_loss", torch.nn.MSELoss())
        self.neumann_f_loss = kwargs.get("neumann_f_loss", torch.nn.L1Loss())
        self.reg_f_loss = kwargs.get("reg_f_loss", torch.nn.MSELoss())

        self.w_eik = kwargs.get("w_eik", 1.0)
        self.adaptive_weights = kwargs.get("adaptive_weights", None)
        self.w_dir = kwargs.get("w_dir", 1.0)
        self.w_neu = kwargs.get("w_neu", 1.0)
        self.w_reg = kwargs.get("w_reg", 1.0)

        self.alpha_lr_annealing = kwargs.get("alpha_lr_annealing", 0.5)
        self.activate_reg_in_annealing = kwargs.get("activate_reg_in_annealing", True)
        if self.adaptive_weights is not None:
            self.w_eik_history = [self.w_eik]
            self.w_dir_history = [self.w_dir]
            self.w_neu_history = [self.w_neu]
            self.w_reg_history = [self.w_reg]

        self.loss_history = []
        self.eik_loss_history = []
        self.dir_loss_history = []
        self.neu_loss_history = []
        self.reg_loss_history = []

    def try_to_load(self, checkpoint, string):
        try:
            return checkpoint[string]
        except KeyError:
            return None

    def load(self, checkpoint):
        """
        Load the losses history of a file.

        :param file_name: name of the .pth file containing the losses history
        :type fine_name: str
        """
        self.loss = self.try_to_load(checkpoint, "loss")
        self.loss_history = self.try_to_load(checkpoint, "loss_history")
        self.eik_loss_history = self.try_to_load(checkpoint, "eik_loss_history")
        self.dir_loss_history = self.try_to_load(checkpoint, "dir_loss_history")
        self.neu_loss_history = self.try_to_load(checkpoint, "neu_loss_history")
        self.reg_loss_history = self.try_to_load(checkpoint, "reg_loss_history")

    def init_losses(self):
        """
        initialize all the sublosses at zero
        """
        self.loss = torch.tensor(0.0)
        self.eikonal_loss = torch.tensor(0.0)
        self.dirichlet_loss = torch.tensor(0.0)
        self.neumann_loss = torch.tensor(0.0)
        self.reg_loss = torch.tensor(0.0)

    def learning_rate_annealing(self, optimizers: OptimizerData):
        """
        Annealing of the learning rate
        """
        self.eikonal_loss.backward(create_graph=False, retain_graph=True)
        grad_eikonal = optimizers.get_first_opt_gradients()
        max_grad_eikonal = torch.max(torch.abs(grad_eikonal))
        self.w_eik = 1.0

        self.dirichlet_loss.backward(create_graph=False, retain_graph=True)
        grad_dirichlet = optimizers.get_first_opt_gradients()
        mean_grad_dirichlet = torch.mean(torch.abs(grad_dirichlet))
        self.w_dir = (
            self.alpha_lr_annealing * max_grad_eikonal / mean_grad_dirichlet
            + (1 - self.alpha_lr_annealing) * self.w_dir
        )
        self.w_dir_history.append(self.w_dir)

        self.neumann_loss.backward(create_graph=False, retain_graph=True)
        grad_neumann = optimizers.get_first_opt_gradients()
        mean_grad_neumann = torch.mean(torch.abs(grad_neumann))
        self.w_neu = (
            self.alpha_lr_annealing * max_grad_eikonal / mean_grad_neumann
            + (1 - self.alpha_lr_annealing) * self.w_neu
        )
        self.w_neu_history.append(self.w_neu)

        if self.reg_loss_bool and self.activate_reg_in_annealing:
            self.reg_loss.backward(create_graph=False, retain_graph=True)
            grad_reg = optimizers.get_first_opt_gradients()
            mean_grad_reg = torch.mean(torch.abs(grad_reg))
            self.w_reg = (
                self.alpha_lr_annealing * max_grad_eikonal / mean_grad_reg
                + (1 - self.alpha_lr_annealing) * self.w_reg
            )
            self.w_reg_history.append(self.w_reg)

        self.alpha_lr_annealing *= 0.999

    def update_eikonal_loss(self, value: torch.Tensor):
        """
        update the value fo the residual loss

        :param value: the current value of the residual loss
        :type value: torch.Tensor
        """
        self.eikonal_loss = value

    def update_dirichlet_loss(self, value: torch.Tensor):
        """
        update the value fo the data loss

        :param value: the current value of the data loss
        :type value: torch.Tensor
        """
        self.dirichlet_loss = value

    def update_neumann_loss(self, value: torch.Tensor):
        """
        update the value fo the init loss

        :param value: the current value of the init loss
        :type value: torch.Tensor
        """
        self.neumann_loss = value

    def update_reg_loss(self, value: torch.Tensor):
        """
        update the value fo the bc loss

        :param value: the current value of the bc loss
        :type value: torch.Tensor
        """
        self.reg_loss = value

    def compute_full_loss(self, optimizers: OptimizerData, epoch:int):
        """
        compute the full loss as the combination of all the losses
        """
        if self.adaptive_weights is not None:
            if self.adaptive_weights == "annealing":
                self.learning_rate_annealing(optimizers)
            else:
                raise ValueError(
                    f"adaptive_weights {self.adaptive_weights} not recognized"
                )

        self.loss = (
            self.w_eik * self.eikonal_loss
            + self.w_dir * self.dirichlet_loss
            + self.w_neu * self.neumann_loss
            + self.w_reg * self.reg_loss
        )

    def update_histories(self):
        """
        Add all the current loss values in the histories
        """
        self.loss_history.append(self.loss.item())
        self.eik_loss_history.append(self.eikonal_loss.item())
        self.neu_loss_history.append(self.neumann_loss.item())
        self.dir_loss_history.append(self.dirichlet_loss.item())
        if self.reg_loss_bool:
            self.reg_loss_history.append(self.reg_loss.item())

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
            "eik_loss_history": self.eik_loss_history,
            "neu_loss_history": self.neu_loss_history,
            "dir_loss_history": self.dir_loss_history,
        }
        if self.reg_loss_bool:
            dic["reg_loss_history"] = self.reg_loss_history
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
        ax.semilogy(self.eik_loss_history, label="eikonal")
        ax.semilogy(self.dir_loss_history, label="dirichlet")
        ax.semilogy(self.neu_loss_history, label="neumann")
        if self.reg_loss_bool:
            ax.semilogy(self.reg_loss_history, label="reg")
        ax.set_title("loss history")
        ax.legend()
        return ax
