import asyncio
import threading
from typing import Any, Coroutine, Generic, Optional, TypeVar, Union

T = TypeVar("T")


class _Sentinel: ...


class _CoroutineThread(threading.Thread, Generic[T]):
    """_CoroutineThread is a thread designed for running coroutines.

    It is cancelable and will propagate the cancel to the underlying coroutine.
    The result is stored in the `result` attribute.
    """

    def __init__(self, coroutine: Coroutine[Any, Any, T]):
        threading.Thread.__init__(self)
        self._coroutine = coroutine
        self._asyncio_loop = None
        self.asyncio_loop: Optional[asyncio.AbstractEventLoop] = None
        self._result: Union[T, _Sentinel] = _Sentinel()
        self.exception: Optional[Exception] = None

    @property
    def result(self) -> T:
        # We use a Sentinel object instead of `None`, since `None` could be a valid
        # output to a coroutine. This allows us to differentiate between the scenario where
        # we didn't complete execution, from where there's a valid output.
        if isinstance(self._result, _Sentinel):
            raise ValueError("Result not set")
        return self._result

    def run(self):
        self._asyncio_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._asyncio_loop)
        try:
            self._result = self._asyncio_loop.run_until_complete(self._coroutine)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.exception = e
        finally:
            self._asyncio_loop.close()

    def cancel(self):
        if self._asyncio_loop is not None:
            self._asyncio_loop.call_soon_threadsafe(self._cancel_coroutine)

    def _cancel_coroutine(self):
        tasks = asyncio.all_tasks(loop=self._asyncio_loop)
        for task in tasks:
            task.cancel()


def _run_coroutine_as_thread(coroutine: Coroutine[Any, Any, T]) -> T:
    """Runs a coroutine in a separate thread and returns the result."""
    thread = _CoroutineThread(coroutine)
    thread.start()

    try:
        thread.join()
        if thread.exception is not None:
            raise thread.exception
        return thread.result
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Stopping the thread...")
        thread.cancel()
        thread.join()
        raise


def _is_running_loop() -> bool:
    """Utility that returns a boolean representing whether an an event loop is running"""
    try:
        return asyncio.get_running_loop() is not None
    except RuntimeError:
        return False


def run(coroutine: Coroutine[Any, Any, T]) -> T:
    """Runs a coroutine synchronously.

    If executing without an event loop (typical setting), it uses `asyncio.run`.
    If executing with an existing event loop (happens in Jupyter), it runs the coroutine in a separate thread.
    """
    if _is_running_loop():
        return _run_coroutine_as_thread(coroutine)
    else:
        return asyncio.run(coroutine)
