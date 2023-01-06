import json
from surge.api_resource import QUESTIONS_ENDPOINT, APIResource


class Question(APIResource):
    def __init__(self, id, text, type_=None, required=True, column_header=None):
        self.id = id
        self.text = text
        self.type = type_
        self.required = required
        self.column_header = column_header

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_params(cls, q):
        if q["type"] == "free_response":
            return FreeResponseQuestion(
                    q["text"],
                    id=q["id"],
                    required=q["required"],
                    preexisting_annotations=q["preexisting_annotations"])
        elif q["type"] == "multiple_choice":
            return MultipleChoiceQuestion(
                    q["text"],
                    id=q["id"],
                    options=q["options"],
                    required=q["required"],
                    preexisting_annotations=q["preexisting_annotations"],
                    require_tiebreaker=q["require_tie_breaker"])

        elif q["type"] == "checkbox":
            return CheckboxQuestion(q["text"],
                                 id=q["id"],
                                 options=q["options"],
                                 required=q["required"],
                                 preexisting_annotations=q["preexisting_annotations"],
                                 require_tiebreaker=q["require_tie_breaker"])
        elif q["type"] == "text_tagging":
            return TextTaggingQuestion(
                    q["text"],
                    id=q["id"],
                    required=q["required"],
                    options=q["options"],
                    preexisting_annotations=q["preexisting_annotations"],
                    token_granularity=q["ner_token_granularity"],
                    allow_relationship_tags=q["ner_allow_relationship_tags"],
                    allow_overlapping_tags=q["ner_allow_overlapping_tags"],
                    require_tiebreaker=q["require_tie_breaker"])

        elif q["type"] == "tree_selection":
            return TreeSelectionQuestion(
                    q["text"],
                    id=q["id"],
                    options=q["options"],
                    required=q["required"],
                    preexisting_annotations=q["preexisting_annotations"],
                    require_tiebreaker=q["require_tie_breaker"])
        elif q["type"] == "ranking":
            return RankingQuestion(
                    q["text"],
                    id=q["id"],
                    options=q["options"],
                    required=q["required"],
                    preexisting_annotations=q["preexisting_annotations"],
                    allow_ranking_ties=q["allow_ranking_ties"])
        elif q["type"] == "file_upload":
            return FileUpload(q["text"],
                           id=q["id"],
                           required=q["required"])
        elif q["type"] == "text":
            return TextArea(q["text"], id=q["id"])
        elif q["type"] == "chat":
            return ChatBot(
                    q["text"],
                    id=q["id"],
                    options=q["options"],
                    endpoint_url=q["endpoint_url"],
                    endpoint_headers=q["endpoint_headers"],
                    preexisting_annotations=q["preexisting_annotations"])

    def update(self,
               text: str = None,
               hidden_by_item_option_id: str = None,
               shown_by_item_option_id: str = None):
        params = {}

        if text is not None:
            params["text"] = text
        if hidden_by_item_option_id is not None:
            params["hidden_by_item_option_id"] = hidden_by_item_option_id
        if shown_by_item_option_id is not None:
            params["shown_by_item_option_id"] = shown_by_item_option_id

        endpoint = f"{QUESTIONS_ENDPOINT}/{self.id}"
        response_json = self.put(endpoint, params)
        return Question.from_params(response_json)


