from pydantic import BaseModel, Field, field_validator
from zenetics.evaluators.base import BaseEvaluator, EvaluatorResult, EvaluatorError
from zenetics.llm.llm_client import LLMClient, LLMResponse, TokenUsage
from zenetics.models.generation_data import Generation
from zenetics.models.test_case import TestCase
from zenetics.models.test_run import EvaluationResultState
from zenetics.utils.validate_json import validate_json
from .template import ReferenceTemplate
import json
import time
from typing import Any, List, Optional, Dict


# Define the expected response structure using Pydantic
class ContentSimilarityScores(BaseModel):
    information_completeness: float = Field(..., ge=0.0, le=1.0)
    factual_accuracy: float = Field(..., ge=0.0, le=1.0)
    contextual_relevance: float = Field(..., ge=0.0, le=1.0)
    logical_flow: float = Field(..., ge=0.0, le=1.0)


class ContentSimilarityAnalysis(BaseModel):
    matching_points: List[str]
    missing_points: List[str]
    incorrect_points: List[str]


class ContentSimilarityResult(BaseModel):
    scores: ContentSimilarityScores
    analysis: ContentSimilarityAnalysis
    overall_score: float = Field(..., ge=0.0, le=1.0)
    explanation: str


class StructuralScores(BaseModel):
    """Schema for individual structural evaluation scores."""

    required_sections: float = Field(..., ge=0.0, le=1.0)
    format_compliance: float = Field(..., ge=0.0, le=1.0)
    hierarchical_organization: float = Field(..., ge=0.0, le=1.0)
    formatting_consistency: float = Field(..., ge=0.0, le=1.0)


class StructuralSimilarityResult(BaseModel):
    """Schema for enhanced structural similarity evaluation results."""

    detected_format: str = Field(
        ..., description="Identified primary format of the reference output"
    )

    structural_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall structural similarity score between 0.0 and 1.0",
    )

    scores: StructuralScores = Field(
        ..., description="Detailed scores for each structural evaluation criterion"
    )

    missing_elements: List[str] = Field(
        ..., description="List of structural elements missing from the generated output"
    )

    format_issues: List[str] = Field(
        ..., description="List of issues related to formatting or invalid output types"
    )

    explanation: str = Field(
        ..., description="Detailed explanation of the structural similarity evaluation"
    )

    @field_validator("structural_score")
    @classmethod
    def validate_score_with_format_issues(cls, v: float, info: Any) -> float:
        """Validate that if format_issues exist, the score should be appropriately low."""
        format_issues = info.data.get("format_issues", [])
        if format_issues and v > 0.3:
            raise ValueError(
                "If format_issues exist, structural_score should not exceed 0.3"
            )
        return v

    @field_validator("missing_elements")
    @classmethod
    def validate_empty_list_if_perfect_score(cls, v: List[str], info: Any) -> List[str]:
        """Validate that missing_elements is empty if score is 1.0."""
        structural_score = info.data.get("structural_score")
        if structural_score == 1.0 and v:
            raise ValueError(
                "If structural_score is 1.0, missing_elements must be empty"
            )
        return v


