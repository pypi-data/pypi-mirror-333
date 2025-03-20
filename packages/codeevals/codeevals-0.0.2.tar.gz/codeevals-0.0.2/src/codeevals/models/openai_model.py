from abc import ABC

from codeevals.models.base_model import BaseModel


class OpenAIModel(BaseModel, ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def load_model(self):
        """
        load openai model from the list of valid models and return the model object
        :return: model_object
        """
        pass
