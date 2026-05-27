from unittest.mock import patch

import pytest

from surge.async_jobs import (
    AsyncJobError,
    AsyncJobTimeoutError,
    poll_async_job,
)


def test_returns_on_first_completed_status():
    statuses = iter([{"status": "COMPLETED", "url": "u"}])
    result = poll_async_job(lambda: next(statuses), poll_time=10, poll_interval=0)
    assert result == {"status": "COMPLETED", "url": "u"}


def test_polls_through_in_progress_then_returns_completed():
    statuses = iter(
        [
            {"status": "IN_PROGRESS"},
            {"status": "IN_PROGRESS"},
            {"status": "COMPLETED", "url": "u"},
        ]
    )
    with patch("time.sleep"):
        result = poll_async_job(lambda: next(statuses), poll_time=10, poll_interval=0)
    assert result == {"status": "COMPLETED", "url": "u"}


def test_accepts_creating_and_ready_status_vocabulary():
    statuses = iter(
        [
            {"status": "CREATING"},
            {"status": "READY", "url": "u"},
        ]
    )
    with patch("time.sleep"):
        result = poll_async_job(lambda: next(statuses), poll_time=10, poll_interval=0)
    assert result == {"status": "READY", "url": "u"}


def test_raises_async_job_error_on_error_status():
    with pytest.raises(AsyncJobError, match="kaboom"):
        poll_async_job(
            lambda: {"status": "ERROR", "error": "kaboom"},
            poll_time=10,
            poll_interval=0,
        )


def test_raises_async_job_error_on_unknown_status():
    with pytest.raises(AsyncJobError, match="weird"):
        poll_async_job(lambda: {"status": "weird"}, poll_time=10, poll_interval=0)


def test_raises_timeout_when_poll_time_elapses():
    with patch("time.sleep"):
        with pytest.raises(AsyncJobTimeoutError):
            poll_async_job(
                lambda: {"status": "IN_PROGRESS"},
                poll_time=0,
                poll_interval=0,
            )
