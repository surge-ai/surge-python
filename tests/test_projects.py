from datetime import datetime
import pytest

import surge
from surge.projects import Project
from surge.errors import SurgeMissingIDError, SurgeMissingAttributeError


def test_raise_exception_if_missing_id():
    with pytest.raises(SurgeMissingIDError) as e_info:
        p = Project(name="Test")


def test_raise_exception_if_missing_name():
    with pytest.raises(SurgeMissingAttributeError) as e_info:
        p = Project(id="123ABCD")


def test_print_attrs():
    attr = Project(id="ABC1234",
                   name="Hello World",
                   created_at='2021-01-22T19:49:03.185Z').print_attrs()
    assert attr == 'id="ABC1234" name="Hello World" created_at="2021-01-22 19:49:03.185000+00:00"'


def test_repr():
    attr = repr(
        Project(id="ABC1234",
                name="Hello World",
                created_at='2021-01-22T19:49:03.185Z'))
    assert attr == '<surge.Project#ABC1234 name="Hello World" created_at="2021-01-22 19:49:03.185000+00:00">'


def test_str():
    p_str = str(
        Project(id="ABC1234",
                name="Hello World",
                created_at='2021-01-22T19:49:03.185Z'))
    assert p_str == '<surge.Project#ABC1234 name="Hello World">'
