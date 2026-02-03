import numpy as np
import matplotlib.pyplot as plt

from processes import GeometricBrownianMotion

S0 = 100
mu = 0.05
sigma = 0.2
T = 1.0

num_paths = 20
num_steps = 252

process = GeometricBrownianMotion(S0=S0, sigma=sigma, mu=mu)
paths = process.generate_paths(num_paths=num_paths, num_steps=num_steps, T=T)

# plot the paths
time_grid = np.linspace(0, T, num_steps + 1)

plt.figure(figsize=(10, 6))

for i in range(num_paths):
    plt.plot(time_grid, paths[i])

plt.xlabel("time")
plt.ylabel("price")
plt.title("GBM simulation of paths")
plt.grid(True)

plt.show()