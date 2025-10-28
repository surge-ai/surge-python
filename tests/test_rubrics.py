from unittest.mock import patch

from surge.api_resource import APIResource
from surge.rubrics import Rubric


def test_evaluate_with_all_params():
    """Test evaluate method with all parameters provided"""
    with patch.object(Rubric, "post") as mock_post:
        mock_post.return_value = {
            "answer": True,
            "explanation": 'The text explicitly mentions two animals: "fox" and "dog." Therefore, it contains an animal, satisfying the rubric.',
        }

        result = Rubric.evaluate(
            text_for_grading="The quick brown fox jumps over the lazy dog",
            rubric_text="Check if the text contains an animal",
            prompt="Grade this text based on the rubric",
            api_key="test_key",
        )

        mock_post.assert_called_once_with(
            "evaluate_rubric",
            {
                "text_for_grading": "The quick brown fox jumps over the lazy dog",
                "rubric_text": "Check if the text contains an animal",
                "prompt": "Grade this text based on the rubric",
            },
            api_key="test_key",
        )

        assert result["answer"] == True
        assert "fox" in result["explanation"] or "dog" in result["explanation"]


def test_evaluate_without_prompt():
    """Test evaluate method without optional prompt parameter"""
    with patch.object(Rubric, "post") as mock_post:
        mock_post.return_value = {
            "answer": False,
            "explanation": "The text does not contain any animals.",
        }

        result = Rubric.evaluate(
            text_for_grading="The quick brown car drives down the road",
            rubric_text="Check if the text contains an animal",
        )

        mock_post.assert_called_once_with(
            "evaluate_rubric",
            {
                "text_for_grading": "The quick brown car drives down the road",
                "rubric_text": "Check if the text contains an animal",
            },
            api_key=None,
        )

        assert result["answer"] == False
        assert "explanation" in result


def test_evaluate_returns_dict():
    """Test that evaluate returns a dictionary with expected keys"""
    with patch.object(Rubric, "post") as mock_post:
        mock_post.return_value = {"answer": True, "explanation": "Test explanation"}

        result = Rubric.evaluate(
            text_for_grading="Sample text", rubric_text="Sample rubric"
        )

        assert isinstance(result, dict)
        assert "answer" in result
        assert "explanation" in result
        assert isinstance(result["answer"], bool)
        assert isinstance(result["explanation"], str)


def test_rubric_inherits_from_api_resource():
    """Test that Rubric class inherits from APIResource"""
    assert issubclass(Rubric, APIResource)
