from datetime import datetime
from dateutil.tz import tzutc
import pytest

import surge
from surge.api_resource import APIResource
from surge.projects import Project
from surge.questions import Question, FreeResponseQuestion, MultipleChoiceQuestion, CheckboxQuestion, TextTaggingQuestion, TextArea
from surge.errors import SurgeMissingIDError, SurgeMissingAttributeError


def test_raise_exception_if_missing_id():
    with pytest.raises(SurgeMissingIDError) as e_info:
        p = Project(name="Test")


def test_raise_exception_if_missing_name():
    with pytest.raises(SurgeMissingAttributeError) as e_info:
        p = Project(id="123ABCD")


def test_init_basic():
    p = Project(id="ABC1234",
                name="Hello World",
                created_at='2021-01-22T19:49:03.185Z')

    assert isinstance(p, APIResource)
    assert isinstance(p, Project)
    assert p.id == "ABC1234"
    assert p.name == "Hello World"
    assert p.created_at == datetime(2021,
                                    1,
                                    22,
                                    19,
                                    49,
                                    3,
                                    185000,
                                    tzinfo=tzutc())


def test_init_complete():
    response_json = {
        'fields_template':
        '<p><iframe src="{{video}}" width="560" height="315"></iframe><br></p>',
        'id':
        'A1B2C3-abcd-1234-wxyz-5823gd2238ac',
        'slug':
        'aJlz0Vr2ozdX',
        'name':
        'Identifying video results',
        'num_workers_per_task':
        3,
        'status':
        'paused',
        'created_at':
        '2021-01-22T19:49:03.185Z',
        'num_tasks_completed':
        176,
        'num_responses_completed':
        177,
        'instructions':
        '<p><b>Instructions: Categorize the following video.</b></p>',
        'num_tasks':
        177,
        'link_to_work_on_task':
        'https://app.surgehq.ai/workers/tasks?project_id=A1B2C3-abcd-1234-wxyz-5823gd2238ac',
        'avg_gold_standard_score':
        65.09,
        'interrater_agreement': {
            'What is this video?': 0.859154078549849
        },
        'private_workforce':
        False,
        'num_tasks_in_progress':
        0,
        'payment_per_response':
        0.12,
        'questions': [{
            'id':
            'c6ee667c-b260-415d-a200-f34250793b81',
            'text':
            'What is this video?',
            'required':
            True,
            'ner_allow_overlapping_tags':
            None,
            'ner_allow_relationship_tags':
            None,
            'preexisting_annotations':
            None,
            'require_tie_breaker':
            False,
            'type':
            'multiple_choice',
            'options': ['Option A', 'Option B', 'Option C'],
            'options_objects': [{
                'id': 'a1aex762-8b06-5xce-zd28-3fac8c4245b0',
                'text': 'Option A',
                'item_id': 'xyz123c-h260-415l-a999-g34250793b80',
                'created_at': '2021-01-22T19:53:04.552Z',
                'updated_at': '2021-01-22T19:53:04.552Z',
                'order': 1
            }, {
                'id': 'd77k9c91-9d9c-463c-87o7-b153eb89dfle',
                'text': 'Option B',
                'item_id': 'xyz123c-h260-415l-a999-g34250793b80',
                'created_at': '2021-01-22T19:53:04.557Z',
                'updated_at': '2021-01-22T19:53:04.557Z',
                'order': 2
            }, {
                'id': 'r79682ds-5cc4-4e54-8c6f-7ef06olo3c79',
                'text': 'Option C',
                'item_id': 'xyz123c-h260-415l-a999-g34250793b80',
                'created_at': '2021-01-22T19:53:04.560Z',
                'updated_at': '2021-01-22T19:53:04.560Z',
                'order': 3
            }]
        }]
    }

    p = Project(**response_json)

    assert isinstance(p, APIResource)
    assert isinstance(p, Project)
    assert p.id == "A1B2C3-abcd-1234-wxyz-5823gd2238ac"
    assert p.name == "Identifying video results"
    assert p.instructions == '<p><b>Instructions: Categorize the following video.</b></p>'
    assert p.num_workers_per_task == 3
    assert p.status == 'paused'
    assert p.num_tasks_completed == 176
    assert p.avg_gold_standard_score == 65.09
    assert p.interrater_agreement == {'What is this video?': 0.859154078549849}
    assert p.created_at == datetime(2021,
                                    1,
                                    22,
                                    19,
                                    49,
                                    3,
                                    185000,
                                    tzinfo=tzutc())
    assert type(p.questions) == list
    for q in p.questions:
        assert isinstance(q, Question)
        assert isinstance(q, MultipleChoiceQuestion)
        assert type(q.options) == list


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


