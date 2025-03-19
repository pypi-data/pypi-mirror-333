from dataclasses import dataclass


@dataclass
class LLMInput:
    ground_truth: str
    actual_response: str