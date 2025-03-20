from zenetics.evaluators.base import BaseEvaluator, EvaluatorResult
from zenetics.llm.llm_client import LLMClient, TokenUsage
from zenetics.models.generation_data import Generation
from zenetics.models.test_case import TestCase
from zenetics.models.test_run import EvaluationResultState
import time


class MockEvaluator(BaseEvaluator):
    """
    Mock evaluator that always returns success.
    Useful for testing and development.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        threshold: float,
        fixed_score: float = 0.95,
        simulated_delay: float = 0.1,
    ):
        """
        Initialize mock evaluator.
        """
        self.llm_client = llm_client
        self.threshold = threshold
        self.fixed_score = fixed_score
        self.simulated_delay = simulated_delay
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
        """
        Run mock evaluation.
        Always returns success with fixed score.

        Args:
            test_case: Test case (not used)

        Returns:
            EvaluatorResult with successful evaluation
        """
        # Simulate processing time
        start_time = time.time()
        if self.simulated_delay > 0:
            time.sleep(self.simulated_delay)

        # Create mock score breakdown
        score_breakdown = (
            {
                "primary_score": self.fixed_score,
                "sub_scores": {"metric1": 0.96, "metric2": 0.94, "metric3": 0.95},
            }
            if self.verbose_mode
            else None
        )

        # Create mock verbose logs
        verbose_logs = (
            """
Evaluation Details:
- Primary evaluation completed successfully
- All checks passed
- No issues detected
""".strip()
            if self.verbose_mode
            else None
        )

        # Create result
        self.result = EvaluatorResult(
            threshold=self.threshold,
            score=self.fixed_score,
            reason="Mock evaluation completed successfully. All criteria met."
            if self.include_reason
            else "",
            state=EvaluationResultState.PASSED,
            cost=0.0,
            duration=(time.time() - start_time) * 1000,
            tokens=TokenUsage(
                input_tokens=100,  # Mock token counts
                completion_tokens=50,
                total_tokens=150,
            ),
            score_breakdown=score_breakdown,
            verbose_logs=verbose_logs,
        )

        return self.result

    def is_completed(self) -> bool:
        """
        Check if evaluation is completed.
        Always returns True after run is called.
        """
        return self.result is not None or self.error is not None or self.skipped

    def is_successful(self) -> bool:
        """
        Check if evaluation was successful.
        Always returns True after run is called.
        """
        return (
            self.result is not None
            and self.result.state == EvaluationResultState.SUCCESS
        )

    @property
    def name(self) -> str:
        return "Mock Evaluator"
