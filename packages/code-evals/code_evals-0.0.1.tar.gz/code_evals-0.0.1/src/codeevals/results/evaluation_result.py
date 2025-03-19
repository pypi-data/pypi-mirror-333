from typing import List

from codeevals.results.base_result import BaseResult


class EvaluationResult:
    def __init__(self):
        self.results: List[BaseResult] = []

    def push(self, llm_result: BaseResult) -> None:
        self.results.append(llm_result)

    def show(self) -> List[BaseResult]:
        return self.results