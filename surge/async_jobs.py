"""Polling helper for async-job status endpoints."""

import time

DEFAULT_IN_PROGRESS_STATUSES = ("IN_PROGRESS", "CREATING")
DEFAULT_COMPLETED_STATUSES = ("COMPLETED", "READY")
DEFAULT_ERROR_STATUSES = ("ERROR", "FAILED")


class AsyncJobError(Exception):
    """Raised when an async job returns a terminal error status."""

    def __init__(self, status):
        self.status = status
        error = status.get("error") or status.get("type") or "async job failed"
        super().__init__(error)


class AsyncJobTimeoutError(Exception):
    """Raised when an async job does not reach a terminal status in time."""


def poll_async_job(
    check_status,
    *,
    poll_time,
    poll_interval,
    in_progress_statuses=DEFAULT_IN_PROGRESS_STATUSES,
    completed_statuses=DEFAULT_COMPLETED_STATUSES,
    error_statuses=DEFAULT_ERROR_STATUSES,
):
    """Poll ``check_status()`` until it returns a terminal status.

    Arguments:
        check_status: zero-arg callable returning a dict with a ``status`` key.
        poll_time: maximum seconds to wait before raising AsyncJobTimeoutError.
        poll_interval: seconds to sleep between polls.
        in_progress_statuses: status strings that mean "keep polling".
        completed_statuses: status strings that mean "return the status dict".
        error_statuses: status strings that mean "raise AsyncJobError".

    Returns the terminal status dict.
    """
    in_progress = set(in_progress_statuses)
    completed = set(completed_statuses)
    error = set(error_statuses)

    deadline = time.monotonic() + poll_time
    while True:
        status = check_status()
        value = status.get("status")
        if value in completed:
            return status
        if value in error:
            raise AsyncJobError(status)
        if value not in in_progress:
            raise AsyncJobError({**status, "error": f"unexpected status {value!r}"})
        if time.monotonic() >= deadline:
            raise AsyncJobTimeoutError(
                f"async job did not complete within {poll_time} seconds"
            )
        time.sleep(poll_interval)
