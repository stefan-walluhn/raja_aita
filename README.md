# Raja Aita

Finnic for "border fence". Toolset to monitor and visualize computer usage.

## Install server

Create virtualenv and install server

    python3 -m venv .
    ./bin/pip install -c requirements.txt -e .

Run server

    ./bin/uvicorn --workers=1 raja_aita.api:api

### Configure server

Server settings are configured using env vars. Make use of uvicorn's
`--env-file` flag for file based configuration.

| Config         | Format    | Default                                  |
|----------------|-----------|------------------------------------------|
| RA_TINYDB_PATH | file path | unset, in memory storage (not persisted) |

## Install client

Install dependencies and headers

    sudo apt install cmake libcairo-dev libdbus-1-dev libgirepository1.0-dev libglib2.0-dev libpython3-dev

Create virtualenv and install client

    python3 -m venv .
    ./bin/pip install -c requirements.txt -e ".[client]"

Create UID

    ./bin/python3 -c "from uuid import uuid4; print(uuid4())"

Run client

    ./bin/raja-client --api-url="$RAJA_AITA_SERVER_URL" $UID

### Autostart client on login

See https://wiki.ubuntuusers.de/Autostart/#Startprogramme-unter-Unity-GNOME-3


## Hacking

Install and run test suite

    python -m venv .
    ./bin/pip install -c requirements.txt -e ".[test]"
    ./bin/pytest
    ./bin/flake8
    ./bin/mypy src
