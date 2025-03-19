import numpy as np
from bayessizer.inference import compute_posterior, probability_test_better, credible_interval
from bayessizer.priors import get_beta_prior

def bayesian_sample_size(prior_a=1, prior_b=1, min_effect=0.02, power=0.8, loss_threshold=0.01):
    """
    Computes Bayesian sample size for A/B testing using a Beta prior.

    Parameters:
    - prior_a (float): Alpha parameter for Beta prior.
    - prior_b (float): Beta parameter for Beta prior.
    - min_effect (float): Minimum detectable effect.
    - power (float): Desired probability of detecting the effect.
    - loss_threshold (float): Maximum tolerated decision loss.

    Returns:
    - int: Required sample size per group.
    """
    sample_size = 10  # Start small
    step_size = 10     # Increment size

    while True:
        # Compute posterior distributions
        control_posterior = compute_posterior(prior_a, prior_b, sample_size, 0.5)
        test_posterior = compute_posterior(prior_a, prior_b, sample_size, 0.5 + min_effect)

        # Compute probability that the test is better than control
        prob_test_better = probability_test_better(control_posterior, test_posterior)

        # Compute 95% credible intervals
        control_ci = credible_interval(control_posterior)
        test_ci = credible_interval(test_posterior)

        if prob_test_better >= power:
            return sample_size
        
        sample_size += step_size
