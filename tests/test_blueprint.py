from datetime import datetime
from dateutil.tz import tzutc
import unittest

from surge.errors import SurgeMissingAttributeError
from surge.api_resource import APIResource
from surge.projects import Project
from surge.blueprints import Blueprint


class BlueprintTests(unittest.TestCase):
    '''Use unittest in this class to assert on error messages.'''

    def test_validate_fields_data_fail(self):
        b = Blueprint(id=id,
                      name='name_blueprint',
                      created_at='2021-01-22T19:49:03.185Z')
        b.fields_template = '<p><iframe src="{{video}}" width="560" height="315"></iframe><br></p>'
        key = 'video'
        with self.assertRaises(SurgeMissingAttributeError) as context:
            Blueprint._validate_fields_data(b.required_data_fields(), [{'foo': 'task'}])
        self.assertTrue(key in str(context.exception), f'error message {context.exception} should contain {key}')


def test_validate_fields_data():
    # TODO: more test coverage
    b = Blueprint(id=id,
                  name='name_blueprint',
                  created_at='2021-01-22T19:49:03.185Z')
    b.fields_template = '<p><iframe src="{{video}}" width="560" height="315"></iframe><br></p>'

    key = 'video'
    Blueprint._validate_fields_data(b.required_data_fields(), [{key: 'task'}])


def test_required_data_fields():
    '''Ensure a Blueprint object knows how to find required fields in fields_template.'''
    assert_required_data_fields(None, [])
    assert_required_data_fields('', [])
    assert_required_data_fields('foo', [])
    assert_required_data_fields('{{one}}', ['one'])
    assert_required_data_fields('{{video}}{{audio}}{{spacial}}', ["video", "audio", "spacial"])
    assert_required_data_fields('<p><iframe src="{{video}}" width="560" height="315"></iframe><br></p>', ['video'])


def test_init_basic():
    project_id = "ABC1234"
    name = "Hello World Blueprint"
    blueprint = Blueprint(id=project_id,
                          name=name,
                          created_at='2021-01-22T19:49:03.185Z')

    assert isinstance(blueprint, APIResource)
    assert isinstance(blueprint, Project)
    assert isinstance(blueprint, Blueprint)
    assert blueprint.id == project_id
    assert blueprint.name == name
    assert blueprint.created_at == datetime(2021,
                                            1,
                                            22,
                                            19,
                                            49,
                                            3,
                                            185000,
                                            tzinfo=tzutc())


def assert_required_data_fields(fields_template, expected_fields):
    blueprint = Blueprint(id="id1",
                          name="name1",
                          created_at='2021-01-22T19:49:03.185Z')
    blueprint.fields_template = fields_template
    assert_values_in(blueprint.required_data_fields(), expected_fields)


def assert_values_in(ary, expected):
    for value in expected:
        assert value in ary
