class SurgeRequestError(Exception):
    """Catch-all exception for errors that occur during request"""
    def __init__(self, message="Something went wrong with the API request."):
        self.message = message
        super().__init__(self.message)


class SurgeMissingAPIKeyError(Exception):
    """Raise when user has not set their API key"""
    def __init__(self, message="Surge API key has not been set."):
        self.message = message
        super().__init__(self.message)


class SurgeMissingIDError(Exception):
    """Raise for exceptions that occur during authentication"""
    def __init__(self, message="Must be initialized with an id."):
        self.message = message
        super().__init__(self.message)


class SurgeProjectQuestionError(Exception):
    """Raise for exceptions that occur when adding Questions to a new Project"""
    def __init__(
            self,
            message="All questions added to a Project must be of type Question."
    ):
        self.message = message
        super().__init__(self.message)
