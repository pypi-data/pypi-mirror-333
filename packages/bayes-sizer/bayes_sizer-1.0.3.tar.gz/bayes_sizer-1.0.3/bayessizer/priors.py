from scipy.stats import beta, norm

def get_beta_prior(prior_a=1, prior_b=1):
    """
    Returns a Beta distribution prior.

    Parameters:
    - prior_a (float): Alpha parameter (default: 1).
    - prior_b (float): Beta parameter (default: 1).

    Returns:
    - scipy.stats.beta: Beta prior distribution.
    """
    return beta(prior_a, prior_b)

def get_normal_prior(mean=0, std=1):
    """
    Returns a Normal distribution prior.

    Parameters:
    - mean (float): Mean of the normal distribution (default: 0).
    - std (float): Standard deviation (default: 1).

    Returns:
    - scipy.stats.norm: Normal prior distribution.
    """
    return norm(mean, std)
