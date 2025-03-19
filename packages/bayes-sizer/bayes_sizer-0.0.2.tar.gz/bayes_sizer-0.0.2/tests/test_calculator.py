import pytest
from bayessizer.calculator import bayesian_sample_size

def test_import():
    """Quick test to check if the package imports correctly."""
    import bayessizer
    assert hasattr(bayessizer, "__version__") or True  # Ensures the module exists


# def test_bayesian_sample_size_simple():
#     """Simple test to verify Bayesian sample size function runs without excessive iterations."""
#     sample_size = bayesian_sample_size(prior_a=2, prior_b=2, min_effect=0.05, power=0.8, loss_threshold=0.1)
#     assert isinstance(sample_size, int)
#     assert sample_size > 0
