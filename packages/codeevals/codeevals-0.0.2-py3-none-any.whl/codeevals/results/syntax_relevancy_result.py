from abc import ABC

from codeevals.results.base_result import BaseResult


class SyntaxRelevancyResult(BaseResult, ABC):
    def __init__(self, score: str, reason: str):
        self.score = score
        self.reason = reason
        self.eval_name = "Syntax Relevancy"