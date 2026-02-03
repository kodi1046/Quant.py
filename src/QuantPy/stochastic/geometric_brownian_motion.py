from api import StochasticProcess
import numpy as np

class GeometricBrownianMotion(StochasticProcess):
    def __init__():
        super().__init__()
    
    def generate_paths(num_paths: int, num_steps: int, T: float):
        dt = T / num_steps
        paths = np.zeros((num_paths, num_steps + 1))
        paths[:, 0] = self.S0

        Z = np.random.normal(size=(num_paths, num_steps))
        drift = (self.mu - 0.5 * self.sigma**2) * dt
        diffusion = self.sigma * np.sqrt(dt)

        for i in range(1, num_steps + 1):
            paths[:, t] = paths[:, t-1] * np.exp(drift + diffusion * Z[:, t-1])

        return paths