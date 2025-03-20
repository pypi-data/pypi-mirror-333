from typing import Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field


class AnswerConfig(BaseModel):
    """
    Configuration for the agent's answer behavior.
    """

    system_prompt: Optional[str] = None


class AgentStateConfigure(BaseModel):
    """
    Sent to configure the agent with a system prompt.
    (agent.state.configure)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.state.configure"] = "agent.state.configure"
    config_id: str = Field(default="default", description="Configuration identifier.")
    answer: AnswerConfig = Field(
        default_factory=AnswerConfig, description="Answer configuration."
    )


class AgentStateConfigured(BaseModel):
    """
    Returned when the agent has been successfully configured.
    (agent.state.configured)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.state.configured"] = "agent.state.configured"
    config_id: str = Field(..., description="The configuration ID that was applied.")


class AgentOutputWaiting(BaseModel):
    """
    Notifies that the agent is waiting for more user input.
    (agent.output.waiting)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.output.waiting"] = "agent.output.waiting"


class AgentOutputGenerating(BaseModel):
    """
    Notifies that the agent is generating a final response.
    (agent.output.generating)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.output.generating"] = "agent.output.generating"


class AgentOutputTranscript(BaseModel):
    """
    Returned when the model-generated transcription of audio output is updated.
    (agent.output.transcript)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.output.transcript"] = "agent.output.transcript"
    transcript: str = Field(..., description="The current transcript.")


class AgentOutputDelta(BaseModel):
    """
    Returned when an incremental text delta is received from the agent.
    (agent.output.delta)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.output.delta"] = "agent.output.delta"
    delta: str = Field(..., description="The incremental text delta.")


class AgentOutputDone(BaseModel):
    """
    Returned when the agent's streaming is complete.
    (agent.output.done)
    """

    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["agent.output.done"] = "agent.output.done"
    text: str = Field(..., description="The complete agent output text.")


# Union type for all agent output types
AgentOutput = Annotated[
    Union[
        AgentStateConfigured,
        AgentOutputWaiting,
        AgentOutputGenerating,
        AgentOutputTranscript,
        AgentOutputDelta,
        AgentOutputDone,
    ],
    Field(discriminator="object"),
]


# --- Error Models ---
class ErrorDetail(BaseModel):
    type: str = Field(
        ...,
        description="The type of error (e.g., 'invalid_request_error', 'server_error').",
    )
    code: Optional[str] = Field(None, description="Error code, if any.")
    message: str = Field(..., description="A human-readable error message.")
    param: Optional[str] = Field(
        None, description="Parameter related to the error, if any."
    )
    event_id: Optional[str] = Field(
        None,
        description="The event_id of the client event that caused the error, if applicable.",
    )


class ErrorResponse(BaseModel):
    event_id: str = Field(..., description="The unique ID of the server event.")
    object: Literal["error"] = "error"
    error: ErrorDetail
