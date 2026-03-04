# Surge Python SDK

The Surge Python SDK provides convenient access to the Surge API from applications written in the Python language.

## Installation

Install this package by using pip:

```bash
pip install --upgrade surge-api
```

### Requirements

* Python 3.6+

## Getting Your API Key

Before using the SDK, you need to obtain an API key:

1. **Log in to Surge AI**
   - Go to https://app.surgehq.ai
   - Sign in with your account

2. **Navigate to Profile Settings**
   - Click your profile picture (top right)
   - Select "Profile" from the dropdown

3. **Get Your API Key**
   - Look for the "API Key" section
   - Click "Reveal" or "Copy" to get your key
   - It will look like: `surge_xxxxxxxxxxxxxxxxxxxxxxxx`

4. **Keep it secure!**
   - Never commit your API key to version control
   - Use environment variables in production

## Usage

### Authentication

There are two ways to authenticate:

#### Option 1: Environment Variable (Recommended)

```bash
export SURGE_API_KEY=surge_xxxxxxxxxxxxxxxxxxxxxxxx
```

```python
import surge
# API key is automatically loaded from environment
```

#### Option 2: Direct Configuration

```python
import surge
surge.api_key = "surge_xxxxxxxxxxxxxxxxxxxxxxxx"
```

### Quick Start Example

```python
import surge

# Set your API key
surge.api_key = "YOUR_API_KEY"

# List your projects
projects = surge.Project.list()
print(f"You have {len(projects)} projects")

# Get a specific project
project = surge.Project.retrieve("project-id-here")
print(project.name)
```

## Common Operations

### Downloading Project Results

Once authenticated, you can list all Projects or retrieve a specific Project by its ID:

```python
# List your Projects
projects = surge.Project.list()

# Print the name of the first Project
print(projects[0].name)

# Retrieve a specific Project
project = surge.Project.retrieve("076d207b-c207-41ca-b73a-5822fe2248ab")

# Download the results for that project
results = project.download_json()

# Alternatively, download the results to a file
project.save_report("export_csv", "results.csv")
```

### Creating Projects

If you have a blueprint, you can use it as a template to get a new batch of data annotated.
You can add new labeling tasks from a CSV or with a list of dictionaries.

```python
# List blueprint projects
blueprint_projects = surge.Project.list_blueprints()
blueprint = blueprint_projects[0]

# Create a project from a blueprint
project = surge.Project.create("My Labeling Project (July 2023 Batch)", template_id=blueprint.id)

# Add data from a CSV file
project.create_tasks_from_csv('my_data.csv')

# Or add data directly
tasks = project.create_tasks([{
    "company": "Surge",
    "city": "San Francisco",
    "state": "CA"
}])
```

### Creating Tasks

You can create new Tasks for a project, list all of the Tasks in a given project, or retrieve a specific Task given its ID.

```python
# Create Tasks for the new Project
tasks_data = [{"id": 1, "company": "Surge AI"}, {"id": 2, "company":"Twitch TV"}]
tasks = project.create_tasks(tasks_data)

# List all Tasks in the Project
all_tasks = project.list_tasks()

# Retrieve a specific Task
task = surge.Task.retrieve(task_id = "eaa44610-c8f6-4480-b746-28b6c8defd4d")

# Print the fields of that Task
print(task.fields)
```

You can also create Tasks in bulk by uploading a local CSV file. The header of the CSV file must specify the fields that are used in your Tasks.

| id    |   company             |
| :---  |   :----:              |
| 1     |   Surge AI    |
| 2     |   Twitch TV  |

```python
# Create Tasks in bulk via CSV file
file_path = "./companies_to_classify.csv"
tasks = project.create_tasks_from_csv(file_path)
```

## Error Handling

```python
import surge
from surge.errors import SurgeRequestError

try:
    project = surge.Project.retrieve("invalid-id")
except SurgeRequestError as e:
    print(f"API Error: {e}")
```

## Troubleshooting

### "Cannot seem to get API Key"

1. Make sure you're logged in to https://app.surgehq.ai
2. Check that you have a valid Surge AI account
3. The API key section is in your Profile page
4. If you still can't find it, contact support@surgehq.ai

### "Authentication failed"

1. Verify your API key is correct
2. Check that the key hasn't been revoked
3. Ensure no extra spaces when copying
4. Try using environment variable instead of hardcoding

## Full API Documentation

Complete API documentation is available at: https://app.surgehq.ai/docs/api#

## Development

The test suite depends on `pytest`, which you can install using pip:

```bash
pip install pytest
```

To run tests from the command line:

```bash
# Run all tests
pytest

# Run tests in a specific file
pytest tests/test_projects.py

# Run a specific test
pytest tests/test_projects.py::test_init_complete
```

## License

MIT License - See LICENSE file for details

## Support

- Documentation: https://app.surgehq.ai/docs/api#
- Email: support@surgehq.ai
- Issues: https://github.com/surge-ai/surge-python/issues
