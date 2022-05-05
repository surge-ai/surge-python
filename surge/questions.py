import json


class Question(object):
    def __init__(self, text, type_=None, required=True):
        self.text = text
        self.type = type_
        self.required = required

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())


class FreeResponseQuestion(Question):
    def __init__(self, text, required=True, preexisting_annotations=None):
        super().__init__(text, type_="free_response", required=required)
        self.preexisting_annotations = preexisting_annotations


class MultipleChoiceQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True, preexisting_annotations=None, require_tiebreaker=False):
        super().__init__(text, type_="multiple_choice", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker

class CheckboxQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True, preexisting_annotations=None, require_tiebreaker=False):
        super().__init__(text, type_="checkbox", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class TextTaggingQuestion(Question):
    def __init__(self, text, options=[], preexisting_annotations=None, token_granularity=True, allow_relationship_tags=False, allow_overlapping_tags=False):
        super().__init__(text, type_="text_tagging", required=False)
        self.options = options
        self.preexisting_annotations = preexisting_annotations
        self.token_granularity = token_granularity
        self.allow_relationship_tags = allow_relationship_tags
        self.allow_overlapping_tags = allow_overlapping_tags

class TreeSelectionQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True, preexisting_annotations=None):
        super().__init__(text, type_="tree_selection", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations

class RankingQuestion(Question):
    def __init__(self, text, options=[]):
        super().__init__(text, type_="ranking", required=False)
        self.options = options

class FileUpload(Question):
    def __init__(self, text):
        """
            Add a file upload widget where workers can upload images, documents, or other files.

            Args:
                text (string): This text will appear above the file upload and can be used to specify any instructions.
        """
        super().__init__(text, type_="file_upload", required=False)

class ChatBot(Question):
    def __init__(self, text, options=[], endpoint_url=None, endpoint_headers=None):
        super().__init__(text, type_="chat", required=False)
        self.options = options
        self.endpoint_url = endpoint_url
        self.endpoint_headers = endpoint_headers

class TextArea(Question):
    def __init__(self, text):
        super().__init__(text, type_="text")
