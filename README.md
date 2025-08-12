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

Documentation and examples are available [here](https://app.surgehq.ai/docs/api#).

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

### Downloading project results

Once the API key has been set, you can list all of the Projects under your Surge account or retrieve a specific Project by its ID.

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

### Creating projects

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

### Creating tasks

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
