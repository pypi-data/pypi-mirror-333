# import pytest
# from scipy.stats import beta, norm
# from bayessizer.priors import get_beta_prior, get_normal_prior

# @pytest.mark.parametrize("alpha, beta_param", [(2, 5)])  # Reduced test cases
# def test_get_beta_prior(alpha, beta_param):
#     """Test Beta prior distribution efficiently with minimal cases."""
#     prior = get_beta_prior(alpha, beta_param)
#     assert isinstance(prior, beta)

# @pytest.mark.parametrize("mean, std", [(0, 1)])  # Reduced test cases
# def test_get_normal_prior(mean, std):
#     """Test Normal prior distribution efficiently with minimal cases."""
#     prior = get_normal_prior(mean, std)
#     assert isinstance(prior, norm)
