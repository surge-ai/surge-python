import json


class Response(object):
    def __init__(self, id: str):
        self.id = id

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class TaskResponse(Response):
    def __init__(self, id: str, data: dict, time_spent_in_secs: int,
                 completed_at: str, worker_id: str):
        super().__init__(id)
        self.data = data
        self.time_spent_in_secs = time_spent_in_secs
        self.completed_at = completed_at
        self.worker_id = worker_id
