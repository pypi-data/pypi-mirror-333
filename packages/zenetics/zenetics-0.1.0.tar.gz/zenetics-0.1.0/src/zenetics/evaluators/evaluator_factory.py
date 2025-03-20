from enum import Enum
from typing import Dict, Type, Optional
from zenetics.evaluators.answer_relevance.answer_relevance import (
    AnswerRelevanceEvaluator,
)
from zenetics.evaluators.base import BaseEvaluator, EvaluatorCreateError, EvaluatorError
from zenetics.evaluators.context_relevance.context_relevance import (
    ContextualRelevanceEvaluator,
)
from zenetics.evaluators.groundedness.groundedness import GroundedNessEvaluator
from zenetics.evaluators.mock.mock import MockEvaluator
from zenetics.evaluators.reference.reference import ReferenceEvaluator
from zenetics.llm.llm_client import LLMClient
from zenetics.models.evaluator import EvaluatorAssignment


class EvaluatorType(Enum):
    """Supported evaluator types"""

    MOCK = "mock"
    REFERENCE = "reference_evaluator"
    ANSWER_RELEVANCE = "answer_relevance"
    CONTEXTUAL_RELEVANCE = "contextual_relevance"
    GROUNDEDNESS = "groundedness"
    FACTUAL_CONSISTENCY = "factual_consistency"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    # Add more evaluator types as needed


class EvaluatorFactory:
    """Factory for creating evaluator instances"""

    @classmethod
    def create_evaluator(
        cls, evaluator_spec: EvaluatorAssignment, llm_client: LLMClient
    ) -> BaseEvaluator:
        """
        Create an evaluator instance based on configuration.

        Args:
            config: Configuration for the evaluator
            llm_client: Optional LLM client for evaluators that need it

        Returns:
            Instance of BaseEvaluator

        Raises:
            EvaluatorError: If evaluator type is not supported or creation fails
        """
        threshold = evaluator_spec.threshold

        if evaluator_spec.evaluator.type == EvaluatorType.ANSWER_RELEVANCE.value:
            return AnswerRelevanceEvaluator(llm_client=llm_client, threshold=threshold)
        elif evaluator_spec.evaluator.type == EvaluatorType.CONTEXTUAL_RELEVANCE.value:
            return ContextualRelevanceEvaluator(
                llm_client=llm_client, threshold=threshold
            )
        elif evaluator_spec.evaluator.type == EvaluatorType.GROUNDEDNESS.value:
            return GroundedNessEvaluator(llm_client=llm_client, threshold=threshold)
        elif evaluator_spec.evaluator.type == EvaluatorType.REFERENCE.value:
            return ReferenceEvaluator(llm_client=llm_client, threshold=threshold)
        else:
            # TODO: remove this code after testing
            return MockEvaluator(llm_client=llm_client, threshold=threshold)
