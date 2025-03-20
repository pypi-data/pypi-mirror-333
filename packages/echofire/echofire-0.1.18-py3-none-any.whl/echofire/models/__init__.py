"""Models for EchoFire."""

# Interactive models
from echofire.models.interactive_models import (
    AgentStateConfigure,
    AgentStateConfigured,
    AgentOutputDelta,
    AgentOutputDone,
    AgentOutputTranscript,
    AgentOutputWaiting,
    AgentOutputGenerating,
    AgentOutput,
    AnswerConfig,
    ErrorDetail,
    ErrorResponse,
)

# Testing models
from echofire.models.testing_models import (
    ContainsAssertion,
    LlmAsJudgeAssertion,
    Assertion,
    AssertionResult,
    TestResult,
)

__all__ = [
    # Interactive models
    "AgentStateConfigure",
    "AgentStateConfigured",
    "AgentOutputDelta",
    "AgentOutputDone",
    "AgentOutputTranscript",
    "AgentOutputWaiting",
    "AgentOutputGenerating",
    "AgentOutput",
    "AnswerConfig",
    "ErrorDetail",
    "ErrorResponse",
    # Testing models
    "ContainsAssertion",
    "LlmAsJudgeAssertion",
    "Assertion",
    "AssertionResult",
    "TestResult",
]
