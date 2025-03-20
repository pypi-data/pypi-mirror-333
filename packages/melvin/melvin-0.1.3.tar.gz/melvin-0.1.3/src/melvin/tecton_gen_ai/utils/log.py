import logging
import io
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator


class CostMonitor:
    def __init__(self):
        self.total_cost = 0.0
        self.total_requests = 0.0

    def report(self, cost: float, requests: float):
        self.total_cost += cost
        self.total_requests += requests


_COST_MONITOR = ContextVar("_COST_MONITOR", default=None)


@contextmanager
def cost_monitor() -> Iterator[CostMonitor]:
    try:
        monitor = CostMonitor()
        token_cost = _COST_MONITOR.set(monitor)
        yield monitor
    finally:
        _COST_MONITOR.reset(token_cost)


def get_cost_monitor() -> CostMonitor:
    res = _COST_MONITOR.get()
    if res is None:
        raise RuntimeError("Cost monitor is not set")
    return res


def report_cost(cost: float, requests: float) -> None:
    res = _COST_MONITOR.get()
    if res is not None:
        get_cost_monitor().report(cost, requests)


def make_noop_logger() -> logging.Logger:
    null_logger = logging.getLogger("NOOP")
    null_logger.handlers.clear()
    null_logger.addHandler(logging.NullHandler())  # read below for reason
    null_logger.propagate = False
    return null_logger


def make_string_logger(name: str, sio: io.StringIO) -> logging.Logger:
    string_logger = logging.getLogger(name)
    string_logger.handlers.clear()
    string_logger.addHandler(logging.StreamHandler(sio))
    string_logger.propagate = False
    return string_logger


NOOP_LOGGER = make_noop_logger()
