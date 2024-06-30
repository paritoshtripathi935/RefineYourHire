class LLMApiClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_response(self, prompt):
        raise NotImplementedError   