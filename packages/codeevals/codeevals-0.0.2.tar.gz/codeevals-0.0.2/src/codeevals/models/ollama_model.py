from abc import ABC

from codeevals.models.base_model import BaseModel


class OllamaModel(BaseModel, ABC):
    def __init__(self, model_name: str, base_url: str):
        self.model_name = model_name
        self.base_url = base_url

    def load_model(self):
        """
        load ollama open source model and return the model object
        :return: model_object
        """
        pass
