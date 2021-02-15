# Surge Python SDK

The Surge Python SDK provides convenient access to the Surge API from applications written in the Python language.

## Installation

Install this package by using pip:

```bash
pip install git+ssh://git@github.com/surge-ai/surge-python.git
```

### Requirements

* Python 3.6+

## Usage

The library needs to be configured with your account's API key which is available in your Surge Profile. Set `surge.api_key` to its value:

```python
import surge
surge.api_key = "..."

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
free_response_q = FreeResponseQuestion(text = "What is the name of the company at this website?")
multiple_choice_q = MultipleChoiceQuestion(text = "What category does this company belong to?", options = ["Tech", "Sports", "Gaming"])
checkbox_q = CheckboxQuestion(text = "Check all the social media accounts this company has", options = ["Facebook", "Twitter", "Pinterest", "Google+"])

surge.Project.create(
    name = "Test Project", 
    payment_per_response = 0.1,
    instructions = "Hello World!", 
    questions = [free_response_q, multiple_choice_q, checkbox_q],
    callback_url = "https://customer-callback-url/",
    num_workers_per_task = 3
)
```

You can list all of the Tasks for a given project, or retrieve a specific Task given its ID.

```python
# List all Tasks in a Project
surge.Task.list(project_id = "076d207b-c207-41ca-b73a-5822fe2248ab")

# Retrieve a specific Task
surge.Task.retrieve(task_id = "eaa44610-c8f6-4480-b746-28b6c8defd4d")
```