# ScimBa

[![pipeline status](https://gitlab.inria.fr/scimba/scimba/badges/main/pipeline.svg)](https://gitlab.inria.fr/scimba/scimba/-/commits/main)
[![coverage report](https://gitlab.inria.fr/scimba/scimba/badges/main/coverage.svg)](https://sciml.gitlabpages.inria.fr/scimba/coverage)
[![Latest Release](https://gitlab.inria.fr/scimba/scimba/-/badges/release.svg)](https://gitlab.inria.fr/scimba/scimba/-/releases)
[![Doc](https://img.shields.io/badge/doc-sphinx-blue)](https://scimba.gitlabpages.inria.fr/scimba/)

Scimba is a Python that implements varying SciML methods for PDE problems as well as tools for hybrid numerical methods.
See [documentation](https://scimba.gitlabpages.inria.fr/scimba/) for details.

## Current Content

- **Nets**: MLP networks, Discontinuous MLP, RBF networks, some activations functions and a basic trainer
- **Sampling and domain**: general uniform sampling methods for PINNs and Neural Operators. Sampling based on approximated signed distance function for general geometries.
- **PDEs**: the librairiy implement différent type of model: ODE, spatial pde, times-apce pde, stationary kinetic PDE and kinetic PDE.
- **Specific networks for PINNs**: For all the equations we implement PINNs networks based on: MLP, Discontinuous MLP and nonlinear radial basis function.
We implement also the Fourier network with general features (Fourier but also Gaussian etc)
- **Trainer**: for each type of PDE we gives a specific trainer.
- **Generative Nets**: Normalized flows, Gaussian mixture. The classical and conditional approaches are proposed. Trainer based on the maximum likelihood principle.
- **Neural Operator**: Continuous Auto-encoder based on PointNet encoder and coordinate based decoder. Physic informed DeepOnet for ODE, spatial and time space PDE.
- **Neural Galerkin**: Method Neural Galerkin for time PDE based on the same network than PINNs.


## Ongoing work for 2024
- **Nets**: New activation function used for implicit representation, Symbolic models, Sindy
- **Sampling and domain**: learning of signed distance function using PINNs, adaptive sampling
- **Specific networks for PINNs**: Multiscale architecture, spectral architecture for kinetic, specific architecture.
- **Trainer**: Trainer with sparsity constraints and globalization method. Loss Balancing
- **Generative Nets**: Energy models, score matching, more complex normalized flow, Continuous VAE
- **Neural Operator**: physic informed DeepGreen operator, FNO, GINO based on FNO, NO with neural implicit representation. Kinetic case
- **Neural Galerkin**: Adaptive sampling, randomization, Least Square solver, implicit scheme. CROM Space time reduced Galerkin model. Greedy basis.


## References

### PINNs and MLP

- https://www.sciencedirect.com/science/article/abs/pii/S0021999118307125
- https://arxiv.org/abs/2209.03984
- https://arxiv.org/abs/1912.00873
- https://arxiv.org/abs/1912.00873
- https://arxiv.org/abs/2109.01050
- https://arxiv.org/abs/2203.01360
- https://arxiv.org/abs/2103.09959
- https://openreview.net/forum?id=vsMyHUq_C1c

### Neural Galerkin

- https://arxiv.org/abs/2306.15630
- https://arxiv.org/abs/2306.03749
- https://arxiv.org/abs/2207.13828
- https://arxiv.org/abs/2201.07953
- https://arxiv.org/abs/2104.13515

### DeepOnet

- https://www.nature.com/articles/s42256-021-00302-5
- https://www.science.org/doi/10.1126/sciadv.abi8605
- https://arxiv.org/abs/2205.11404
- https://arxiv.org/abs/2206.03551

### FNO and diverse geometry

- https://openreview.net/forum?id=c8P9NQVtmnO
- https://arxiv.org/abs/2207.05209
- https://arxiv.org/abs/2212.04689
- https://arxiv.org/abs/2305.00478
- https://arxiv.org/abs/2306.05697
- https://arxiv.org/abs/2305.19663

### Other NO

- https://openreview.net/forum?id=LZDiWaC9CGL
- https://arxiv.org/abs/2205.10573
- https://arxiv.org/abs/2205.02191
- https://openreview.net/forum?id=kIo_C6QmMOM
- https://arxiv.org/abs/2303.10528
- https://arxiv.org/abs/2302.05925
