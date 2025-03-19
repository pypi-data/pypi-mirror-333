from abc import abstractmethod
from typing import Optional


class BaseModel:
    model_name: str
    base_url: str

    @abstractmethod
    def load_model(self):
        """Loads a model, that will be responsible for evaluating & scoring.

        Returns:
            A model object
        """
        raise NotImplementedError