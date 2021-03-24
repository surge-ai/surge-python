from datetime import datetime
from dateutil.tz import tzutc
import pytest

import surge
from surge.api_resource import APIResource
from surge.projects import Task
from surge.responses import Response, TaskResponse
from surge.errors import SurgeMissingIDError, SurgeMissingAttributeError


def test_raise_exception_if_missing_id():
    with pytest.raises(SurgeMissingIDError) as e_info:
        t = Task()

    with pytest.raises(SurgeMissingIDError) as e_info:
        t = Task(project_id="ABC1234")


def test_raise_exception_if_missing_project_id():
    with pytest.raises(SurgeMissingIDError) as e_info:
        t = Task(id="XYZ-123-ABC")


def test_init_basic():
    t = Task(id="XYZ-123-ABC",
             project_id="ABC1234",
             created_at='2021-01-22T19:49:03.185Z')

    assert isinstance(t, APIResource)
    assert isinstance(t, Task)
    assert t.id == "XYZ-123-ABC"
    assert t.project_id == "ABC1234"
    assert t.created_at == datetime(2021,
                                    1,
                                    22,
                                    19,
                                    49,
                                    3,
                                    185000,
                                    tzinfo=tzutc())


def test_init_complete():
    response_json = {
        'id':
        'eaa44510-c8f6-4480-b746-28a6c8defd4c',
        'project_id':
        'A1B2C3-abcd-1234-wxyz-5823gd2238ac',
        'status':
        'completed',
        'created_at':
        '2021-01-22T19:49:42.000Z',
        'is_gold_standard':
        False,
        'fields': {
            'id':
            '163',
            'video':
            'https://streamable.com/m/tyler-glasnow-foul-to-austin-barnes-xzJURv'
        },
        'gold_standards_data':
        None,
        'is_complete':
        True,
        'responses': [{
            'id': '6db8b28d-bddc-491f-81ba-dbeb9e9f4399',
            'data': {
                'What is the result of this pitch?': 'Foul Tip'
            },
            'completed_at': '2021-01-22T20:57:13.273Z',
            'worker_id': 'J14X3BTCZX3M'
        }]
    }

    t = Task(**response_json)

    assert isinstance(t, APIResource)
    assert isinstance(t, Task)
    assert t.id == "eaa44510-c8f6-4480-b746-28a6c8defd4c"
    assert t.project_id == "A1B2C3-abcd-1234-wxyz-5823gd2238ac"
    assert t.status == "completed"
    assert t.is_complete == True
    assert t.created_at == datetime(2021,
                                    1,
                                    22,
                                    19,
                                    49,
                                    42,
                                    000,
                                    tzinfo=tzutc())
    assert type(t.responses) == list
    for r in t.responses:
        assert isinstance(r, Response)
        assert isinstance(r, TaskResponse)


def test_print_attrs():
    attr = Task(id="XYZ-123-ABC",
                project_id="ABC1234",
                created_at='2021-01-22T19:49:03.185Z').print_attrs()
    assert attr == 'id="XYZ-123-ABC" project_id="ABC1234" created_at="2021-01-22 19:49:03.185000+00:00"'


def test_repr():
    attr = repr(
        Task(id="XYZ-123-ABC",
             project_id="ABC1234",
             created_at='2021-01-22T19:49:03.185Z'))
    assert attr == '<surge.Task#XYZ-123-ABC project_id="ABC1234" created_at="2021-01-22 19:49:03.185000+00:00">'


def test_str():
    t_str = str(
        Task(id="XYZ-123-ABC",
             project_id="ABC1234",
             created_at='2021-01-22T19:49:03.185Z'))
    assert t_str == '<surge.Task#XYZ-123-ABC>'
