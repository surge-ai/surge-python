# Surge Python SDK

The Surge Python SDK provides convenient access to the Surge API from applications written in the Python language.

## Installation

### Requirements

* Python 3.6+

## Usage

The library needs to be configured with your account's API key which is available in your Surge Profile. Set `surge.api_key` to its value:

```python
import surge
surge.api_key = "..."

# List your projects
surge.Projects.list()

# Retrieve a project
surge.Projects.retrieve("076d207b-c207-41ca-b73a-5822fe2248ab")

# Create a new project
questions = [{"text": "What is the name of the company at this website?"}, {"text": "What category does this company belong to?", "options": ["Tech", "Sports", "Gaming"]}, {"type": "checkbox", "text": "Check all the social media accounts this company has", "options": ["Facebook", "Twitter", "Pinterest", "Google+"]}]

surge.Projects.create(
    name = "Test Project", 
    payment_per_response = 0.1,
    instructions = "Hello World!", 
    questions = questions,
    callback_url = "https://customer-callback-url/",
    num_workers_per_task = 3
)
```
