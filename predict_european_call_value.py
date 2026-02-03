import numpy as np
import matplotlib.pyplot as plt

from src.QuantPy.simulation.monte_carlo import MonteCarloSimulation
from src.QuantPy.options.european import EuropeanCallOption
from src.QuantPy.stochastic.geometric_brownian_motion import GeometricBrownianMotion

def main():

    S0 = 100
    K = 80
    T = 1.0
    r = 0.05 # assumption
    sigma = 0.25 # medium volatility
    mu = 0.05

    num_paths = 20
    num_steps = 252

    european_call = EuropeanCallOption(S0, K, T, r, sigma)

    GBM = GeometricBrownianMotion(S0, sigma, mu)

    monte_carlo = MonteCarloSimulation(european_call, GBM, r)
    result = monte_carlo.run(num_paths, num_steps)

    print(result)

if __name__ == "__main__":
    main()