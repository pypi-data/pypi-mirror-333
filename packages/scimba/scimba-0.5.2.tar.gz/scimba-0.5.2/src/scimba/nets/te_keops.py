import time

import torch

import scimba.nets.rbfnet as rbfnet
import scimba.nets.training_tools as training_tools
import scimba.pinns.pinn_losses as pinn_losses
import scimba.pinns.pinn_x as pinn_x
import scimba.pinns.training_x as training_x
import scimba.sampling.sampling_parameters as sampling_parameters
import scimba.sampling.sampling_pde as sampling_pde
import scimba.sampling.uniform_sampling as uniform_sampling
from scimba.equations import domain, pdes

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"torch loaded; device is {device}")

torch.set_default_dtype(torch.double)
torch.set_default_device(device)

PI = 3.14159265358979323846
ELLIPSOID_A = 4 / 3
ELLIPSOID_B = 1 / ELLIPSOID_A


class PoissonDisk2D(pdes.AbstractPDEx):
    def __init__(self, space_domain):
        super().__init__(
            nb_unknowns=1,
            space_domain=space_domain,
            nb_parameters=1,
            parameter_domain=[[0.5, 1]],
        )

        self.first_derivative = True
        self.second_derivative = True

    def make_data(self, n_data):
        pass

    def bc_residual(self, w, x, mu, **kwargs):
        return self.get_variables(w)

    def residual(self, w, x, mu, **kwargs):
        x1, x2 = x.get_coordinates()
        u_xx = self.get_variables(w, "w_xx")
        u_yy = self.get_variables(w, "w_yy")
        f = self.get_parameters(mu)
        return u_xx + u_yy + f

    def reference_solution(self, x, mu):
        x1, x2 = x.get_coordinates()
        x1_0, x2_0 = self.space_domain.large_domain.center
        f = self.get_parameters(mu)
        return 0.25 * f * (1 - (x1 - x1_0) ** 2 - (x2 - x2_0) ** 2)


class Poisson_2D(pdes.AbstractPDEx):
    def __init__(self, space_domain):
        super().__init__(
            nb_unknowns=1,
            space_domain=space_domain,
            nb_parameters=1,
            parameter_domain=[[0.50000, 0.500001]],
        )

        self.first_derivative = True
        self.second_derivative = True

    def make_data(self, n_data):
        pass

    def bc_residual(self, w, x, mu, **kwargs):
        u = self.get_variables(w)
        return u

    def residual(self, w, x, mu, **kwargs):
        x1, x2 = x.get_coordinates()
        alpha = self.get_parameters(mu)
        u_xx = self.get_variables(w, "w_xx")
        u_yy = self.get_variables(w, "w_yy")
        f = 8 * PI**2 * alpha * torch.sin(2 * PI * x1) * torch.sin(2 * PI * x2)
        return u_xx + u_yy + f

    def post_processing(self, x, mu, w):
        x1, x2 = x.get_coordinates()
        return x1 * (1 - x1) * x2 * (1 - x2) * w

    def reference_solution(self, x, mu):
        x1, x2 = x.get_coordinates()
        alpha = self.get_parameters(mu)
        return alpha * torch.sin(2 * PI * x1) * torch.sin(2 * PI * x2)


CPU_forward = []
CPU_forward_keops = []
CPU_training = []
CPU_training_keops = []

all_nb_func = [10, 50, 500]

for nb_func in all_nb_func:
    xi = torch.tensor([[1.0, 1.0], [2.0, 2.0]])
    # print(xi)
    res1 = rbfnet.RBFLayer(in_size=2, out_size=1, points=xi)

    x = torch.tensor([[1.0, -1.0], [-1.2, 1.4], [5.0, 2 - 0.4]])

    # print(res1.forward(xi))

    res2 = rbfnet.RBFLayer_keops(in_size=2, out_size=1, points=xi)
    # print(res2.forward(xi))

    xdomain = domain.SpaceDomain(2, domain.SquareDomain(2, [[0.0, 1.0], [0.0, 1.0]]))
    pde = Poisson_2D(xdomain)
    x_sampler = sampling_pde.XSampler(pde=pde)
    mu_sampler = sampling_parameters.MuSampler(
        sampler=uniform_sampling.UniformSampling, model=pde
    )
    sampler = sampling_pde.PdeXCartesianSampler(x_sampler, mu_sampler)
    x, mu = sampler.sampling(20000)
    losses = pinn_losses.PinnLossesData()
    optimizers = training_tools.OptimizerData(learning_rate=1.2e-2, decay=0.99)

    start_forward = time.time()
    network = pinn_x.RBFNet_x(pde, sampler, nb_func=nb_func)
    pinn = pinn_x.PINNx(network, pde)
    pinn.get_w(x, mu)
    end_forward = time.time()
    start_training = time.time()
    trainer = training_x.TrainerPINNSpace(
        pde=pde,
        network=pinn,
        sampler=sampler,
        losses=losses,
        file_name=f"prout_{nb_func}",
        optimizers=optimizers,
        batch_size=10000,
    )
    trainer.train(epochs=20, n_collocation=10000, n_data=0)
    end_training = time.time()

    start_forward2 = time.time()
    network2 = pinn_x.RBFNet_x_keops(pde, sampler, nb_func=nb_func)
    pinn2 = pinn_x.PINNx(network2, pde)
    x, mu = sampler.sampling(20000)
    pinn2.get_w(x, mu)
    end_forward2 = time.time()
    start_training2 = time.time()
    trainer = training_x.TrainerPINNSpace(
        pde=pde,
        network=pinn2,
        sampler=sampler,
        losses=losses,
        file_name=f"pouet_{nb_func}",
        optimizers=optimizers,
        batch_size=10000,
    )
    trainer.train(epochs=20, n_collocation=10000, n_data=0)
    end_training2 = time.time()

    CPU_forward.append(end_forward - start_forward)
    CPU_forward_keops.append(end_forward2 - start_forward2)
    CPU_training.append(end_training - start_training)
    CPU_training_keops.append(end_training2 - start_training2)

for i, nb_func in enumerate(all_nb_func):
    print("\n")
    print(f"{nb_func} Gaussian functions")
    print(
        f"CPU time for forward: classical {CPU_forward[i]:3.2f}s, keops {CPU_forward_keops[i]:3.2f}s, ratio {CPU_forward[i] / CPU_forward_keops[i]:3.2f}"
    )
    print(
        f"CPU time for training: classical {CPU_training[i]:3.2f}s, keops {CPU_training_keops[i]:3.2f}s, ratio {CPU_training[i] / CPU_training_keops[i]:3.2f}"
    )
