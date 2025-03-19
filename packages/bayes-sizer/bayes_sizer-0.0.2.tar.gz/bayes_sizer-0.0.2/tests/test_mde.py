import pytest
from bayessizer.mde import fixed_sample_mde

def test_fixed_sample_mde():
    """Test fixed sample MDE calculation."""
    mde = fixed_sample_mde()
    assert isinstance(mde, float)
    assert mde > 0
