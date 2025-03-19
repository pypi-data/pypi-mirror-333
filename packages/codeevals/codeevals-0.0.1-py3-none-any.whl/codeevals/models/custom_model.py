import os
from abc import ABC
from openai import OpenAI
from codeevals.models.base_model import BaseModel


class CustomModel(BaseModel, ABC):
    def __init__(self, model_name: str, base_url: str):
        self.model_name = model_name
        self.base_url = base_url

    def load_model(self) -> OpenAI:
        """
        load self-hosted model and return the model object.
        supports any openai spec followed serving platform like vLLM etc.
        :return: model_object
        """
        #TODO: consider having an API_KEY for self-hosted models also.
        token = os.environ.get("API_KEY") or "token-abc123"
        client = OpenAI(base_url=self.base_url, api_key=token)
        return client
