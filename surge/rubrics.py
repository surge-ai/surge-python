from surge.api_resource import APIResource


class Rubric(APIResource):

    @classmethod
    def evaluate(
        cls,
        text_for_grading: str,
        rubric_text: str,
        prompt: str = None,
        api_key: str = None,
    ):
        """
        Evaluate text against a rubric using AI grading.

        Arguments:
            text_for_grading (str): The text content to be graded.
            rubric_text (str): The rubric or criteria to evaluate against.
            prompt (str, optional): Additional instructions for how to grade the text.
            api_key (str, optional): API key to use for this request.

        Returns:
            dict: A dictionary containing:
                - answer (bool): Whether the text meets the rubric criteria.
                - explanation (str): An explanation of the grading decision.
        """
        endpoint = "evaluate_rubric"
        params = {
            "text_for_grading": text_for_grading,
            "rubric_text": rubric_text,
        }
        if prompt is not None:
            params["prompt"] = prompt

        response_json = cls.post(endpoint, params, api_key=api_key)
        return response_json
