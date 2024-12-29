# Raja Aita

Finnic for "border fence". Toolset to monitor and visualize computer usage.

## Hacking

Install and run test suite

    python -m venv .
    ./bin/pip install -c requirements.txt -e ".[test]"
    ./bin/pytest
    ./bin/flake8
    ./bin/mypy --strict src
