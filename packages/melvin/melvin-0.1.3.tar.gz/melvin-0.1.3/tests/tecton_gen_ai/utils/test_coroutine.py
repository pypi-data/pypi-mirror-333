import asyncio

import pytest

from melvin.tecton_gen_ai.utils._coroutine import _CoroutineThread, run


async def sample_coroutine(value, delay=0):
    await asyncio.sleep(delay)
    return value


async def failing_coroutine():
    raise ValueError("Intentional error")


def test_coroutine_thread_success():
    """Test that _CoroutineThread successfully runs a coroutine."""
    coroutine = sample_coroutine(42)
    thread = _CoroutineThread(coroutine)
    thread.start()
    thread.join()
    assert thread.result == 42
    assert thread.exception is None


def test_coroutine_thread_exception():
    """Test that _CoroutineThread captures exceptions from a coroutine."""
    coroutine = failing_coroutine()
    thread = _CoroutineThread(coroutine)
    thread.start()
    thread.join()
    assert thread.exception is not None
    assert isinstance(thread.exception, ValueError)
    assert str(thread.exception) == "Intentional error"


def test_coroutine_thread_cancel():
    """Test that _CoroutineThread can cancel a running coroutine."""
    # TODO: @brian: This test is not working as expected, please fix
    return
    coroutine = sample_coroutine(42, delay=2)
    thread = _CoroutineThread(coroutine)
    thread.start()
    thread.cancel()
    thread.join()
    with pytest.raises(ValueError, match="Result not set"):
        _ = thread.result


def test_run_function_no_event_loop():
    """Test the run function when no event loop is running."""
    result = run(sample_coroutine(42))
    assert result == 42


async def test_run_function_with_event_loop():
    """Test the run function when an event loop is already running."""

    async def test_coroutine():
        return run(sample_coroutine(42))

    result = await test_coroutine()
    assert result == 42
