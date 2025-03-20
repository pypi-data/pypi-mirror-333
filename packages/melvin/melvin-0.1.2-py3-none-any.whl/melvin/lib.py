import argparse
from contextlib import contextmanager
from typing import Any

from agents import build_agent

@contextmanager
def init_copilot(llm: Any):
    from melvin.tecton_gen_ai.api import Configs
    from melvin.tecton_gen_ai.testing import set_dev_mode

    set_dev_mode()
    with Configs(llm=llm, agent_invoke_kwargs={"max_iterations": 30}).update_default():
        yield build_agent()


def parse_args():
    parser = argparse.ArgumentParser(description="Q&A or chat with tecton docs.")
    # add a model parameter with short form -m to specify model
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="openai/gpt-4o-2024-11-20",
        # default="openai/o3-mini-2025-01-31",
        help="LLM to use",
    )
    # add a temperature parameter with short form -t to specify temperature
    parser.add_argument(
        "--temperature",
        "-t",
        type=float,
        default=0.0,
        help="temperature for sampling",
    )
    # add a max_length parameter with short form -l to specify max_length
    parser.add_argument(
        "--max_tokens",
        "-l",
        type=int,
        default=4096,
        help="maximum token length of the output",
    )

    # parse the input
    args = parser.parse_args()

    llm = {
        "model": args.model,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }
    res = vars(args)
    res["llm"] = llm
    return res
