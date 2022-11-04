ROOT=${WORKSPACE:-$(git rev-parse --show-toplevel)}
DIR_APP="$ROOT/setup"
DIR_VENV="$DIR_APP/venv"
PYTHON="/usr/bin/python3"


function setup_venv() {
    export PIP_CONFIG_FILE=$HOME/.config/pip/pip.conf
    echo "$PIP_CONFIG_FILE"

    "$PYTHON" -m venv "$DIR_VENV"
    source "$DIR_VENV/bin/activate"
  
    echo "=====checking active virtual environment..."
    echo "$VIRTUAL_ENV"

    pip install -r "$DIR_APP/requirements.txt"
}

setup_venv
