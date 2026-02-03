import numpy as np

from ..api import Simulation

class MonteCarloSimulation(Simulation):
    def run(self, num_paths, num_steps):
        paths = self.process.generate_paths(
            num_paths=num_paths,
            num_steps=num_steps,
            T=self.option.T
        )

        payoffs = np.array(
            [self.option.payoff(path) for path in paths]
        )

        expected_payoff = payoffs.mean()

        price = np.exp(-self.r * self.option.T) * expected_payoff
        return price