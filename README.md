# surge-python

## Usage

The library needs to be configured with your account's API key which is available in your Surge Profile. Set `surge.api_key` to its value:

```
import surge
surge.api_key = "..."

# List your projects
surge.Projects.list()

# Retrieve a project
surge.Projects.retrieve("076d207b-c207-41ca-b73a-5822fe2248ab")

# Create a new project
surge.Projects.create("Test Project", 0.1, "Hello World!", [{"text": "What is the name of the company at this website?"}, {"text": "What category does this company belong to?", "options": ["Tech", "Sports", "Gaming"]}, {"type": "checkbox", "text": "Check all the social media accounts this company has", "options": ["Facebook", "Twitter", "Pinterest", "Google+"]}])
```