class FreeResponseQuestion(Question):
    def __init__(self, text, id=None, required=True, preexisting_annotations=None, use_for_serial_collection=False, column_header=None):
        '''
        Create a free response question.

        Args:
            text (string): Required. The instructions above the free text box, e.g. "Please explain your reasoning".
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate text box an option specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            use_for_serial_collection (boolean): Deprecated in favor of carousel. The free response question will not be shown to the user,
                but will rather be used to collect the responses to a number of other items as a JSON string.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="free_response", required=required, column_header=column_header)
        self.preexisting_annotations = preexisting_annotations
        self.use_for_serial_collection = use_for_serial_collection


class MultipleChoiceQuestion(Question):
    def __init__(
            self,
            text,
            id=None,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False,
            column_header=None):
        '''
        Create a multiple choice radio question.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Is the sentiment of this text positive or negative?"
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            options (list of strings): Required. A list of the options for the radios, e.g. ["Yes", "No"].
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the radio selection with an option specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="multiple_choice", required=required, column_header=column_header)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class CheckboxQuestion(Question):
    def __init__(
            self,
            text,
            id=None,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False,
            column_header=None):
        '''
        Create a checkbox question. Unlike a multiple choice question, it's possible to select multiple checkboxes.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Check all the apply."
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            options (list of strings): Required. A list of the options for the checkboxes.
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the checkboxes with an options specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="checkbox", required=required, column_header=column_header)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class TextTaggingQuestion(Question):
    def __init__(
            self,
            text,
            id=None,
            options=[],
            required=True,
            preexisting_annotations=None,
            token_granularity=True,
            allow_relationship_tags=False,
            allow_overlapping_tags=False,
            require_tiebreaker=False,
            column_header=None):
        '''
        Create a text tagging (NER) question. Unlikely a multiple choice question, it's possible to select multiple checkboxes

        Args:
            text (string): Required. The text that needs to be tagged.
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            required (boolean): If true, worker must tag at least element.
            options (list of strings): Required. A list of tags that can be used to tag spans of text, e.g. ["Person", "Place"].
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the named entity tagger. This must contain serialized JSON data
                in the same format outputted by the text tagging tool.
            token_granularity (boolean): If set to true, spans will snap to the nearest word to prevent workers from accidentally tagging parts of words.
            allow_relationship_tags (boolean): If true, enable relationship tagging.
            allow_overlapping_tags (boolean): If true, allow multiple tags to be assigned to the same span of text.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                Workers must have the exact same set of tags to be considered in agreement.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="text_tagging", required=required, column_header=column_header)
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
            id=None,
            options=[],
            descriptions=[],
            required=True,
            preexisting_annotations=None,
            require_tiebreaker=False,
            column_header=None):
        '''
        Create a hierarchical multiple choice question. This is useful if you have a lot of options in a nested format.

        Args:
            text (string): Required. The text of the question being asked, e.g. "Which category does this example belong to?"
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            options (list of strings): Required. A list of the options for the tree. Each level of hierarchy should be separate by a " / ".
                For example, one valid set of options would be ["1A / 2A", "1A / 2B", "1B / 2C", "1B / 2D"].
            descriptions(list of strings): Tooltip text for the options. This should have the same length as the options.
                You can substitute in empty strings if one option doesn't have a tooltip.
            required (boolean): Defaults to true. Whether or not workers must fill out this question before moving on to the next task.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the radio selection with an option specified in the task data.
                The preexisting_annotations param should contain the task data key you are loading the default values from.
            require_tiebreaker (boolean): If set to true, more workers will be assigned to this task if fewer than 50% agree on an answer.
                For example, imagine you are using two workers per task. If one selects Option A and the second one selections Option B a third will be assigned to the task to break the tie.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="tree_selection", required=required, column_header=column_header)
        self.options = options
        self.descriptions = descriptions
        self.preexisting_annotations = preexisting_annotations
        self.require_tiebreaker = require_tiebreaker


class FileUpload(Question):
    def __init__(self, text, id=None, required=False, column_header=None):
        '''
        Add a file upload widget where workers can upload images, documents, or other files.

        Args:
            text (string): This text will appear above the file upload and can be used to specify any instructions.
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            required (boolean): If true, Surgers will be required to upload a file before moving on to the next task.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="file_upload", required=required, column_header=column_header)


class RankingQuestion(Question):
    def __init__(
            self,
            text,
            id=None,
            options=[],
            required=False,
            preexisting_annotations=None,
            allow_ranking_ties=False,
            column_header=None):
        '''
        Create a ranking widget. Workers can drag and drop the option to specify their ranking.

        Args:
            required (boolean): If true, worker must rank at least one element.
            text (string): Required. The text of the question being asked, e.g. "Please rank these search results from best to worst"
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            options (list of strings): Required. A list of the options being ranked.
            preexisting_annotations (string): You can use preexisting annotations to prepopulate the named entity tagger.
                This must contain serialized data in the same format outputted by the ranking tool.
            allow_ranking_ties (boolean): Optional. Whether or not to allow ties in the ranking. If ties are allowed, two options can be ranked in the same group.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="ranking", required=required, column_header=column_header)
        self.options = options
        self.allow_ranking_ties = allow_ranking_ties


class ChatBot(Question):
    def __init__(
            self,
            text,
            id=None,
            options=[],
            endpoint_url=None,
            endpoint_headers=None,
            preexisting_annotations=None,
            required=False,
            column_header=None):
        '''
        Create an interactive chatbot on the labeling page. This is an advanced item type.

        Args:
            text (string): This text will appear above the chatbot and can be used to specify any instructions.
            id (string): The UUID of this question, if it has been created. Otherwise, it will be None.
            options (list of strings): Options for rating chatbot responses.
            endpoint_url (string): A URL to send chat responses to. It must include a "text" field in its response.
            endpoint_headers (string): Please provide a JSON string with any headers that need to be set when calling this URL.
            column_header (string): This value will be used as the column header for the results table on the Surge AI site and in results CSV and JSON files.
        '''
        super().__init__(id, text, type_="chat", required=required, column_header=column_header)
        self.options = options
        self.endpoint_url = endpoint_url
        self.endpoint_headers = endpoint_headers
        self.preexisting_annotations=preexisting_annotations


class TextArea(Question):
    def __init__(self, text, id=None):
        super().__init__(id, text, type_="text", required=False)
