"""Polling helper for async-job status endpoints."""

import time

DEFAULT_IN_PROGRESS_STATUSES = frozenset({"IN_PROGRESS", "CREATING"})
DEFAULT_COMPLETED_STATUSES = frozenset({"COMPLETED", "READY"})
DEFAULT_ERROR_STATUSES = frozenset({"ERROR", "FAILED"})


class AsyncJobError(Exception):
    """Raised when an async job fails or times out.

    The ``status`` dict carries the underlying error; timeouts use the
    synthetic ``status="TIMEOUT"`` sentinel so callers can distinguish
    them from server-side failures.
    """

    def __init__(self, status):
        self.status = status
        error = status.get("error") or status.get("type") or "async job failed"
        super().__init__(error)


def poll_async_job(
    check_status,
    *,
    poll_time,
    poll_interval,
    initial_status=None,
    in_progress_statuses=DEFAULT_IN_PROGRESS_STATUSES,
    completed_statuses=DEFAULT_COMPLETED_STATUSES,
    error_statuses=DEFAULT_ERROR_STATUSES,
):
    """Poll ``check_status()`` until it returns a terminal status.

    Arguments:
        check_status: zero-arg callable returning a dict with a ``status`` key.
        poll_time: maximum seconds to wait before raising AsyncJobError
            with the synthetic ``status="TIMEOUT"`` sentinel.
        poll_interval: seconds to sleep between polls.
        initial_status: optional status dict consumed in place of the first
            ``check_status()`` call — useful when the caller already has the
            response from a kick-off endpoint.
        in_progress_statuses: status strings that mean "keep polling".
        completed_statuses: status strings that mean "return the status dict".
        error_statuses: status strings that mean "raise AsyncJobError".

    Returns the terminal status dict.
    """
    deadline = time.monotonic() + poll_time
    status = initial_status if initial_status is not None else check_status()
    while True:
        value = status.get("status")
        if value in completed_statuses:
            return status
        if value in error_statuses:
            raise AsyncJobError(status)
        if value not in in_progress_statuses:
            message = f"unexpected status {value!r}"
            raise AsyncJobError({**status, "error": message})
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            message = f"async job did not complete within {poll_time} seconds"
            raise AsyncJobError({"status": "TIMEOUT", "error": message})
        time.sleep(min(poll_interval, remaining))
        status = check_status()
