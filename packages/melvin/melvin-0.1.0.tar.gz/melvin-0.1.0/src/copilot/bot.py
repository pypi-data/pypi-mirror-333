from typing import Any

from lib import init_copilot, parse_args
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from utils import initialize_tecton_account_info_if_needed

# We need to do this hack because set_dev_mode below actually overrides some env vars that get_current_tecton_account_info depends on
initialize_tecton_account_info_if_needed()



def text_chat(llm: Any) -> None:
    history = []
    console = Console()

    with init_copilot(llm) as copilot:
        while True:
            console.rule("[bold][green]Your Question[/green][/bold]", align="left")
            console.print("")
            question = Prompt.ask().strip()
            if not question:
                break
            res = copilot.invoke(question, chat_history=history)
            md = Markdown(res)
            history.append(("user", question))
            history.append(("assistant", res))
            console.print("")
            console.rule("[bold][blue]AI Response[/blue][/bold]", align="left")
            console.print("")
            console.print(md)
            console.print("")


if __name__ == "__main__":
    args = parse_args()
    text_chat(args["llm"])
