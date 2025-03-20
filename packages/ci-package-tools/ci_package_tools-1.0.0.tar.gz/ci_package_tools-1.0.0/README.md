# CI Package Tools
[![PyPI version](https://badge.fury.io/py/hermes-storage-nodes.svg)](https://pypi.org/project/ci-package-tools)

A tool to manage the packaging process in CI/CD pipelines.

## Installation

### From PyPI

Install the package directly from PyPI using pip:

```bash
pip install ci-package-tools
```

### From Source

Clone the repository and install dependencies:

```bash
git clone https://github.com/node-hermes/ci-package-tools
pip install -e hermes-storage-nodes
```

## Development

This project depends on UV for managing dependencies.
Make sure you have UV installed and set up in your environment.

You can find more information about UV [here](https://docs.astral.sh/uv/getting-started/installation/).

```bash
uv venv
```

```bash
uv sync --all-extras --dev
```
