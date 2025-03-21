# 📦 Latest PyPI Version

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-blue)](https://github.com/astral-sh/ruff)
[![MyPy](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A simple CLI tool to check the latest version of any package on PyPI.

## 🌟 Features

- Fetch the latest version of any PyPI package directly from your terminal
- Display detailed package information with verbose mode
- Fast and lightweight with minimal dependencies

## 🚀 Installation

### Using pip

```bash
pip install latest-pypi-version
```

### From Source

Clone the repository and install using [Poetry](https://python-poetry.org/) and [Taskfile](https://taskfile.dev/):

```bash
git clone https://github.com/yourusername/latest-pypi-version.git
cd latest-pypi-version
task install  # This will set up a virtual environment and install dependencies
```

## 🔧 Usage

### Basic Usage

Check the latest version of any package:

```bash
latest-pypi-version requests
```

Example output:
```
requests latest version: 2.32.3
```

### Verbose Mode

Get more detailed package information:

```bash
latest-pypi-version requests --verbose
```

Example output:

```
Package: requests
Latest version: 2.31.0
Author: Kenneth Reitz
Homepage: https://requests.readthedocs.io
Summary: Python HTTP for Humans.
Upload date: 2023-05-22
```

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

### Setting Up Development Environment
```bash
# Clone the repository
git clone https://github.com/yourusername/latest-pypi-version.git
cd latest-pypi-version

# Install development dependencies
task install
```

### Development Tasks
The project includes a Taskfile with useful commands:

* `task install` - Set up the development environment
* `task run` - Run the CLI tool
* `task cq` - Run code quality checks (formatting, linting, and type checking)
* `task clean` - Clean up temporary files and build artifacts

### 📝 TODOs
* [ ] Add CI/CD pipeline
* [ ] Add tests
* [ ] Add support for specifying a specific index URL