# tulpa

[![PyPI version](https://badge.fury.io/py/tulpa.svg)](https://badge.fury.io/py/tulpa)
[![Test](https://github.com/phillipdupuis/tulpa/actions/workflows/test.yml/badge.svg)](https://github.com/phillipdupuis/tulpa/actions/workflows/test.yml)
[![Lint](https://github.com/phillipdupuis/tulpa/actions/workflows/lint.yml/badge.svg)](https://github.com/phillipdupuis/tulpa/actions/workflows/lint.yml)
[![Coverage Status](https://codecov.io/github/phillipdupuis/tulpa/branch/main/graph/badge.svg)](https://codecov.io/github/phillipdupuis/tulpa)

Tools enabling generative AI to interact with the physical world

## Installation

```bash
pip install tulpa
```

With [uv](https://github.com/astral-sh/uv):

```bash
uv pip install tulpa
```

## Usage

```python
import tulpa

# Add usage examples here
```

## Development

This project uses modern Python tooling:

- [uv](https://github.com/astral-sh/uv) for dependency management
- [pytest](https://docs.pytest.org/) for testing
- [ruff](https://github.com/astral-sh/ruff) for linting and formatting

### Setup

```bash
# Clone the repository
git clone https://github.com/phillipdupuis/tulpa.git
cd tulpa

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
ruff check .
ruff format .
```

## License

[GNU General Public License v3.0](LICENSE)
