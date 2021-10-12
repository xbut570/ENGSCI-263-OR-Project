import matplotlib.pyplot as plt
import numpy as np

# estimated inputs for lognorm distribution
mu = 0.03 
sigma = 0.07
np.random.seed(100)      # seed for random distribution

# log normal distribution for travel times
random = np.random.lognormal(mu, sigma, 1000) 

# plot a histogram to view the random numbers
plt.hist(random, 100, density=True, align='mid')
plt.show()