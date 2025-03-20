from typing import List, Dict, Any, Optional, Union, Literal
from pydantic import BaseModel, Field, RootModel
from echofire.models.tracing_models import Trace


class ContainsAssertion(BaseModel):
    """Assertion that checks if a specific text is contained within the response."""

    type: Literal["contains"]
    description: Optional[str] = None  # Optional description of the assertion
    text: str  # Text that should be present in the response


class LlmAsJudgeAssertion(BaseModel):
    """Assertion evaluated by an LLM based on a provided prompt and condition."""

    type: Literal["llm-as-judge"]
    description: Optional[str] = None  # Optional description of the assertion
    prompt: str  # Prompt sent to the LLM for evaluation
    return_type: Literal[
        "integer", "string", "boolean"
    ]  # Expected return type from the LLM
    condition: str  # Condition to evaluate the LLM's response (e.g., "equals 'upsold'", "greater than 3")


class NoInterruptionAssertion(BaseModel):
    """
    Assertion that checks if the assistant remains silent for a specified duration
    after the last user utterance, ensuring it doesn't interrupt the user while thinking.

    Note: This assertion should only be used with recording sessions where you expect
    the last message to not be interrupted by the assistant. The assertion works by checking
    if the conversation ends with a user message followed by the end of conversation event,
    without any assistant response in between.
    """

    type: Literal["no-interruption"]
    description: Optional[str] = None  # Optional description of the assertion
    timeout_ms: int = Field(
        default=...,  # This means the field is required and has no default value
        description="Duration in milliseconds that the assistant should remain silent after the last utterance",
    )


Assertion = RootModel[
    Union[ContainsAssertion, LlmAsJudgeAssertion, NoInterruptionAssertion]
]


class AssertionResult(BaseModel):
    """Model for the result of an assertion evaluation"""

    assertion: Assertion
    passed: bool
    details: str


class TestResult(BaseModel):
    """Model to store test results"""

    test_name: str
    run_id: str
    audio_files: List[str]
    responses: List[Dict[str, Any]]
    success: bool
    error: Optional[str] = None
    iteration: int
    assertions: Optional[List[Assertion]] = None
    assertion_results: Optional[List[AssertionResult]] = None
    global_run_id: Optional[str] = None
    trace: Optional[Trace] = None  # Trace for the test run