def test_convert_questions_to_objects():
    questions_data = [{
        'id':
        'cd3efdb7-3cf2-4558-b443-486fd09b4cc6',
        'text':
        'Checkbox for {{url}}',
        'required':
        True,
        'ner_allow_overlapping_tags':
        None,
        'ner_allow_relationship_tags':
        None,
        'preexisting_annotations':
        None,
        'require_tie_breaker':
        False,
        'type':
        'checkbox',
        'options': ['Option 1', 'Option 2'],
        'options_objects': [{
            'id': 'f3c69282-93dd-496e-aeba-4768f5eea658',
            'text': 'Option 1',
            'item_id': 'cd3efdb7-3cf2-4558-b443-486fd09b4cc6',
            'created_at': '2021-02-20T20:56:34.540Z',
            'updated_at': '2021-02-20T20:56:34.540Z',
            'order': 1
        }, {
            'id': '0dffdc42-4abe-4b39-99b3-4b3bcfda5b55',
            'text': 'Option 2',
            'item_id': 'cd3efdb7-3cf2-4558-b443-486fd09b4cc6',
            'created_at': '2021-02-20T20:56:34.543Z',
            'updated_at': '2021-02-20T20:56:34.543Z',
            'order': 2
        }]
    }, {
        'id':
        'c4b0d6a9-f735-40c1-9b42-0414945ef2db',
        'text':
        'Multiple choice for {{url}}',
        'required':
        False,
        'ner_allow_overlapping_tags':
        None,
        'ner_allow_relationship_tags':
        None,
        'preexisting_annotations':
        None,
        'require_tie_breaker':
        False,
        'type':
        'multiple_choice',
        'options': ['Choice 1', 'Choice 2'],
        'options_objects': [{
            'id': '92ca3805-efdd-4740-b0a6-bf35997be321',
            'text': 'Choice 1',
            'item_id': 'c4b0d6a9-f735-40c1-9b42-0414945ef2db',
            'created_at': '2021-02-20T20:56:34.549Z',
            'updated_at': '2021-02-20T20:56:34.549Z',
            'order': 1
        }, {
            'id': '44756518-06db-4774-a4b9-32ffc33351b6',
            'text': 'Choice 2',
            'item_id': 'c4b0d6a9-f735-40c1-9b42-0414945ef2db',
            'created_at': '2021-02-20T20:56:34.551Z',
            'updated_at': '2021-02-20T20:56:34.551Z',
            'order': 2
        }]
    }, {
        'id': '6123463e-349e-4450-80d2-6684a28755b3',
        'text': 'Free response for {{url}}',
        'required': False,
        'ner_allow_overlapping_tags': None,
        'ner_allow_relationship_tags': None,
        'preexisting_annotations': None,
        'type': 'free_response',
        'options': [],
        'options_objects': []
    }, {
        'id':
        'c46e2714-9bf6-44a8-aac3-f01f9fec8ae2',
        'text':
        'This is a Named Entity Recognition prompt for {{url}}',
        'required':
        False,
        'ner_allow_overlapping_tags':
        None,
        'ner_allow_relationship_tags':
        None,
        'preexisting_annotations':
        None,
        'ner_token_granularity':
        True,
        'require_tie_breaker':
        False,
        'type':
        'text_tagging',
        'options': ['Label 1', 'Label 2', 'Label 3'],
        'options_objects': [{
            'id': '6a434174-09ee-48c3-8490-149ac4554132',
            'text': 'Label 1',
            'item_id': 'c46e2714-9bf6-44a8-aac3-f01f9fec8ae2',
            'created_at': '2021-02-20T20:56:34.569Z',
            'updated_at': '2021-02-20T20:56:34.569Z',
            'order': 1
        }, {
            'id': '3747d91a-79a9-4227-8daf-32384d4f1b4f',
            'text': 'Label 2',
            'item_id': 'c46e2714-9bf6-44a8-aac3-f01f9fec8ae2',
            'created_at': '2021-02-20T20:56:34.572Z',
            'updated_at': '2021-02-20T20:56:34.572Z',
            'order': 2
        }, {
            'id': '46f3cf0d-687e-4a44-a436-47681b64f7d5',
            'text': 'Label 3',
            'item_id': 'c46e2714-9bf6-44a8-aac3-f01f9fec8ae2',
            'created_at': '2021-02-20T20:56:34.575Z',
            'updated_at': '2021-02-20T20:56:34.575Z',
            'order': 3
        }]
    }, {
        'id': '6123463e-349e-4450-80d2-6684a28755b4',
        'text': 'Text area for {{url}}',
        'type': 'text',
        'required': False,
        'options': [],
        'options_objects': []
    }]

    project = Project(id="ABC1234", name="Hello World")
    questions = project._convert_questions_to_objects(questions_data)
    assert type(questions) == list
    assert len(questions) == 5

    assert type(questions[0]) == CheckboxQuestion
    assert questions[0].text == 'Checkbox for {{url}}'
    assert questions[0].required == True
    assert questions[0].options

    assert type(questions[1]) == MultipleChoiceQuestion
    assert questions[1].text == 'Multiple choice for {{url}}'
    assert questions[1].required == False
    assert questions[1].options

    assert type(questions[2]) == FreeResponseQuestion
    assert questions[2].text == 'Free response for {{url}}'
    assert questions[2].required == False
    assert not hasattr(questions[2], "options")

    assert type(questions[3]) == TextTaggingQuestion
    assert questions[
        3].text == 'This is a Named Entity Recognition prompt for {{url}}'
    assert questions[3].required == False
    assert questions[3].options

    assert type(questions[4]) == TextArea
    assert questions[
        4].text == 'Text area for {{url}}'
    assert questions[4].required == False
    assert not hasattr(questions[4], "options")
