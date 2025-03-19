# BayesSizer

[![PyPI version](https://badge.fury.io/py/bayes-sizer.svg)](https://pypi.org/project/bayes-sizer/)
[![Build Status](https://github.com/allanbutler/bayes-sizer/actions/workflows/ci_cd.yml/badge.svg)](https://github.com/allanbutler/bayes-sizer)

BayesSizer is a Bayesian sample size calculator. It helps data scientists and experimenters determine the required sample size for A/B tests using Bayesian inference.

## Features
- Computes Bayesian-based sample sizes for A/B testing
- Supports configurable Type I (α) and Type II (β) error rates
- Designed for data science and experimentation teams
- Lightweight, simple, and efficient

## Installation

Install BayesSizer from PyPI:

```bash
pip install bayessizer
```

## Usage

```python
from bayessizer import bayesian_sample_size

# Example: Calculate required sample size with default parameters
sample_size = bayesian_sample_size(alpha=0.05, beta=0.2, effect_size=0.1, std_dev=1)
print(f"Required sample size per group: {sample_size}")
```

## Parameters
- `alpha` (float): Type I error rate (default: 0.05)
- `beta` (float): Type II error rate (default: 0.2)
- `effect_size` (float): Minimum detectable effect size (default: 0.1)
- `std_dev` (float): Standard deviation of the population (default: 1)

## Example Output
```bash
Required sample size per group: 385
```

## Running Tests
To ensure correctness, run:

```bash
pytest tests/
```

## Contributing
We welcome contributions! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.