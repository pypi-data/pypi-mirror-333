from abc import abstractmethod
from typing import Optional, Dict

from codeevals.inputs.llm_input import LLMInput
from codeevals.models.base_model import BaseModel


class BaseMetric:
    threshold: float
    score: Optional[float] = None
    reason: Optional[str] = None
    success: Optional[bool] = None
    verbose_mode: bool = True
    strict_mode: bool = False
    include_reason: bool = False
    error: Optional[str] = None
    model = Optional[BaseModel]

    @abstractmethod
    def compute(self, llm_input: LLMInput, *args, **kwargs) -> float:
        raise NotImplementedError