import numpy as np

from ..api import StochasticProcess

class GeometricBrownianMotion(StochasticProcess):
    def generate_paths(self, num_paths: int, num_steps: int, T: float):
        """
        Generate stock price paths

        we use the Euler-Maruyama discretization of Geometric Brownian motion to model the stock:
            S_n+1 = S_n * exp((mu - 0.5 sigma²)dt + sigma * sqrt(dt)Z_n)
        
        Parameters:
        self: self
        num_paths (int): number of paths to generate
        num_steps (int): number of steps for all paths
        T (float): duration (for how long will we simulate)

        Returns:
        List(List(float)): a list containing all the paths as time series
        """
        dt = T / num_steps # partition the interval

        paths = []

        for path in range(num_paths):
            S = np.zeros(num_steps + 1)
            S[0] = self.S0

            for i in range(num_steps):
                Z = np.random.normal(0,1)
                S[i+1] = S[i] * np.exp((self.mu - 0.5 * (self.sigma ** 2)) * dt 
                    + self.sigma * np.sqrt(dt) * Z)
            paths.append(S)

        paths = np.array(paths)
        return paths
            