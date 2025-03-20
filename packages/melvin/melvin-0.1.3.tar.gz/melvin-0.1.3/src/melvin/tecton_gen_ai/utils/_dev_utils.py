from ..constants import TECTON_DEV_MODE_KEY
import os


def set_dev_flag():
    os.environ[TECTON_DEV_MODE_KEY] = "true"


def is_dev_mode():
    return os.environ.get(TECTON_DEV_MODE_KEY, "false") == "true"
