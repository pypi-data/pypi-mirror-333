import numpy as np
from scipy.stats import norm

def fixed_sample_mde(alpha=0.05, beta=0.2, sigma_sq=1, N=1000, mu=1):
    """Compute the Minimum Detectable Effect (MDE) for a fixed-sample experiment."""
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(1 - beta)
    return ((z_alpha + z_beta) ** 2 * sigma_sq / N) / mu
