import json
from datetime import datetime


class Response(object):
    def __init__(self, id: str):
        self.id = id

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())

    def print_attrs(self, forbid_list: list = []):
        return " ".join([
            f"{k}=\"{v}\"" for k, v in self.__dict__.items()
            if not k in forbid_list
        ])


class TaskResponse(Response):
    def __init__(self, id: str, data: dict, completed_at: datetime,
                 worker_id: str):
        super().__init__(id)
        self.data = data
        self.completed_at = completed_at
        self.worker_id = worker_id

    def __str__(self):
        return f"<surge.TaskResponse#{self.id}>"

    def __repr__(self):
        return f"<surge.TaskResponse#{self.id} {self.attrs_repr()}>"

    def attrs_repr(self):
        return self.print_attrs(forbid_list=["id"])
