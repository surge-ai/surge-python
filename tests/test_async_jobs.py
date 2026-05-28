from unittest.mock import patch

import pytest

from surge.async_jobs import AsyncJobError, poll_async_job


def test_returns_on_first_completed_status():
    statuses = iter([{"status": "COMPLETED", "url": "u"}])
    result = poll_async_job(lambda: next(statuses),
                            poll_time=10,
                            poll_interval=0)
    assert result == {"status": "COMPLETED", "url": "u"}


def test_polls_through_in_progress_then_returns_completed():
    statuses = iter([
        {
            "status": "IN_PROGRESS"
        },
        {
            "status": "IN_PROGRESS"
        },
        {
            "status": "COMPLETED",
            "url": "u"
        },
    ])
    with patch("time.sleep"):
        result = poll_async_job(lambda: next(statuses),
                                poll_time=10,
                                poll_interval=0)
    assert result == {"status": "COMPLETED", "url": "u"}


def test_accepts_creating_and_ready_status_vocabulary():
    statuses = iter([
        {
            "status": "CREATING"
        },
        {
            "status": "READY",
            "url": "u"
        },
    ])
    with patch("time.sleep"):
        result = poll_async_job(lambda: next(statuses),
                                poll_time=10,
                                poll_interval=0)
    assert result == {"status": "READY", "url": "u"}


def test_raises_async_job_error_on_error_status():
    with pytest.raises(AsyncJobError, match="kaboom"):
        poll_async_job(
            lambda: {
                "status": "ERROR",
                "error": "kaboom"
            },
            poll_time=10,
            poll_interval=0,
        )


def test_raises_async_job_error_on_unknown_status():
    with pytest.raises(AsyncJobError, match="weird"):
        poll_async_job(lambda: {"status": "weird"},
                       poll_time=10,
                       poll_interval=0)


def test_raises_timeout_when_poll_time_elapses():
    with patch("time.sleep"):
        with pytest.raises(AsyncJobError) as excinfo:
            poll_async_job(
                lambda: {"status": "IN_PROGRESS"},
                poll_time=0,
                poll_interval=0,
            )
    assert excinfo.value.status.get("status") == "TIMEOUT"


def test_caps_sleep_to_remaining_poll_time():
    """Sleep should never exceed the remaining budget — even with a
    poll_interval much larger than poll_time."""

    statuses = iter([
        {
            "status": "IN_PROGRESS"
        },
        {
            "status": "COMPLETED",
            "url": "u"
        },
    ])

    with patch("time.sleep") as mock_sleep:
        poll_async_job(
            lambda: next(statuses),
            poll_time=5,
            poll_interval=60,
        )

    assert mock_sleep.call_count == 1
    (slept_seconds, ) = mock_sleep.call_args.args
    assert slept_seconds <= 5


def test_raises_timeout_instead_of_returning_completed_after_deadline():
    """When poll_interval > poll_time the loop sleeps past the deadline.
    The second status must not be honored — even if it would be COMPLETED."""

    statuses = iter([
        {
            "status": "IN_PROGRESS"
        },
        {
            "status": "COMPLETED",
            "url": "u"
        },
    ])

    # Simulate the deadline elapsing immediately after the first poll:
    # call 1 sets the deadline, calls 2+ all report well past it.
    with patch("time.sleep"), patch("time.monotonic",
                                    side_effect=[0.0, 1e9, 1e9, 1e9]):
        with pytest.raises(AsyncJobError) as excinfo:
            poll_async_job(
                lambda: next(statuses),
                poll_time=1,
                poll_interval=2,
            )
    assert excinfo.value.status.get("status") == "TIMEOUT"
