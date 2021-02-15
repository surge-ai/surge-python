class SurgeRequestError(Exception):
    """Raise for exceptions that occur during authentication"""
    def __init__(self, message="Something went wrong with the API request."):
        self.message = message
        super().__init__(self.message)


class SurgeProjectQuestionError(Exception):
    """Raise for exceptions that occur when adding Questions to a new Project"""
    def __init__(self, message="All questions added to new Project must be of type Question."):
        self.message = message
        super().__init__(self.message)
