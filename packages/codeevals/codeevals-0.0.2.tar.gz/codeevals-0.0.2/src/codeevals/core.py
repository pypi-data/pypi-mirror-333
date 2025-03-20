from typing import List

from codeevals.inputs.llm_input import LLMInput
from codeevals.metrics.base_metrics import BaseMetric
from codeevals.metrics.logic_relevancy import LogicRelevancy
from codeevals.metrics.syntax_relevancy import SyntaxRelevancy
from codeevals.models.custom_model import CustomModel
from codeevals.models.base_model import BaseModel
from codeevals.results.evaluation_result import EvaluationResult


class Evaluate:
    def __init__(self, metrics: List[BaseMetric], model: str, base_url: str):
        self.metrics = metrics
        self.base_url: str = base_url
        self.model: BaseModel = self._initialize_model(model=model)
        self.eval_results = EvaluationResult()

    def evaluate(self, llm_input: List[LLMInput]):
        for metric in self.metrics:
            if isinstance(metric, LogicRelevancy):
                metric.model = self.model
                metric.compute(llm_inputs=llm_input, eval_results=self.eval_results)
            if isinstance(metric, SyntaxRelevancy):
                metric.model = self.model
                metric.compute(llm_inputs=llm_input, eval_results=self.eval_results)
        return self.eval_results


    def _initialize_model(self, model: str):
        if model is not None or model != "":
            model_details = model.split("/")
            model_name = "/".join(model.split("/")[1:])
            if model_details[0] == "self-hosted":
                _model = CustomModel(model_name=model_name, base_url=self.base_url)
                return _model
            else:
                raise NotImplementedError("Other LLM implementations under development")

