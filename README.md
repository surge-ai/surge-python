# Surge Python SDK

The Surge Python SDK provides convenient access to the Surge API from applications written in the Python language.

## Installation

Install this package by using pip:

```bash
pip install --upgrade surge-api
```

### Requirements

* Python 3.6+

## Usage

Documentation and and examples are available [here](https://app.surgehq.ai/docs/api#).

### Authentication

The library needs to be configured with your account's API key which is available in your Surge Profile. Set `surge.api_key` to its value:

```python
import surge
surge.api_key = "YOUR API KEY"
```
Or set the API key as an environment variable:

```bash
export SURGE_API_KEY=<YOUR API KEY>
```

### Projects

Once the API key has been set, you can list all of the Projects under your Surge account or retrieve a specific Project by its ID.

```python
# List your Projects
projects = surge.Project.list()

# Print the name of the first Project
print(projects[0].name)

# Retrieve a specific Project
project = surge.Project.retrieve("076d207b-c207-41ca-b73a-5822fe2248ab")

# print the number of tasks in that Project
print(project.num_tasks)
```

When creating a new Project, you can create a list of Questions and include them in the new Project.

```python
from surge.questions import FreeResponseQuestion, MultipleChoiceQuestion, CheckboxQuestion

# Create a new Project
free_response_q = FreeResponseQuestion(
    text="What is this company's website?")

multiple_choice_q = MultipleChoiceQuestion(
    text="What category does this company belong to?",
    options=["Tech", "Sports", "Gaming"])

checkbox_q = CheckboxQuestion(
    text="Check all the social media accounts this company has",
    options=["Facebook", "Twitter", "Pinterest", "Google+"])

fields_template_text = '''
    <p>website: {{website}}</p>
'''

project = surge.Project.create(
    name="Categorize this company",
    instructions="You will be asked to categorize a company.",
    questions=[free_response_q, multiple_choice_q, checkbox_q],
    callback_url="https://customer-callback-url/",
    fields_template=fields_template_text,
    num_workers_per_task=3)
```

### Tasks

You can create new Tasks for a project, list all of the Tasks in a given project, or retrieve a specific Task given its ID.

```python
# Create Tasks for the new Project
tasks_data = [{"id": 1, "company": Surge AI"}, {"id": 2, "company":"Twitch TV"}]
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
file_path = './companies_to_classify.csv'
tasks = project.create_tasks_from_csv(file_path)
```


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
