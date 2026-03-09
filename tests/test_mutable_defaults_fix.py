"""
Test to verify that mutable default arguments bug is fixed.

This test ensures that creating multiple projects doesn't share state
between calls due to mutable default arguments (lists and dicts).
"""
from unittest.mock import patch
import pytest
from surge.projects import Project


def test_create_multiple_projects_with_template_no_shared_state():
    """
    Verify that creating multiple projects with template_id doesn't
    cause shared state between calls.

    This test reproduces the bug where project1's name would be overwritten
    with project2's name due to mutable default arguments.
    """

    # Mock the API responses
    with patch.object(Project, 'post') as mock_post, \
         patch.object(Project, 'get') as mock_get:

        # Setup mock responses for project creation
        mock_post.side_effect = [
            {"id": "project-1", "name": "Test Project 1"},
            {"id": "project-2", "name": "Test Project 2"},
        ]

        # Setup mock responses for project retrieval
        mock_get.side_effect = [
            {"id": "project-1", "name": "Test Project 1"},
            {"id": "project-2", "name": "Test Project 2"},
            {"id": "project-1", "name": "Test Project 1"},  # Third retrieve of project 1
        ]

        # Create first project
        project1 = Project.create(
            name="Test Project 1",
            template_id="template-123"
        )
        assert project1.name == "Test Project 1"
        assert project1.id == "project-1"

        # Retrieve to verify
        project1_retrieved = Project.retrieve("project-1")
        assert project1_retrieved.name == "Test Project 1"

        # Create second project
        project2 = Project.create(
            name="Test Project 2",
            template_id="template-123"
        )
        assert project2.name == "Test Project 2"
        assert project2.id == "project-2"

        # Retrieve to verify
        project2_retrieved = Project.retrieve("project-2")
        assert project2_retrieved.name == "Test Project 2"

        # Retrieve project 1 again - this is where the bug would manifest
        # Before fix: project1 would have name "Test Project 2"
        # After fix: project1 should still have name "Test Project 1"
        project1_retrieved_again = Project.retrieve("project-1")
        assert project1_retrieved_again.name == "Test Project 1", \
            f"Project 1 name was corrupted! Expected 'Test Project 1' but got '{project1_retrieved_again.name}'"

        # Verify the params passed to post don't share state
        assert mock_post.call_count == 2

        # Get the params from each call
        call1_params = mock_post.call_args_list[0][0][1]  # First call, second argument (params)
        call2_params = mock_post.call_args_list[1][0][1]  # Second call, second argument (params)

        # Verify each call had correct name
        assert call1_params["name"] == "Test Project 1"
        assert call2_params["name"] == "Test Project 2"

        # Verify params dicts are different objects (not shared)
        assert call1_params is not call2_params


def test_params_dict_not_shared_between_calls():
    """
    Test that the params dict default argument doesn't share state
    between multiple create() calls.
    """
    with patch.object(Project, 'post') as mock_post:
        mock_post.side_effect = [
            {"id": "p1", "name": "Project 1"},
            {"id": "p2", "name": "Project 2"},
        ]

        # Create first project with custom params
        Project.create(
            name="Project 1",
            params={"custom_field": "value1"}
        )

        # Create second project without custom params
        # Bug: If params dict is shared, it would still contain custom_field
        Project.create(
            name="Project 2"
        )

        # Verify second call doesn't have custom_field from first call
        second_call_params = mock_post.call_args_list[1][0][1]

        # The second call should not have the custom_field from the first call
        # (unless params dict was incorrectly shared)
        assert "custom_field" not in second_call_params or \
               second_call_params.get("custom_field") != "value1", \
               "params dict is being shared between calls!"


def test_list_defaults_not_shared():
    """
    Test that list default arguments (questions, tags, etc.) don't share
    state between multiple create() calls.
    """
    with patch.object(Project, 'post') as mock_post:
        mock_post.side_effect = [
            {"id": "p1", "name": "Project 1"},
            {"id": "p2", "name": "Project 2"},
        ]

        # Create first project
        Project.create(name="Project 1")

        # Create second project
        Project.create(name="Project 2")

        # Get the params from each call
        call1_params = mock_post.call_args_list[0][0][1]
        call2_params = mock_post.call_args_list[1][0][1]

        # Verify that the lists are different objects
        assert call1_params["questions"] is not call2_params["questions"]
        assert call1_params["tags"] is not call2_params["tags"]
        assert call1_params["qualifications_required"] is not call2_params["qualifications_required"]


def test_update_params_not_shared():
    """
    Test that update() method's params dict doesn't share state.
    """
    project = Project(id="test-id", name="Test Project")

    with patch.object(Project, 'put') as mock_put:
        mock_put.side_effect = [
            {"id": "test-id", "name": "Updated 1"},
            {"id": "test-id", "name": "Updated 2"},
        ]

        # First update
        project.update(name="Updated 1", params={"field1": "value1"})

        # Second update without params
        project.update(name="Updated 2")

        # Verify second call doesn't have field1 from first call
        second_call_params = mock_put.call_args_list[1][0][1]
        assert "field1" not in second_call_params or \
               second_call_params.get("field1") != "value1", \
               "params dict is being shared between update calls!"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
