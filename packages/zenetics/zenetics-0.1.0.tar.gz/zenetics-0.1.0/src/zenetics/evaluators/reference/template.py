class ReferenceTemplate:
    @staticmethod
    def content_similarity(reference_output: str, generated_output: str) -> str:
        return f"""You are an expert evaluator analyzing the similarity between a reference (correct) output and a generated output. Your task is to be STRICT and PRECISE in your evaluation.

INITIAL VALIDATION:
Before scoring, verify that the generated output is an actual response and not:
- A prompt or request for information
- Instructions or templates
- Format specifications
- Empty or placeholder content
If any of these are detected, score all metrics as 0.0 and list the issues in incorrect_points.

EVALUATION CRITERIA:

1. Information Completeness (Weight: 0.4)
Scoring guidelines:
- 0.0: No relevant information or completely different content
- 0.3: Only basic information matches
- 0.5: Some key points present but major omissions
- 0.8: Most key points present with minor omissions
- 1.0: All key points present and properly detailed

2. Factual Accuracy (Weight: 0.3)
Scoring guidelines:
- 0.0: Completely incorrect or unrelated facts
- 0.3: Major factual errors present
- 0.5: Mix of correct and incorrect facts
- 0.8: Mostly correct with minor inaccuracies
- 1.0: All facts completely accurate

3. Contextual Relevance (Weight: 0.2)
Scoring guidelines:
- 0.0: Completely different context or topic
- 0.3: Minimal contextual overlap
- 0.5: Partial context match
- 0.8: Good context match with some gaps
- 1.0: Perfect contextual alignment

4. Logical Flow (Weight: 0.1)
Scoring guidelines:
- 0.0: No logical structure or completely different
- 0.3: Poor organization with major issues
- 0.5: Basic structure with some issues
- 0.8: Good structure with minor issues
- 1.0: Perfect logical flow match

Reference Output:
{reference_output}

Generated Output:
{generated_output}

STRICT EVALUATION REQUIREMENTS:
1. Compare content word-by-word for factual matches
2. Use exact numeric comparisons for any figures
3. Check for presence of ALL key points
4. Verify proper context and scope
5. Ensure logical flow matches

The JSON response must follow this exact structure:
{{
    "scores": {{
        "information_completeness": <float 0-1>,
        "factual_accuracy": <float 0-1>,
        "contextual_relevance": <float 0-1>,
        "logical_flow": <float 0-1>
    }},
    "analysis": {{
        "matching_points": [<string>],
        "missing_points": [<string>],
        "incorrect_points": [<string>]
    }},
    "overall_score": <float 0-1>,
    "explanation": <string>
}}

SCORING RULES:
1. Overall score must be weighted average of individual scores
2. Any score of 0.0 in completeness or accuracy should result in overall score ≤ 0.3
3. Missing critical information should reduce completeness score by at least 0.3
4. Factual errors should reduce accuracy score by at least 0.5 per error
5. If generated output is not a valid response, all scores should be 0.0"""

    @staticmethod
    def structural_comparison(reference_output: str, generated_output: str) -> str:
        return f"""Analyze the structural similarity between the reference and generated outputs with STRICT criteria, with special attention to formatting conventions.

INITIAL VALIDATION:
Before scoring, verify that the generated output is an actual response and not:
- A prompt or request for information
- Instructions or templates
- Format specifications
- Empty or placeholder content
If any of these are detected, score as 0.0 and list in format_issues.

Reference:
{reference_output}

Generated:
{generated_output}

FORMAT DETECTION:
First, identify the primary format(s) used in the reference output:
- Markdown (headings, lists, code blocks, tables)
- JSON/Dictionary structures
- YAML format
- XML/HTML elements
- CSV/Tabular data
- Code (specify language if detected)
- Plain text with custom formatting

STRICT EVALUATION CRITERIA:

1. Required Sections (Weight: 0.35)
   - All major sections/components present
   - Required headers/identifiers included
   - Essential structural elements maintained

2. Format-Specific Compliance (Weight: 0.25)
   - Markdown: Correct heading levels, list types, code block formatting
   - JSON/YAML: Valid syntax, proper nesting, correct key-value structure
   - Code: Language-appropriate syntax, indentation, block structure
   - Tables: Proper column alignment, header formatting, cell structure
   - XML/HTML: Proper tag nesting, attribute formatting, element closure

3. Hierarchical Organization (Weight: 0.20)
   - Proper nesting of elements
   - Correct parent-child relationships
   - Consistent indentation patterns
   - Logical grouping of related elements

4. Formatting Consistency (Weight: 0.20)
   - Consistent use of formatting elements
   - Uniform style across similar components
   - Proper whitespace and delimiter usage
   - Appropriate use of formatting conventions

Scoring Guidelines:
0.0: No valid structure or completely different format
0.2: Major structural issues, format errors, or missing sections
0.4: Basic structure present but significant formatting differences
0.6: Good structure with noticeable formatting inconsistencies
0.8: Strong structural match with minor formatting differences
1.0: Perfect structural and formatting match

FORMAT-SPECIFIC CHECKS:
For Markdown:
- Heading levels (# vs ## vs ###)
- List formatting (-, *, numbering)
- Code block delimiters (```)
- Table structure (| and --- usage)
- Emphasis markers (*, _, **)

For JSON/Dictionary:
- Bracket/brace matching
- Key-value pair formatting
- Indentation consistency
- Array formatting
- Quote usage (single vs double)

For YAML:
- Indentation-based hierarchy
- List item markers
- Key-value separator style
- Multi-line string formatting
- Comment usage

For Code:
- Language-specific syntax
- Function/class structure
- Indentation patterns
- Comment style
- Block delimiters

For Tables/CSV:
- Header formatting
- Column alignment
- Cell delimiter consistency
- Row formatting

The JSON response must follow this exact structure:
{{
    "detected_format": "string identifying primary format",
    "structural_score": 0.0 to 1.0,
    "scores": {{
        "required_sections": 0.0 to 1.0,
        "format_compliance": 0.0 to 1.0,
        "hierarchical_organization": 0.0 to 1.0,
        "formatting_consistency": 0.0 to 1.0
    }},
    "missing_elements": ["list of missing elements"],
    "format_issues": ["list of format issues"],
    "explanation": "detailed explanation"
}}

SCORING RULES:
1. Overall structural score must be weighted average of individual scores
2. Missing critical sections should reduce required_sections score by at least 0.3
3. Format-specific errors should reduce format_compliance score proportionally to their severity
4. If generated output is not in the expected format, format_compliance should not exceed 0.3
5. If generated output is not a valid response, all scores should be 0.0"""
