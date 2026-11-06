from datetime import datetime
from unittest.mock import patch

import pytest

from surge.errors import SurgeTaskDataError
from surge.tasks import Task


@pytest.mark.parametrize("bulk", [False, True])
@pytest.mark.parametrize("value,error,detail", [
    ({1, 2}, TypeError, "set is not JSON serializable"),
    ({
        (1, 2): "value"
    }, TypeError, "keys must be str"),
    (datetime(2026, 1, 1), TypeError, "datetime is not JSON serializable"),
    (float("nan"), ValueError, "Out of range float values"),
    (float("inf"), ValueError, "Out of range float values"),
    (-float("inf"), ValueError, "Out of range float values"),
])
def test_invalid_task_data_preserves_json_error(bulk, value, error, detail):
    with patch.object(Task, "post") as post:
        with pytest.raises(SurgeTaskDataError, match=detail) as exc:
            if bulk:
                Task.create_many("project", [{"value": value}], launch=False)
            else:
                Task.create("project", value=value)
        post.assert_not_called()
    assert isinstance(exc.value.__cause__, error)


@pytest.mark.parametrize("bulk", [False, True])
def test_circular_task_data_preserves_json_error(bulk):
    value = []
    value.append(value)
    with patch.object(Task, "post") as post:
        with pytest.raises(SurgeTaskDataError,
                           match="Circular reference detected") as exc:
            if bulk:
                Task.create_many("project", [{"value": value}], launch=False)
            else:
                Task.create("project", value=value)
        post.assert_not_called()
    assert isinstance(exc.value.__cause__, ValueError)


def test_serializable_single_task_is_sent_unchanged():
    fields = {"value": {"nested": [None, True, 1, 1.5, "café"]}}
    response = {"id": "task", "project_id": "project", "fields": fields}
    with patch.object(Task, "post", return_value=response) as post:
        result = Task.create("project", api_key="test-key", **fields)
    post.assert_called_once_with("projects/project/tasks", {"fields": fields},
                                 api_key="test-key")
    assert result.fields == fields


def test_serializable_bulk_tasks_are_sent_unchanged():
    fields = {"value": {"nested": [None, True, 1, 1.5, "café"]}}
    response = {"id": "task", "project_id": "project", "fields": fields}
    with patch.object(Task, "post", return_value=[response]) as post:
        result = Task.create_many("project", [fields],
                                  launch=True,
                                  api_key="test-key")
    post.assert_called_once_with("projects/project/tasks/create_tasks", {
        "tasks": [fields],
        "launch": True
    },
                                 api_key="test-key")
    assert result[0].fields == fields
