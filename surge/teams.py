import dateutil.parser

from surge.errors import SurgeMissingIDError
from surge.api_resource import TEAMS_ENDPOINT, APIResource


class Team(APIResource):

    def __init__(self, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.id is None:
            raise SurgeMissingIDError

        if self.description is None:
            self.description = ""

        if hasattr(self, "created_at") and self.created_at:
            # Convert timestamp str into datetime
            self.created_at = dateutil.parser.parse(self.created_at)

    def __str__(self):
        return f"<surge.Team#{self.id}>"

    def __repr__(self):
        return f"<surge.Team#{self.id} {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["id"])

    def update(self, name=None, description=None, api_key: str = None):
        '''
        Update an existing team

        Arguments:
            name (str): Name of the team.
            description (str): Team description.
        
        Returns:
            team: new Team object
        '''

        params = {}
        if name is not None and len(name) > 0:
            params["name"] = name
        if description is not None:
            params["description"] = description

        endpoint = f"{TEAMS_ENDPOINT}/{self.id}"
        response_json = self.put(endpoint, params, api_key=api_key)
        return Team(**response_json)

    def add_surgers(self, surger_ids, api_key: str = None):
        '''
        Add Surgers to the team

        Arguments:
            surger_ids (list): List of Surger IDs to add to the team.
        
        Returns:
            team: new Team object
        '''
        endpoint = f"{TEAMS_ENDPOINT}/{self.id}/add_surgers"
        params = {"surger_ids": surger_ids}
        response_json = self.post(endpoint, params, api_key=api_key)
        return Team(**response_json)

    def remove_surgers(self, surger_ids, api_key: str = None):
        '''
        Remove Surgers from the team

        Arguments:
            surger_ids (list): List of Surger IDs to remove from the team.
        
        Returns:
            team: new Team object
        '''
        endpoint = f"{TEAMS_ENDPOINT}/{self.id}/remove_surgers"
        params = {"surger_ids": surger_ids}
        response_json = self.post(endpoint, params, api_key=api_key)
        return Team(**response_json)

    @classmethod
    def create(cls,
               name: str,
               members: list,
               description=None,
               api_key: str = None):
        '''
        Creates a new Team.

        Arguments:
            name (str): Team name.
            members (list): List of user IDs to add to the team.
            description (str): Optional, team description.

        Returns:
            team: new Team object
        '''
        endpoint = f"{TEAMS_ENDPOINT}"
        data = {"name": name, "members": members}
        if description:
            data["description"] = description
        response_json = cls.post(endpoint, data, api_key=api_key)
        return cls(**response_json)

    @classmethod
    def list(cls, api_key: str = None):
        '''
        Lists all of your teams.
        Returns:
            teams (list): list of Team objects.
        '''
        endpoint = f"{TEAMS_ENDPOINT}/list"
        response_json = cls.get(endpoint, api_key=api_key)
        tasks = [Team(**team_data) for team_data in response_json]
        return tasks

    @classmethod
    def retrieve(cls, team_id: str, api_key: str = None):
        '''
        Retrieves a specific team you have created.

        Arguments:
            team_id (str): ID of team.

        Returns:
            team: Team object
        '''
        endpoint = f"{TEAMS_ENDPOINT}/{team_id}"
        response_json = cls.get(endpoint, api_key=api_key)
        return cls(**response_json)

    @classmethod
    def delete(cls, team_id: str, api_key: str = None):
        '''
        Delete the team with the given ID. This is an irreversible operation.
        
        Arguments:
            team_id (str): ID of team to be deleted.

        Returns:
            { "success": boolean }
        '''
        endpoint = f"{TEAMS_ENDPOINT}/{team_id}"
        response_json = cls.delete_request(endpoint, api_key=api_key)
        return response_json
