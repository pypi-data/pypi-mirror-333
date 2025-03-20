import datetime
import json
import os

from constants import FILE_DIR
from utils import get_cwd, is_in_feature_repo, get_tecton_account_info

import logfire

# configure logfire
LOGFIRE_API_KEY = os.getenv("LOGFIRE_API_KEY")
if LOGFIRE_API_KEY:
    logfire.configure(token=LOGFIRE_API_KEY)
    logfire.instrument_openai()
    print("Tracing to https://logfire.pydantic.dev/")
else:
    print("LOGFIRE_API_KEY is not set, so logfire will not be used")

def sys_prompt() -> str:
    context = {
        "Current directory": get_cwd(),
        "In feature repo": is_in_feature_repo(),
        "Current Tecton account info": get_tecton_account_info(),
        "Current time": datetime.datetime.now().isoformat(),
    }
    with open(os.path.join(FILE_DIR, "data", "gotchas.md"), "r") as f:
        gotchas = f.read()
    with open(os.path.join(FILE_DIR, "data", "sys_prompt.md"), "r") as f:
        return f.read().format(context=json.dumps(context, indent=4), gotchas=gotchas)
