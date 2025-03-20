from typing import List

from codeevals.core import Evaluate
from codeevals.metrics.logic_relevancy import LogicRelevancy
from codeevals.inputs.llm_input import LLMInput
from codeevals.metrics.syntax_relevancy import SyntaxRelevancy
from codeevals.results.base_result import BaseResult

code_relevancy = LogicRelevancy()
syntax_relevancy = SyntaxRelevancy()

evals = Evaluate(metrics=[code_relevancy, syntax_relevancy], model="self-hosted/meta-llama/Meta-Llama-3.1-8B-Instruct",
                 base_url="https://9styblyjb29d54-8003.proxy.runpod.net/v1")

input_1 = LLMInput(ground_truth = "def sum(a,b):\n\treturn a+b",
                   actual_response = "def summation(number_1,number_2):\n\tif number_1 is not 0 and number_2 is not 0:\n\t\treturn number_1+number_2")

results: List[BaseResult] = evals.evaluate(llm_input=[input_1])
for result in results.results:
    print(f"eval: {result.eval_name}, score: {result.score}, reason: {result.reason}")


