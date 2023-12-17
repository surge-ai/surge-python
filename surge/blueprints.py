import re
from surge.projects import Project
from surge.errors import SurgeMissingAttributeError


class Blueprint(Project):
    def __int__(self, **kwargs):
        super().__init__(kwargs)

    @classmethod
    def _from_project(cls, project):
        '''Converts a Project to a Blueprint. This is useful when we want to create a Project and then return
        a Blueprint to the user.

        Arguments:
            project (Project): The project to convert to a Blueprint

        Returns:
            blueprint (Blueprint): A Blueprint derived from the given Project
        '''
        kwargs = project.__dict__
        # A Project object will have already parsed created_at, so omit that and save current value to avoid errors.
        created_at = kwargs.pop('created_at', None)
        b = Blueprint(**project.__dict__)
        b.created_at = created_at
        return b

    def required_data_fields(self):
        '''
        Returns all keys surrounded by {{}} from the fields_template string.

        Returns:
            matches (list): all the required data fields from fields_template
            e.g. ['field1', 'field2']
        '''
        if not self.fields_template:
            return []
        pattern = r"{{(.*?)}}"
        matches = re.findall(pattern, self.fields_template)
        return matches

    def create_new_batch(self, name):
        '''
        Create a new project from this blueprint. Once created, call create_tasks on the returned object
        to assign tasks.

        Arguments:
            name (str): Name of the project

        Returns:
            blueprint (Blueprint): a created project from a blueprint project which can be assigned tasks and launched.
        '''
        if not name:
            raise SurgeMissingAttributeError('name is required when creating a project from a template')

        create_params = {'template_id': self.id, 'name': name}
        project = Project.create(**create_params)
        blueprint = Blueprint._from_project(project)
        return blueprint

    def create_tasks(self, tasks_data: list, launch=False):
        '''Create tasks for this Blueprint project. Ensures that task_data contains fields referenced in
        fields_template.

        Arguments:
            tasks_data (list): List of dicts. Each dict is key/value pairs for populating fields_template.

        Returns:
            tasks (list): list of Tasks objects
        '''
        Blueprint._validate_fields_data(self.required_data_fields(), tasks_data)
        return super().create_tasks(tasks_data, launch)

    @classmethod
    def _validate_fields_data(cls, required_fields, tasks_data):
        '''
        Checks the keys in task_data exist in required_fields.
        NOTE: this assumes tasks_data is a flat dict (no nested keys).

        Arguments:
            required_fields (list): list of required field names
            tasks_data (list) list of dicts of task_data. All keys in these dicts should exist in required_fields

        Returns:
            None. Only raises if there are required fields missing.
        '''
        missing_keys = []
        for data in tasks_data:
            diff = set(required_fields) - set(data)
            if diff:
                missing_keys.append(diff)
        if missing_keys:
            msg = f'task_data is missing required keys: {missing_keys}'
            raise SurgeMissingAttributeError(msg)
