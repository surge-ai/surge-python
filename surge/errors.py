class SurgeRequestError(Exception):
    """Catch-all exception for errors that occur when making a request"""

    def __init__(self, message="Something went wrong with the API request."):
        self.message = message
        super().__init__(self.message)


class SurgeMissingAPIKeyError(Exception):
    """Raise when user has not set their API key"""

    def __init__(self, message="Surge API key has not been set."):
        self.message = message
        super().__init__(self.message)


class SurgeMissingIDError(Exception):
    """Raise when a Surge object is missing an ID"""

    def __init__(self, message="Must be initialized with an id."):
        self.message = message
        super().__init__(self.message)


class SurgeMissingAttributeError(Exception):
    """Raise when a Surge object is missing a required attribute"""

    def __init__(self, message="Object is missing a required attribute."):
        self.message = message
        super().__init__(self.message)



class SurgeTaskDataError(Exception):
    """Raise for exceptions that occur when creating Task objects"""

    def __init__(
        self,
        message="Invalid argument: task_data must be a non-empty list of dicts."
    ):
        self.message = message
        super().__init__(self.message)
