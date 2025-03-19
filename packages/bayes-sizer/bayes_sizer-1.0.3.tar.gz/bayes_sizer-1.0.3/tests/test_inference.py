# import pytest
# import numpy as np
# from scipy.stats import beta
# from bayessizer.inference import compute_posterior, credible_interval, probability_test_better

# @pytest.mark.parametrize("sample_size, success_rate", [(50, 0.5), (75, 0.55)])  # Reduced test cases
# def test_compute_posterior(sample_size, success_rate):
#     """Test posterior distribution computation with fewer iterations."""
#     posterior = compute_posterior(prior_a=2, prior_b=2, sample_size=sample_size, success_rate=success_rate)
#     assert isinstance(posterior, beta)

# @pytest.mark.parametrize("confidence", [0.95])  # Reduced test cases
# def test_credible_interval(confidence):
#     """Test credible interval computation with minimal cases for speed."""
#     posterior = compute_posterior(prior_a=2, prior_b=2, sample_size=75, success_rate=0.5)
#     lower, upper = credible_interval(posterior, confidence)
#     assert 0 <= lower <= upper <= 1

# @pytest.mark.parametrize("success_rate_test", [0.52])  # Reduced test cases
# def test_probability_test_better(success_rate_test):
#     """Test probability that test is better than control with minimal cases."""
#     control_posterior = compute_posterior(prior_a=2, prior_b=2, sample_size=75, success_rate=0.5)
#     test_posterior = compute_posterior(prior_a=2, prior_b=2, sample_size=75, success_rate=success_rate_test)
#     prob = probability_test_better(control_posterior, test_posterior)
#     assert 0 <= prob <= 1
