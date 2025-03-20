# pipli

[![PyPI version](https://img.shields.io/pypi/v/pipli.svg)](https://pypi.org/project/pipli/)

Auto install pip dependencies needed for a given command to run successfully.
Pipli keeps installing missing packages as long as it encounters `ModuleNotFoundError`
or `command not found` errors while running user given command. Pipli finally
runs the given command when all required packages have been installed.

## Usage

```bash
pipli  '<cmd>'
```

:warning: It's recommended to use a vitual environment to keep your package
installations contained and isolated.
```bash
python -m venv .myenv
```

## Installation

```bash
pip install pipli
```

## Examples

```bash
pipli 'python main.py'
```

```bash
pipli 'flask --app hello run'
```

```bash
pipli 'uvicorn main:app --host 0.0.0.0 --port 80'
```
