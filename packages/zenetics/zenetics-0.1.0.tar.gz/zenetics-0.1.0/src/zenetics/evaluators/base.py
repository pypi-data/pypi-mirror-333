from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional

from zenetics.llm.llm_client import TokenUsage
from zenetics.models.generation_data import Generation
from zenetics.models.test_case import TestCase
from zenetics.models.test_run import EvaluationResultState


class EvaluatorError(Exception):
    """
    Base class for all evaluator related errors
    """

    def __init__(self, message):
        self.message = message


class EvaluatorCreateError(EvaluatorError):
    """
    Error raised when evaluator creation fails
    """

    def __init__(self, message):
        super().__init__(message)


@dataclass
class EvaluatorResult:
    """
    Result of an evaluation
    """

    threshold: float
    score: float
    reason: str
    state: EvaluationResultState
    duration: float
    cost: float
    tokens: TokenUsage
    score_breakdown: Optional[Dict] = None
    verbose_logs: Optional[str] = None


class BaseEvaluator(ABC):
    threshold: float
    strict_mode: bool = False
    async_mode: bool = True
    verbose_mode: bool = True
    include_reason: bool = False
    error: Optional[str] = None
    skipped = False
    result: Optional[EvaluatorResult] = None

    @abstractmethod
    def run(
        self, actual_output: Generation, test_case: TestCase, *args, **kwargs
    ) -> EvaluatorResult:
        raise NotImplementedError

    @abstractmethod
    def is_completed(self) -> bool:
        """
        Check if the evaluation is completed. This will return true in case of
        successful or failed evaluation.
        """
        raise NotImplementedError

    @abstractmethod
    def is_successful(self) -> bool:
        """
        Check if the evaluation is successful. This will return true only if the
        evaluation is successful. It returns false in case the evaluation is
        not completed or has failed.
        """
        raise NotImplementedError

    @property
    def __name__(self):
        return "Base Evaluator"
