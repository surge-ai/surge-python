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
    def __init__(
            self,
            text,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False):
        '''
        Create a multiple choice radio question.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Is the sentiment of this text positive or negative?"
            options (list of strings): Required. A list of the options for the radios, e.g. ["Yes", "No"].
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the radio selection with an option specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
        '''
        super().__init__(text, type_="multiple_choice", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class CheckboxQuestion(Question):
    def __init__(
            self,
            text,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False):
        '''
        Create a checkbox question. Unlike a multiple choice question, it's possible to select multiple checkboxes.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Check all the apply."
            options (list of strings): Required. A list of the options for the checkboxes.
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the checkboxes with an options specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
        '''
        super().__init__(text, type_="checkbox", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class TextTaggingQuestion(Question):
    def __init__(
            self,
            text,
            options=[],
            required=True,
            preexisting_annotations=None,
            token_granularity=True,
            allow_relationship_tags=False,
            allow_overlapping_tags=False,
            require_tiebreaker=False):
        '''
        Create a text tagging (NER) question. Unlikely a multiple choice question, it's possible to select multiple checkboxes

        Args:
            text (string): Required. The text that needs to be tagged.
            required (boolean): If true, worker must tag at least element.
            options (list of strings): Required. A list of tags that can be used to tag spans of text, e.g. ["Person", "Place"].
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the named entity tagger. This must contain serialized JSON data
                in the same format outputted by the text tagging tool.
            token_granularity (boolean): If set to true, spans will snap to the nearest word to prevent workers from accidentally tagging parts of words.
            allow_relationship_tags (boolean): If true, enable relationship tagging.
            allow_overlapping_tags (boolean): If true, allow multiple tags to be assigned to the same span of text.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                Workers must have the exact same set of tags to be considered in agreement.
        '''
        super().__init__(text, type_="text_tagging", required=False)
        self.options = options
        self.preexisting_annotations = preexisting_annotations
        self.token_granularity = token_granularity
        self.allow_relationship_tags = allow_relationship_tags
        self.allow_overlapping_tags = allow_overlapping_tags
        self.require_tiebreaker = require_tiebreaker


class TreeSelectionQuestion(Question):
    def __init__(
            self,
            text,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False):
        '''
        Create a hierarchical multiple choice question. This is useful if you have a lot of options in a nested format.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Which category does this example belong to?"
            options (list of strings): Required. A list of the options for the tree. Each level of hierarchy should be separate by a " / ".
                For example, one valid set of options would be ["1A / 2A", "1A / 2B", "1B / 2C", "1B / 2D"].
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the radio selection with an option specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
        '''
        super().__init__(text, type_="tree_selection", required=required)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class FileUpload(Question):
    def __init__(self, text, required=False):
        '''
        Add a file upload widget where workers can upload images, documents, or other files.

        Args:
            text (string): This text will appear above the file upload and can be used to specify any instructions.
        '''
        super().__init__(text, type_="file_upload", required=required)


class RankingQuestion(Question):
    def __init__(
            self,
            text,
            options=[],
            required=False,
            preexisting_annotations=None,
            allow_ranking_ties=False):
        '''
        Create a ranking widget. Workers can drag and drop the option to specify their ranking.

        Args:
            required (boolean): If true, worker must rank at least one element.
            text (string): Required. The text of the question being asked, e.g. "Please rank these search results from best to worst"
            options (list of strings): Required. A list of the options being ranked.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the named entity tagger.
                This must contain serialized data in the same format outputted by the ranking tool.
            allow_ranking_ties (boolean): Optional. Whether or not to allow ties in the ranking. If ties are allowed, two options can be ranked in the same group.
        '''
        super().__init__(text, type_="ranking", required=required)
        self.options = options
        self.allow_ranking_ties = allow_ranking_ties


class ChatBot(Question):
    def __init__(
            self,
            text,
            options=[],
            endpoint_url=None,
            endpoint_headers=None):
        '''
        Create an interactive chatbot on the labeling page. This is an advanced item type.

        Args:
            text (string): This text will appear above the chatbot and can be used to specify any instructions.
            options (list of strings): Options for rating chatbot responses.
            endpoint_url (string): A URL to send chat responses to. It must include a "text" field in its response.
            endpoint_headers (string): Please provide a JSON string with any headers that need to be set when calling this URL.
        '''
        super().__init__(text, type_="chat", required=False)
        self.options = options
        self.endpoint_url = endpoint_url
        self.endpoint_headers = endpoint_headers


class TextArea(Question):
    def __init__(self, text):
        super().__init__(text, type_="text")