class ReferenceEvaluator(BaseEvaluator):
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
        """
        Run the reference evaluation.

        Args:
            test_case: Test case containing reference and actual output

        Returns:
            EvaluatorResult containing the evaluation results

        Raises:
            EvaluatorError: If evaluation fails
        """
        try:
            start_time = time.time()

            # Track token usage
            total_input_tokens = 0
            total_completion_tokens = 0
            total_cost = 0.0

            # evaluation results
            content_result = None
            structure_result = None

            try:
                # Content similarity evaluation
                content_prompt = ReferenceTemplate.content_similarity(
                    test_case.data.reference_output, actual_output.output
                )

                llm_options = {
                    "model": self.llm_client.get_default_model(),
                    "max_tokens": 1000,
                    "temperature": 0.1,
                }

                content_response: LLMResponse = self.llm_client.generate(
                    prompt=content_prompt, llm_options=llm_options
                )
                json_res = validate_json(content_response.completion)
                content_result = ContentSimilarityResult(**json_res)
                total_input_tokens += content_response.tokens.input_tokens
                total_completion_tokens += content_response.tokens.completion_tokens
                content_cost = self.llm_client.calculate_cost(
                    content_response.tokens, llm_options["model"]
                )
            except Exception as e:
                msg = str(e)
                self.error = f"Reference evaluation (content similarity) failed: {msg}"
                raise EvaluatorError(self.error)

            try:
                # Structural comparison
                structure_prompt = ReferenceTemplate.structural_comparison(
                    reference_output=test_case.data.reference_output,
                    generated_output=actual_output.output,
                )

                structure_response = self.llm_client.generate(
                    prompt=structure_prompt, llm_options=llm_options
                )

                json_res = validate_json(structure_response.completion)
                structure_result = StructuralSimilarityResult(**json_res)
                total_input_tokens += structure_response.tokens.input_tokens
                total_completion_tokens += structure_response.tokens.completion_tokens
                total_cost = content_cost + self.llm_client.calculate_cost(
                    structure_response.tokens, llm_options["model"]
                )
            except Exception as e:
                msg = str(e)
                self.error = (
                    f"Reference evaluation (structural comparison) failed: {msg}"
                )
                raise EvaluatorError(self.error)

            # Calculate overall score
            content_score = content_result.overall_score
            structure_score = structure_result.structural_score
            overall_score = (content_score * 0.7) + (structure_score * 0.3)

            # Generate detailed breakdown
            score_breakdown = {
                "content_evaluation": {
                    "total_score": content_score,
                    "weights": {
                        "information_completeness": 0.4,
                        "factual_accuracy": 0.3,
                        "contextual_relevance": 0.2,
                        "logical_flow": 0.1,
                    },
                    "subscores": content_result.scores.model_dump(),
                },
                "structural_evaluation": {
                    "total_score": structure_score,
                    "detected_format": structure_result.detected_format,
                    "weights": {
                        "required_sections": 0.35,
                        "format_compliance": 0.25,
                        "hierarchical_organization": 0.20,
                        "formatting_consistency": 0.20,
                    },
                    "subscores": structure_result.scores.model_dump(),
                    "analysis": {
                        "missing_elements": structure_result.missing_elements,
                        "format_issues": structure_result.format_issues,
                    },
                },
            }

            # Generate comprehensive reason
            reason = (
                self._generate_reason(content_result, structure_result, overall_score)
                if self.include_reason
                else ""
            )

            # Calculate duration
            duration = (time.time() - start_time) * 1000

            # Create and store result
            self.result = EvaluatorResult(
                threshold=self.threshold,
                score=overall_score,
                reason=reason,
                state=EvaluationResultState.PASSED
                if overall_score >= self.threshold
                else EvaluationResultState.FAILED,
                duration=duration,
                cost=total_cost,
                tokens=TokenUsage(
                    input_tokens=total_input_tokens,
                    completion_tokens=total_completion_tokens,
                    total_tokens=total_input_tokens + total_completion_tokens,
                ),
                score_breakdown=score_breakdown,
                verbose_logs=self._generate_verbose_logs(
                    content_result, structure_result
                ),
            )
            return self.result

        except Exception as e:
            self.error = str(e)
            raise EvaluatorError(f"Reference evaluation failed: {str(e)}")

    def _generate_reason(
        self,
        content_result: ContentSimilarityResult,
        structure_result: StructuralSimilarityResult,
        overall_score: float,
    ) -> str:
        """Generate detailed reason for the evaluation result"""
        content_analysis = content_result.explanation
        structure_analysis = structure_result.explanation

        reason_parts = [
            f"Overall Score: {overall_score:.2f}",
            f"Content Score: {content_result.overall_score:.2f}",
            "Content Analysis:",
            content_analysis,
            f"Structure Score: {structure_result.structural_score:.2f}",
            f"Detected Format: {structure_result.detected_format}",
            "Structure Analysis:",
            structure_analysis,
        ]

        return "\n".join(reason_parts)

    def _generate_verbose_logs(
        self,
        content_result: ContentSimilarityResult,
        structure_result: StructuralSimilarityResult,
    ) -> str:
        """Generate detailed logs for verbose mode"""
        verbose_data = {
            "content_analysis": {
                "matching_points": content_result.analysis.matching_points,
                "missing_points": content_result.analysis.missing_points,
                "incorrect_points": content_result.analysis.incorrect_points,
                "detailed_scores": content_result.scores.model_dump(),
            },
            "structural_analysis": {
                "detected_format": structure_result.detected_format,
                "detailed_scores": structure_result.scores.model_dump(),
                "missing_elements": structure_result.missing_elements,
                "format_issues": structure_result.format_issues,
            },
        }
        return json.dumps(verbose_data, indent=2)

    def is_completed(self) -> bool:
        """Check if evaluation is completed"""
        return self.result is not None or self.error is not None or self.skipped

    def is_successful(self) -> bool:
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
        return "Reference Evaluator"
