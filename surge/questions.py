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
    def __init__(self, text, required=True):
        super().__init__(text, type_="free_response", required=required)


class MultipleChoiceQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True):
        super().__init__(text, type_="multiple_choice", required=required)
        self.options = options
        self.descriptions = descriptions

class CheckboxQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True):
        super().__init__(text, type_="checkbox", required=required)
        self.options = options
        self.descriptions = descriptions


class TextTaggingQuestion(Question):
    def __init__(self, text, options=[], required=True):
        super().__init__(text, type_="text_tagging", required=required)
        self.options = options

class TreeSelectionQuestion(Question):
    def __init__(self, text, options=[], descriptions=[], required=True):
        super().__init__(text, type_="tree_selection", required=required)
        self.options = options
        self.descriptions = descriptions

class TextArea(Question):
    def __init__(self, text):
        super().__init__(text, type_="text")
