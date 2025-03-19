Cave Utilities for the Cave App
==========
Basic utilities for the MIT Cave App. This package is intended to be used by the Cave App and the Cave API.

Setup
----------

Make sure you have Python 3.9.x (or higher) installed on your system. You can download it [here](https://www.python.org/downloads/).

### Installation

```
pip install cave_utils
```


# Running Validator Tests

## Example:
1. In your cave_app, update the following file:

    `cave_api/tests/test_init.py`
    ```
    from cave_api import execute_command
    from cave_utils.socket import Socket
    from cave_utils.validator import Validator


    init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

    x = Validator(init_session_data)

    x.log.print_logs()
    # x.log.print_logs(level="error")
    # x.log.print_logs(level="warning")
    # x.log.print_logs(max_count=10)
    ```

2. Run the following command:
    `cave test test_init.py`


# cave_utils development

## Using Local Hotloading

1. In your `cave_app`, update the following file:

    `utils/run_server.sh`
    ```
    #!/bin/bash

    SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
    APP_DIR=$(dirname "$SCRIPT_DIR")

    pip install -e /cave_utils

    source ./utils/helpers/shell_functions.sh
    source ./utils/helpers/ensure_postgres_running.sh
    source ./utils/helpers/ensure_db_setup.sh

    python "$APP_DIR/manage.py" runserver 0.0.0.0:8000 2>&1 | pipe_log "INFO"
    ```

2. Remove `cave_utils` from the root `requirements.txt` file

3. In your `cave_app`, set `LIVE_API_VALIDATION_PRINT=True` in the `.env` file
    - This will validate your data every time an API command is called for each session

4. Use the following command to run your `cave_app`:
    `cave run --docker-args "--volume {local_path_to_cave_utils}/cave_utils:/cave_utils"`
    - As you edit `cave_utils`, any changes will be hotloaded into your running `cave_app`

## Using interactive mode and running tests

1. Run cave_app in interactive mode mounting cave_utils as a volume:
    `cave run --docker-args "--volume {local_path_to_cave_utils}/cave_utils:/cave_utils" -it`
2. Then install cave utils in the docker container:
    `pip install -e /cave_utils`
3. Then run some tests (eg `validate_all_examples.py`):
    `python cave_api/tests/validate_all_examples.py`

# Generate Documentation

1. Set up your virtual environment
    - `python3 -m virtualenv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
2. Update the docs
    - `source venv/bin/activate`
    - `./update_documentation.sh`

# Generate a New Release

1. Set up your virtual environment
    - `python3 -m virtualenv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
2. Update the version number in:
    - `setup.cfg`
    - `pyproject.toml`
3. Update the release
    - `source venv/bin/activate`
    - `./update_version.sh`
