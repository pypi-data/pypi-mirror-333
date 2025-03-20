import time
from zenetics.evaluators.base import BaseEvaluator, EvaluatorError, EvaluatorResult
from zenetics.llm.llm_client import LLMClient, TokenUsage
from zenetics.models.generation_data import Generation
from zenetics.models.test_case import TestCase

from deepeval.metrics import ContextualRelevancyMetric, BaseMetric
from deepeval.test_case import LLMTestCase

from zenetics.models.test_run import EvaluationResultState
from zenetics.utils.convert_result import convertResult


class ContextualRelevanceEvaluator(BaseEvaluator):
    """
    TODO
    """

    def __init__(self, llm_client: LLMClient, threshold: float):
        """
        Initialize the reference evaluator.

        Args:
            llm_client: LLM client for generating evaluations
            threshold: Minimum score threshold for success
        """
        self.llm_client = llm_client
        self.threshold = threshold
        self.result = None
        self.error = None
        self.skipped = False
        self.strict_mode = False
        self.async_mode = True
        self.verbose_mode = True
        self.include_reason = True

    def run(
        self, actual_output: Generation, test_case: TestCase, *args, **kwargs
    ) -> EvaluatorResult:
        # For demonstration purposes, this method is currently implemented using the DeepEval library.
        contextual_relevancy_metric = ContextualRelevancyMetric(
            threshold=self.threshold, async_mode=False, verbose_mode=False
        )
        try:
            de_test_case = LLMTestCase(
                input=test_case.data.input,
                actual_output=actual_output.output,
                retrieval_context=actual_output.retrieval_context,
            )

            start_time = time.time()
            contextual_relevancy_metric.measure(
                test_case=de_test_case, _show_indicator=False
            )
            duration = (time.time() - start_time) * 1000
            res = convertResult(
                metric=contextual_relevancy_metric,
                duration=duration,
                tokens=TokenUsage(0, 0, 0),
            )
            return res
        except Exception as e:
            msg = str(e)
            print(f"Error: Contextual Relevance evaluation failed: {msg}")
            self.error = f"Contextual Relevance evaluation failed: {msg}"
            raise EvaluatorError(self.error)

    def is_completed(self) -> bool:
        """Check if evaluation is completed"""
        return self.result is not None or self.error is not None or self.skipped

    def is_successful(self):
        """Check if evaluation was successful"""
        if not self.is_completed():
            return False
        if self.error is not None:
            return False
        if self.skipped:
            return True
        return (
            self.result is not None
            and self.result.state == EvaluationResultState.PASSED
        )

    @property
    def name(self) -> str:
        return "Answer Relevance Evaluator"
