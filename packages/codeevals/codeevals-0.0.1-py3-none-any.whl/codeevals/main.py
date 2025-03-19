from typing import List

from codeevals.core import Evaluate
from codeevals.metrics.logic_relevancy import LogicRelevancy
from codeevals.inputs.llm_input import LLMInput
from codeevals.results.base_result import BaseResult

code_relevancy = LogicRelevancy()
evals = Evaluate(metrics=[code_relevancy], model="self-hosted/meta-llama/Llama-3.1-8B-Instruct",
                 base_url="https://aowhep684s539n-8003.proxy.runpod.net/v1")

input_1 = LLMInput(ground_truth = "def sum(a,b):\n\treturn a+b",
                   actual_response = "def summation(number_1,number_2):\n\tif number_1 is not 0 and number_2 is not 0:\n\treturn number_1+number_2")

results: List[BaseResult] = evals.evaluate(llm_input=[input_1])
for result in results:
    print(f"score: {result.score}, reason: {result.reason}")
