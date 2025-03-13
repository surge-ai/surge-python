from unittest.mock import patch
from datetime import datetime
from dateutil.tz import tzutc
import pytest

import surge
from surge.api_resource import APIResource, PROJECTS_ENDPOINT
from surge.projects import Project
from surge.errors import SurgeMissingIDError, SurgeMissingAttributeError


def test_raise_exception_if_missing_id():
    with pytest.raises(SurgeMissingIDError) as e_info:
        p = Project(name="Test")


def test_raise_exception_if_missing_name():
    with pytest.raises(SurgeMissingAttributeError) as e_info:
        p = Project(id="123ABCD")


def test_init_basic():
    p = Project(id="ABC1234", name="Hello World", created_at="2021-01-22T19:49:03.185Z")

    assert isinstance(p, APIResource)
    assert isinstance(p, Project)
    assert p.id == "ABC1234"
    assert p.name == "Hello World"
    assert p.created_at == datetime(2021, 1, 22, 19, 49, 3, 185000, tzinfo=tzutc())


def test_init_complete():
    response_json = {
        "fields_template": '<p><iframe src="{{video}}" width="560" height="315"></iframe><br></p>',
        "id": "A1B2C3-abcd-1234-wxyz-5823gd2238ac",
        "slug": "aJlz0Vr2ozdX",
        "name": "Identifying video results",
        "num_workers_per_task": 3,
        "status": "paused",
        "created_at": "2021-01-22T19:49:03.185Z",
        "num_tasks_completed": 176,
        "num_responses_completed": 177,
        "instructions": "<p><b>Instructions: Categorize the following video.</b></p>",
        "num_tasks": 177,
        "link_to_work_on_task": "https://app.surgehq.ai/workers/tasks?project_id=A1B2C3-abcd-1234-wxyz-5823gd2238ac",
        "avg_gold_standard_score": 65.09,
        "interrater_agreement": {"What is this video?": 0.859154078549849},
        "private_workforce": False,
        "num_tasks_in_progress": 0,
        "payment_per_response": 0.12,
    }

    p = Project(**response_json)

    assert isinstance(p, APIResource)
    assert isinstance(p, Project)
    assert p.id == "A1B2C3-abcd-1234-wxyz-5823gd2238ac"
    assert p.name == "Identifying video results"
    assert (
        p.instructions == "<p><b>Instructions: Categorize the following video.</b></p>"
    )
    assert p.num_workers_per_task == 3
    assert p.status == "paused"
    assert p.num_tasks_completed == 176
    assert p.avg_gold_standard_score == 65.09
    assert p.interrater_agreement == {"What is this video?": 0.859154078549849}
    assert p.created_at == datetime(2021, 1, 22, 19, 49, 3, 185000, tzinfo=tzutc())


def test_print_attrs():
    attr = Project(
        id="ABC1234", name="Hello World", created_at="2021-01-22T19:49:03.185Z"
    ).print_attrs()
    assert (
        attr
        == 'id="ABC1234" name="Hello World" created_at="2021-01-22 19:49:03.185000+00:00"'
    )


def test_repr():
    attr = repr(
        Project(id="ABC1234", name="Hello World", created_at="2021-01-22T19:49:03.185Z")
    )
    assert (
        attr
        == '<surge.Project#ABC1234 name="Hello World" created_at="2021-01-22 19:49:03.185000+00:00">'
    )


def test_str():
    p_str = str(
        Project(id="ABC1234", name="Hello World", created_at="2021-01-22T19:49:03.185Z")
    )
    assert p_str == '<surge.Project#ABC1234 name="Hello World">'


def test_update_with_arbitrary_parameters():
    project = Project(id="UPDATE_ARBITRARY", name="Project to update")

    with patch.object(Project, "put") as mock_put:
        mock_put.return_value = {**project.to_dict(), "allow_purgatory_users": True}
        project.update(params={"allow_purgatory_users": True})
        mock_put.assert_called_once_with(
            f"{PROJECTS_ENDPOINT}/{project.id}",
            {"allow_purgatory_users": True},
            api_key=None,
        )

def test_update_with_fields_template():
    project = Project(id="UPDATE_FIELDS_TEMPLATE", name="Project to update")

    with patch.object(Project, "put") as mock_put:
        assert not hasattr(project, "fields_template")
        assert not hasattr(project, "fields_text")
        mock_put.return_value = {**project.to_dict(), "fields_text": "ABC"}
        updated = project.update(fields_template="ABC")
        mock_put.assert_called_once_with(
            f"{PROJECTS_ENDPOINT}/{project.id}",
            {"fields_text": "ABC"},
            api_key=None,
        )
