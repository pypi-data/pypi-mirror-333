from abc import ABC

from codeevals.results.base_result import BaseResult


class CodeRelevancyResult(BaseResult, ABC):
    def __init__(self, score: str, reason: str):
        self.score = score
        self.reason = reason