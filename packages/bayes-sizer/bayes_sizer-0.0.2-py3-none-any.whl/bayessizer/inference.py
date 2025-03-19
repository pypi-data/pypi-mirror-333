import numpy as np
from scipy.stats import beta

def compute_posterior(prior_a, prior_b, sample_size, success_rate):
    """
    Computes the posterior distribution for Bayesian inference.

    Parameters:
    - prior_a (float): Alpha parameter of Beta prior.
    - prior_b (float): Beta parameter of Beta prior.
    - sample_size (int): Number of observations.
    - success_rate (float): Observed conversion rate.

    Returns:
    - scipy.stats.beta: Beta distribution representing the posterior.
    """
    return beta(prior_a + sample_size * success_rate, prior_b + sample_size * (1 - success_rate))

def credible_interval(posterior, confidence=0.95):
    """
    Computes the Bayesian credible interval for a given posterior.

    Parameters:
    - posterior (scipy.stats.beta): Beta posterior distribution.
    - confidence (float): Desired confidence level (default 95%).

    Returns:
    - tuple: Lower and upper bounds of the credible interval.
    """
    lower_bound, upper_bound = posterior.ppf([(1 - confidence) / 2, (1 + confidence) / 2])
    return lower_bound, upper_bound

def probability_test_better(control_posterior, test_posterior):
    """
    Computes the probability that the test group is better than the control.

    Parameters:
    - control_posterior (scipy.stats.beta): Control group's posterior distribution.
    - test_posterior (scipy.stats.beta): Test group's posterior distribution.

    Returns:
    - float: Probability that the test group is better than the control.
    """
    return 1 - control_posterior.cdf(test_posterior.ppf(0.5))
