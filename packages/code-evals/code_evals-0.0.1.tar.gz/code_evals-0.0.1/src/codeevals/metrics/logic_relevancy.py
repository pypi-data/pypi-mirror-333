import json
from abc import ABC

from typing import List, Any

from codeevals.inputs.llm_input import LLMInput
from codeevals.metrics.base_metrics import BaseMetric
from codeevals.models.custom_model import CustomModel
from codeevals.results.code_relevancy_result import CodeRelevancyResult
from codeevals.results.evaluation_result import EvaluationResult
from codeevals.templates.code_relevancy_template import CodeRelevancyTemplate


class LogicRelevancy(BaseMetric, ABC):
    def __init__(self, threshold: float = 0.5, include_reason: bool = True, verbose_mode: bool = False,
                 strict_mode: bool = False):
        self.model = None
        self.threshold = 1 if strict_mode else threshold
        self.verbose_mode = verbose_mode
        self.include_reason = include_reason
        self.eval_results = EvaluationResult()

    def compute(self, llm_inputs: List[LLMInput], *args, **kwargs) -> Any:
        for llm_input in llm_inputs:
            _template = CodeRelevancyTemplate.generate_code_relevancy_percentage_template(ground_truth_code=llm_input.ground_truth,
                                                                              llm_generated_code=llm_input.actual_response)
            if self.model is not None and isinstance(self.model, CustomModel):
                response = self.model.load_model().chat.completions.create(
                    model=self.model.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": _template,
                        },
                    ],
                    temperature=0.2
                )
                if response.choices is not None and len(response.choices) > 0:
                    resp = json.loads(response.choices[0].message.content)
                    code_relevancy_result = CodeRelevancyResult(score=resp["match_percentage"], reason=resp["reason"])
                    self.eval_results.push(llm_result=code_relevancy_result)
            else:
                raise Exception("model cannot be None")

        return self.eval_results.show()