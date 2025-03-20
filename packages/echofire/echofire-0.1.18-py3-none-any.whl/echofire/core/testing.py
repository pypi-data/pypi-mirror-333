#!/usr/bin/env python3

from typing import TypedDict, List
import asyncio
import json
import os
import sys
import ssl
import time
import yaml
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

import websockets
from pydantic import BaseModel, Field, RootModel, TypeAdapter, ValidationError
from typing import Literal, Union, Optional
import sounddevice as sd
import soundfile as sf
from human_id import generate_id
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    SpinnerColumn,
)

# Import for Fireworks AI
from openai import OpenAI
from echofire.models.config_model import EchoFireConfig
from echofire.utils.env import get_api_key, is_ci
from echofire.models.interactive_models import (
    AgentOutputDelta,
    AgentStateConfigure,
    AgentStateConfigured,
    AnswerConfig,
    AgentOutput,
    AgentOutputDone,
    AgentOutputTranscript,
    AgentOutputGenerating,
    ErrorResponse,
)

# Import for tracing
from echofire.models.tracing_models import Trace, Span, SpanKind, SpanStatus, Event

# Create OpenAI client with Fireworks API
client = OpenAI(
    api_key=get_api_key("FIREWORKS_API_KEY"),
    base_url="https://api.fireworks.ai/inference/v1",
)

# Create a global console instance
console = Console()

from echofire.models.testing_models import (
    Assertion,
    AssertionResult,
    TestResult,
)


async def read_audio_file(file_path: str) -> bytes:
    """Read an audio file and return its contents as bytes"""
    with open(file_path, "rb") as f:
        return f.read()


async def play_audio_file(file_path: str):
    """Play an audio file using sounddevice"""
    try:
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate)
        sd.wait()  # Wait until the audio is finished playing
        print(f"Played audio file: {file_path}")
    except Exception as e:
        print(f"Error playing audio file {file_path}: {e}")


async def stream_audio_files(
    websocket,
    audio_files: List[str],
    config: EchoFireConfig,
    progress=None,
    assert_no_interruption: int = 0,
    parent_span: Optional[Span] = None,
    trace: Optional[Trace] = None,
) -> List[Dict[str, Any]]:
    """
    Stream a sequence of audio files to the websocket.
    Wait for an agent.output.done event before sending the next file.
    Also wait for the first agent.output.done event before sending the first file.

    Args:
        websocket: The websocket connection
        audio_files: List of paths to audio files
        config: EchoFireConfig
        progress: Optional Progress instance from parent function
        assert_no_interruption: Time in milliseconds to wait after the last audio file if testing for no interruption
        parent_span: Optional parent span from run_test
        trace: Optional trace object to add spans to

    Returns:
        List of responses received from the server
    """
    responses = []
    audio_file_sent_time = None

    # Create a task to receive messages
    receive_queue = asyncio.Queue()
    receive_task = asyncio.create_task(
        receive_messages(websocket, receive_queue, parent_span, trace)
    )

    try:
        # Create a local progress tracking if no parent progress is provided
        audio_task = None
        local_progress = None

        if progress is None:
            # Create our own progress bar for audio files
            local_progress = Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
                transient=True,  # This makes the progress bars disappear when done
            )
            progress = local_progress
            progress.start()
            # Add a task for overall audio file progress
            audio_task = progress.add_task(
                "[yellow]Processing audio files...", total=len(audio_files)
            )
        else:
            # Use the parent progress but create a new task for audio files
            audio_task = progress.add_task(
                "[yellow]Processing audio files...",
                total=len(audio_files),
                visible=True,
            )

        try:
            # Create a span for waiting for initial response
            initial_wait_span = Span(
                trace_id=parent_span.trace_id,
                name="wait_for_initial_response",
                kind=SpanKind.CLIENT,
                parent_span_id=parent_span.span_id,
            )
            trace.add_span(initial_wait_span)

            # Wait for the first agent.output.done event before sending any audio
            progress.update(
                audio_task,
                description="[yellow]Waiting for initial server response...[/yellow]",
            )

            initial_response_count = 0
            while True:
                response = await receive_queue.get()
                responses.append(response)
                initial_response_count += 1

                # Add event for each response
                initial_wait_span.add_event(
                    f"received_{response.get('object', 'unknown')}", attributes=response
                )

                progress.update(
                    audio_task,
                    description=f"[yellow]Waiting for initial server response... [dim](Received {initial_response_count} responses)[/dim][/yellow]",
                )

                # Try to validate as AgentOutput
                try:
                    output = TypeAdapter(AgentOutput).validate_python(response)

                    # Check if this is an agent.output.done event
                    if isinstance(output, AgentOutputDone):
                        await asyncio.sleep(
                            config.pause_ms / 200
                        )  # Convert ms to seconds
                        initial_wait_span.add_event("received_done")
                        initial_wait_span.end()
                        break
                except ValidationError:
                    # Check for errors in raw response
                    if response.get("object") == "error":
                        error_msg = response.get("error", {}).get(
                            "message", "Unknown error"
                        )
                        console.print(
                            f"[bold red]Error received:[/bold red] {error_msg}"
                        )
                        initial_wait_span.set_status(SpanStatus.ERROR, error_msg)
                        initial_wait_span.end()
                        parent_span.set_status(SpanStatus.ERROR, error_msg)
                        raise Exception(f"Error from server: {error_msg}")

            # Now process each audio file
            for i, audio_file in enumerate(audio_files):
                # Create a span for each audio file processing
                audio_span = Span(
                    trace_id=parent_span.trace_id,
                    name=f"process_audio_file_{i+1}",
                    kind=SpanKind.CLIENT,
                    parent_span_id=parent_span.span_id,
                    attributes={"file_path": audio_file, "file_index": i},
                )
                trace.add_span(audio_span)

                # Update progress description with current file
                file_name = Path(audio_file).name
                progress.update(
                    audio_task,
                    description=f"[yellow]Processing audio file {i+1}/{len(audio_files)}: {file_name}[/yellow]",
                )

                # Create a span for reading the audio file
                read_span = Span(
                    trace_id=parent_span.trace_id,
                    name=f"read_audio_file_{i+1}",
                    kind=SpanKind.INTERNAL,
                    parent_span_id=audio_span.span_id,
                )
                trace.add_span(read_span)
                audio_data = await read_audio_file(audio_file)
                read_span.end()

                # Play the audio file if requested
                if config.play_audio:
                    play_span = Span(
                        trace_id=parent_span.trace_id,
                        name=f"play_audio_file_{i+1}",
                        kind=SpanKind.INTERNAL,
                        parent_span_id=audio_span.span_id,
                    )
                    trace.add_span(play_span)
                    await play_audio_file(audio_file)
                    play_span.end()

                # Create a span for sending the audio data
                send_span = Span(
                    trace_id=parent_span.trace_id,
                    name=f"send_audio_file_{i+1}",
                    kind=SpanKind.PRODUCER,
                    parent_span_id=audio_span.span_id,
                    attributes={"audio_size_bytes": len(audio_data)},
                )
                trace.add_span(send_span)

                # Send the audio data
                await websocket.send(audio_data)
                send_span.end()

                # Wait for agent.output.done event
                response_count = 0
                audio_file_sent_time = time.time()

                # Create a span for waiting for responses
                wait_span = Span(
                    trace_id=parent_span.trace_id,
                    name=f"wait_for_responses_{i+1}",
                    kind=SpanKind.CONSUMER,
                    parent_span_id=audio_span.span_id,
                )
                trace.add_span(wait_span)

                while True:
                    response = await receive_queue.get()
                    responses.append(response)
                    response_count += 1

                    # Add event for each response
                    wait_span.add_event(
                        f"received_{response.get('object', 'unknown')}",
                        attributes=response,
                    )

                    # Update progress description with response count
                    progress.update(
                        audio_task,
                        description=f"[yellow]Processing audio file {i+1}/{len(audio_files)}: {file_name} [dim](Received {response_count} responses)[/dim][/yellow]",
                    )

                    # Track latency between final transcript and first agent response
                    try:
                        output = TypeAdapter(AgentOutput).validate_python(response)

                        if (
                            isinstance(output, AgentOutputGenerating)
                            and audio_file_sent_time
                        ):
                            # Calculate latency
                            latency = time.time() - audio_file_sent_time
                            response["latency_ms"] = int(latency * 1000)
                            wait_span.attributes["latency_ms"] = response["latency_ms"]
                            audio_file_sent_time = None

                        # Check if this is an agent.output.done event
                        if isinstance(output, AgentOutputDone):
                            await asyncio.sleep(
                                config.pause_ms / 200
                            )  # Convert ms to seconds
                            wait_span.add_event("received_done")
                            wait_span.end()
                            break
                    except ValidationError:
                        # Check for errors in raw response
                        if response.get("object") == "error":
                            error_msg = response.get("error", {}).get(
                                "message", "Unknown error"
                            )
                            console.print(
                                f"[bold red]Error received:[/bold red] {error_msg}"
                            )
                            wait_span.set_status(SpanStatus.ERROR, error_msg)
                            wait_span.end()
                            audio_span.set_status(SpanStatus.ERROR, error_msg)
                            audio_span.end()
                            parent_span.set_status(SpanStatus.ERROR, error_msg)
                            raise Exception(f"Error from server: {error_msg}")

                # End the audio file span
                audio_span.end()

                # Advance the progress bar
                progress.advance(audio_task)

            # If we're testing for no interruption, wait for the specified time after the last audio file
            if assert_no_interruption > 0:
                wait_seconds = assert_no_interruption / 1000  # Convert ms to seconds
                no_interrupt_span = Span(
                    trace_id=parent_span.trace_id,
                    name="wait_no_interruption",
                    kind=SpanKind.INTERNAL,
                    parent_span_id=parent_span.span_id,
                    attributes={"wait_ms": assert_no_interruption},
                )
                trace.add_span(no_interrupt_span)

                progress.update(
                    audio_task,
                    description=f"[yellow]Waiting {assert_no_interruption}ms for no-interruption test...[/yellow]",
                )

                # Collect any responses during the waiting period
                wait_start_time = time.time()
                while time.time() - wait_start_time < wait_seconds:
                    try:
                        # Use wait_for with a timeout to avoid blocking indefinitely
                        response = await asyncio.wait_for(
                            receive_queue.get(),
                            timeout=min(
                                1.0, wait_seconds - (time.time() - wait_start_time)
                            ),
                        )
                        responses.append(response)
                        no_interrupt_span.add_event(
                            f"received_{response.get('object', 'unknown')}",
                            attributes=response,
                        )

                        # Update progress with remaining time
                        remaining_ms = int(
                            (wait_seconds - (time.time() - wait_start_time)) * 1000
                        )
                        progress.update(
                            audio_task,
                            description=f"[yellow]Waiting for no-interruption test... [dim]({remaining_ms}ms remaining)[/dim][/yellow]",
                        )
                    except asyncio.TimeoutError:
                        # This is expected, just update the progress
                        remaining_ms = int(
                            (wait_seconds - (time.time() - wait_start_time)) * 1000
                        )
                        if remaining_ms > 0:
                            progress.update(
                                audio_task,
                                description=f"[yellow]Waiting for no-interruption test... [dim]({remaining_ms}ms remaining)[/dim][/yellow]",
                            )

                no_interrupt_span.end()
                progress.update(
                    audio_task,
                    description="[green]No-interruption wait period completed[/green]",
                )

        finally:
            # Stop our local progress if we created one
            if local_progress:
                local_progress.stop()
    finally:
        # Cancel the receive task
        receive_task.cancel()
        try:
            await receive_task
        except asyncio.CancelledError:
            pass

    # Add an end-of-conversation event with a timestamp
    end_event = {
        "object": "conversation.end",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "End of conversation",
    }
    responses.append(end_event)
    parent_span.add_event("conversation_end", attributes=end_event)

    return responses


async def receive_messages(
    websocket, queue: asyncio.Queue, parent_span: Span, trace: Optional[Trace]
):
    """
    Continuously receive messages from the websocket and put them in the queue.

    Args:
        websocket: The websocket connection
        queue: Queue to put received messages into
        parent_span: Parent span to create child spans under
        trace: Optional trace object to add spans to
    """
    # Create a span for the receive loop
    receive_span = Span(
        trace_id=parent_span.trace_id,
        name="receive_messages_loop",
        kind=SpanKind.CONSUMER,
        parent_span_id=parent_span.span_id,
        attributes={"service": "websocket_receiver"},
    )
    trace.add_span(receive_span)

    # Track the current conversation state
    current_text = ""
    current_generating_span = None

    async def put_timestamped_message(message):
        """Helper to add timestamp and put message on queue"""
        if isinstance(message, dict):
            message = message.copy()  # Don't modify the original
        else:
            message = message.model_dump()
        message["timestamp"] = datetime.now(timezone.utc).isoformat()
        await queue.put(message)

    try:
        while True:
            try:
                # Create a span for this message BEFORE the I/O operation
                msg_span = Span(
                    trace_id=parent_span.trace_id,
                    name="processing_message",  # Will be updated with more specific name later
                    kind=SpanKind.CONSUMER,
                    parent_span_id=receive_span.span_id,
                    attributes={"raw_message_received": False},
                )

                # Now do the I/O operation - this will be captured in the span duration
                raw_msg = await websocket.recv()

                # Update the span to indicate we've received data
                msg_span.attributes["raw_message_received"] = True

                if isinstance(raw_msg, bytes):
                    decoded_msg = raw_msg.decode("utf-8", errors="replace")
                else:
                    decoded_msg = raw_msg

                # Strip "data:" prefix if present (as in SSE streams)
                if decoded_msg.startswith("data:"):
                    decoded_msg = decoded_msg.partition("data:")[2].strip()

                try:
                    data = json.loads(decoded_msg)

                    # Try to validate as AgentOutput
                    try:
                        # This will validate and convert to the appropriate model
                        output = TypeAdapter(AgentOutput).validate_python(data)

                        # Update the span name and attributes based on the output type
                        msg_span.name = f"agent_output_{output.object.split('.')[-1]}"
                        msg_span.attributes["event_id"] = output.event_id
                        msg_span.attributes["object"] = output.object

                        # Add specific attributes based on message type
                        if isinstance(output, AgentStateConfigured):
                            msg_span.attributes["config_id"] = output.config_id

                        elif isinstance(output, AgentOutputTranscript):
                            msg_span.attributes["transcript"] = output.transcript

                        elif isinstance(output, AgentOutputGenerating):
                            if "latency_ms" in data:
                                msg_span.attributes["latency_ms"] = data["latency_ms"]
                            current_generating_span = msg_span
                            current_text = ""  # Reset text accumulator

                        elif isinstance(output, AgentOutputDelta):
                            msg_span.attributes["delta"] = output.delta
                            current_text += output.delta
                            if current_generating_span:
                                msg_span.attributes["parent_generating_event_id"] = (
                                    current_generating_span.attributes["event_id"]
                                )

                        elif isinstance(output, AgentOutputDone):
                            msg_span.attributes["text"] = output.text
                            if current_generating_span:
                                msg_span.attributes["parent_generating_event_id"] = (
                                    current_generating_span.attributes["event_id"]
                                )
                            current_generating_span = None  # Reset generating span

                        # Put the validated model in the queue
                        await put_timestamped_message(output)

                        # Complete the span AFTER the queue.put operation
                        trace.add_span(msg_span)
                        msg_span.set_status(SpanStatus.OK)
                        msg_span.end()

                    except ValidationError:
                        # If it's not a valid AgentOutput, just put the raw data
                        # Update span for non-AgentOutput messages
                        msg_span.name = f"message_{data.get('object', 'unknown')}"
                        msg_span.attributes.update(data)

                        await put_timestamped_message(data)

                        # Complete the span AFTER the queue.put operation
                        trace.add_span(msg_span)
                        msg_span.set_status(SpanStatus.OK)
                        msg_span.end()

                except json.JSONDecodeError as e:
                    console.print(f"[bold red]JSON decode error:[/bold red] {e}")
                    error_data = {
                        "object": "error",
                        "error": {"message": f"JSON decode error: {e}"},
                    }

                    # Update the span for the JSON decode error
                    msg_span.name = "json_decode_error"
                    msg_span.attributes.update(error_data)

                    await put_timestamped_message(error_data)

                    # Complete the span with error status
                    trace.add_span(msg_span)
                    msg_span.set_status(SpanStatus.ERROR, str(e))
                    msg_span.end()

            except asyncio.CancelledError:
                receive_span.set_status(SpanStatus.ERROR, "Task cancelled")
                receive_span.end()
                break
            except Exception as e:
                console.print(f"[bold red]Error receiving message:[/bold red] {e}")
                error_data = {
                    "object": "error",
                    "error": {"message": f"Error receiving message: {e}"},
                }

                # Update the existing msg_span with error information
                if "msg_span" in locals():
                    msg_span.name = "receive_error"
                    msg_span.attributes.update(error_data)

                    await put_timestamped_message(error_data)

                    # Complete the span with error status
                    trace.add_span(msg_span)
                    msg_span.set_status(SpanStatus.ERROR, str(e))
                    msg_span.end()
                else:
                    # Fallback if msg_span doesn't exist (shouldn't happen in normal flow)
                    error_span = Span(
                        trace_id=parent_span.trace_id,
                        name="receive_error",
                        kind=SpanKind.CONSUMER,
                        parent_span_id=receive_span.span_id,
                        attributes=error_data,
                    )
                    trace.add_span(error_span)
                    error_span.set_status(SpanStatus.ERROR, str(e))
                    error_span.end()

                    await put_timestamped_message(error_data)
                receive_span.set_status(SpanStatus.ERROR, str(e))
                receive_span.end()
                break

    except Exception as e:
        receive_span.set_status(SpanStatus.ERROR, str(e))
    finally:
        if not receive_span.end_time:
            receive_span.end()


async def evaluate_assertions(
    assertions: List[Assertion],
    responses: List[Dict[str, Any]],
    system_prompt: str,
    progress=None,
) -> List[AssertionResult]:
    """
    Evaluate assertions against the test responses.

    Args:
        assertions: List of assertions to evaluate
        responses: List of responses from the server
        system_prompt: System prompt used for the test
        progress: Optional Progress instance from parent function

    Returns:
        List of assertion results
    """
    results = []

    # Extract all agent output text from responses
    agent_outputs = []
    transcripts = []

    for response in responses:
        try:
            output = TypeAdapter(AgentOutput).validate_python(response)

            if isinstance(output, AgentOutputDone):
                agent_outputs.append(output.text)
            elif isinstance(output, AgentOutputTranscript):
                transcripts.append(output.transcript)
        except ValidationError:
            # Skip non-AgentOutput messages
            pass

    # Combine all agent outputs and transcripts
    combined_agent_output = "\n".join(agent_outputs)
    combined_transcript = "\n".join(transcripts)

    # Create a task for assertion evaluation if progress is provided
    assertion_task = None
    if progress:
        assertion_task = progress.add_task(
            "[cyan]Evaluating assertions...", total=len(assertions)
        )

    # Evaluate each assertion
    for i, assertion in enumerate(assertions):
        if progress:
            progress.update(
                assertion_task,
                description=f"[cyan]Evaluating assertion {i+1}/{len(assertions)}: {assertion.root.description}",
            )

        if assertion.root.type == "contains":
            text_to_find = assertion.root.text
            found_in_output = text_to_find.lower() in combined_agent_output.lower()
            found_in_transcript = text_to_find.lower() in combined_transcript.lower()

            if found_in_output or found_in_transcript:
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=True,
                        details=f"Found text '{text_to_find}' in the {'output' if found_in_output else 'transcript'}",
                    )
                )
                progress.update(
                    assertion_task,
                    description=f"[green]✓ {assertion.root.description}: Found '{text_to_find}'[/green]",
                )
            else:
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=False,
                        details=f"Text '{text_to_find}' not found in the responses",
                    )
                )
                progress.update(
                    assertion_task,
                    description=f"[red]✗ {assertion.root.description}: Text '{text_to_find}' not found[/red]",
                )

        elif assertion.root.type == "no-interruption":
            # Implementation for checking if the agent interrupted the user
            # Check if the conversation ends with a user message followed by end of conversation

            # Initialize with default values
            last_is_conversation_end = False
            second_last_is_transcript = False

            # Simply look at the last two responses
            if len(responses) >= 2:
                last_response = responses[-1]
                second_last_response = responses[-2]

                # Check if the last message is conversation.end
                last_is_conversation_end = (
                    last_response.get("object") == "conversation.end"
                )

                # Check if the second last message is a transcript
                try:
                    output = TypeAdapter(AgentOutput).validate_python(
                        second_last_response
                    )
                    second_last_is_transcript = isinstance(
                        output, AgentOutputTranscript
                    )
                except ValidationError:
                    second_last_is_transcript = False

            # Check if the last message is conversation.end and the second last is a user transcript
            if last_is_conversation_end and second_last_is_transcript:
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=True,
                        details="The conversation ends with a user message followed by end of conversation",
                    )
                )
                progress.update(
                    assertion_task,
                    description=f"[green]✓ {assertion.root.description}: Conversation ends correctly[/green]",
                )
            else:
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=False,
                        details=f"The conversation does not end with a user message followed by end of conversation. Last is conversation.end: {last_is_conversation_end}, Second last is transcript: {second_last_is_transcript}",
                    )
                )
                progress.update(
                    assertion_task,
                    description=f"[red]✗ {assertion.root.description}: Conversation doesn't end correctly[/red]",
                )

        elif assertion.root.type == "llm-as-judge":
            # Build context for the LLM to judge
            context = ""
            for resp in responses:
                try:
                    output = TypeAdapter(AgentOutput).validate_python(resp)

                    if isinstance(output, AgentOutputTranscript):
                        context += f"User: {output.transcript}\n"
                    elif isinstance(output, AgentOutputDone):
                        context += f"Agent: {output.text}\n"
                except ValidationError:
                    # Handle non-AgentOutput messages
                    if "transcript" in resp:
                        context += f"User: {resp.get('transcript', '')}\n"
                    elif "output" in resp:
                        context += f"Agent output: {resp['output']}\n"

            # Prepare the prompt for the LLM
            prompt = f"""
You are evaluating a conversation between a user and an AI assistant.

Here is the conversation:
{context}

System prompt given to the assistant:
{system_prompt}

{assertion.root.prompt}
"""

            try:
                # First call: Generate the return value using JSON mode
                json_prompt = f"""You are evaluating a conversation.
Here is the context:
{context}

Based on this context, please evaluate the following:
{prompt}

Additional context - this was the script the voice agent was supposed to follow:
{system_prompt}

Return your answer as a JSON object with a key "result" with a value of type {assertion.root.return_type} and a key "result_explanation" with a string value explaining the meaning and significance of your result.
"""

                # Make the first API call to get the result
                response = client.chat.completions.create(
                    model="accounts/fireworks/models/llama-v3p3-70b-instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an experienced call center QA professional evaluating whether this call passes the provided evaluation criteria. Provide structured JSON responses with your assessment.",
                        },
                        {"role": "user", "content": json_prompt},
                    ],
                    response_format={
                        "type": "json_object",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "result": {"type": assertion.root.return_type.lower()},
                                "result_explanation": {"type": "string"},
                            },
                            "required": ["result"],
                        },
                    },
                    temperature=0,
                )

                # Extract the result from the JSON response
                result_text = response.choices[0].message.content
                result_json = json.loads(result_text)
                result_value = result_json.get("result")
                result_explanation = result_json.get(
                    "result_explanation", "No result explanation provided"
                )

                if result_value is None:
                    results.append(
                        AssertionResult(
                            assertion=assertion,
                            passed=False,
                            details=f"LLM did not return a valid result. Response: {result_text}",
                        )
                    )
                    progress.update(
                        assertion_task,
                        description=f"[red]✗ {assertion.root.description}: Invalid LLM response[/red]",
                    )
                    continue

                # Second call: Evaluate the condition using LLM
                condition_prompt = f"""You are evaluating a condition.
The result value is: {result_value} (type: {assertion.root.return_type})
The condition is: {assertion.root.condition}

Evaluate if the result satisfies the condition. Return your answer as a JSON object with a key "satisfied" with a boolean value.
"""

                # Make the second API call to evaluate the condition
                condition_response = client.chat.completions.create(
                    model="accounts/fireworks/models/llama-v3p3-70b-instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that returns structured JSON responses.",
                        },
                        {"role": "user", "content": condition_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0,
                )

                # Extract the condition evaluation result
                condition_text = condition_response.choices[0].message.content
                condition_json = json.loads(condition_text)
                condition_satisfied = condition_json.get("satisfied", False)

                # Create the assertion result
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=condition_satisfied,
                        details=f"LLM evaluation: Result={result_value}, Condition={assertion.root.condition}, Satisfied={condition_satisfied}. {result_explanation}",
                    )
                )

                if condition_satisfied:
                    progress.update(
                        assertion_task,
                        description=f"[green]✓ {assertion.root.description}: LLM evaluation passed[/green]",
                    )
                else:
                    progress.update(
                        assertion_task,
                        description=f"[red]✗ {assertion.root.description}: LLM evaluation failed[/red]",
                    )
            except Exception as e:
                error_msg = str(e)
                results.append(
                    AssertionResult(
                        assertion=assertion,
                        passed=False,
                        details=f"Error during LLM evaluation: {error_msg}",
                    )
                )
                progress.update(
                    assertion_task,
                    description=f"[red]✗ {assertion.root.description}: Error - {error_msg}[/red]",
                )

        else:
            results.append(
                AssertionResult(
                    assertion=assertion,
                    passed=False,
                    details=f"Unknown assertion type: {assertion.root.type}",
                )
            )
            progress.update(
                assertion_task,
                description=f"[red]✗ {assertion.root.description}: Unknown assertion type[/red]",
            )

        # Advance the progress bar
        progress.advance(assertion_task)

    return results


async def run_test(
    test_dir: str,
    config: EchoFireConfig,
    run_id: str,
    global_run_id: str = None,
    iteration: int = 0,
    progress=None,
) -> TestResult:
    """
    Run a test by streaming all audio files in the test directory to the websocket.

    Args:
        test_dir: Path to the test directory
        websocket_url: URL of the websocket server
        pause_ms: Pause duration in milliseconds between files
        play_audio: Whether to play the audio files on the device
        global_run_id: Global ID for the entire test run
        iteration: Current iteration number
        progress: Optional Progress instance from parent function

    Returns:
        TestResult object with the test results
    """
    # Create a trace for the entire test run
    test_trace = Trace(name=f"test_run_{Path(test_dir).name}")
    test_span = Span(
        trace_id=test_trace.trace_id,
        name=f"test_run_{Path(test_dir).name}",
        kind=SpanKind.INTERNAL,
        attributes={
            "test_dir": test_dir,
            "run_id": run_id,
            "global_run_id": global_run_id,
            "iteration": iteration,
            "websocket_url": config.original_websocket_url,
            "pause_ms": config.pause_ms,
            "play_audio": config.play_audio,
        },
    )
    test_trace.add_span(test_span)

    test_path = Path(test_dir)
    utterance_path = test_path / "utterances"
    test_name = test_path.name

    # Load assertions from assertions.yaml if it exists
    assertions: List[Assertion] = []
    assertions_file = test_path / "assertions.yaml"
    if assertions_file.exists():
        try:
            with open(assertions_file, "r") as f:
                assertions_data = yaml.safe_load(f)
                if assertions_data and "assertions" in assertions_data:
                    for assertion_data in assertions_data["assertions"]:
                        assertions.append(Assertion(**assertion_data))
        except Exception as e:
            console.print(
                f"[bold red]Error loading assertions from {assertions_file}:[/bold red] {e}"
            )
            test_span.set_status(SpanStatus.ERROR, str(e))
            test_span.end()
            test_trace.end()
            raise e

    # Set assert_no_interruption to the timeout_ms value if a no-interruption assertion exists
    assert_no_interruption = 0
    for assertion in assertions:
        if assertion.root.type == "no-interruption":
            assert_no_interruption = assertion.root.timeout_ms
            break

    # Find all utterance files in the test directory
    audio_files = sorted([str(f) for f in utterance_path.glob("utterance_*.wav")])

    if not audio_files:
        error_msg = f"No utterance files found in test directory: {test_path}"
        test_span.set_status(SpanStatus.ERROR, error_msg)
        test_span.end()
        test_trace.end()
        raise Exception(error_msg)

    # Create SSL context for secure connections
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        # Create a span for the websocket connection
        ws_span = Span(
            trace_id=test_trace.trace_id,
            name="websocket_connection",
            kind=SpanKind.CLIENT,
            parent_span_id=test_span.span_id,
            attributes={"url": config.original_websocket_url},
        )
        test_trace.add_span(ws_span)

        # Determine if we need SSL based on the URL scheme
        use_ssl = config.websocket_url.startswith("wss://")
        ws_kwargs = {"ssl": ssl_context} if use_ssl else {}

        async with websockets.connect(config.websocket_url, **ws_kwargs) as websocket:
            ws_span.set_status(SpanStatus.OK)
            ws_span.end()

            # Create a span for system prompt configuration
            config_span = Span(
                trace_id=test_trace.trace_id,
                name="configure_system_prompt",
                kind=SpanKind.PRODUCER,
                parent_span_id=test_span.span_id,
            )
            test_trace.add_span(config_span)

            # If a system prompt is provided, send it as an agent.state.configure message
            if config.system_prompt is not None:
                config_msg = AgentStateConfigure(
                    event_id=str(uuid.uuid4()),
                    config_id=str(uuid.uuid4()),
                    answer=AnswerConfig(system_prompt=config.system_prompt),
                )
                await websocket.send(json.dumps(config_msg.model_dump()))
                config_span.set_status(SpanStatus.OK)
            else:
                error_msg = "No system prompt provided."
                config_span.set_status(SpanStatus.ERROR, error_msg)
                config_span.end()
                test_span.set_status(SpanStatus.ERROR, error_msg)
                test_span.end()
                test_trace.end()
                raise ValueError(error_msg)

            config_span.end()

            # Create a span for streaming audio files
            stream_span = Span(
                trace_id=test_trace.trace_id,
                name="stream_audio_files",
                kind=SpanKind.PRODUCER,
                parent_span_id=test_span.span_id,
                attributes={"num_files": len(audio_files)},
            )
            test_trace.add_span(stream_span)

            responses = await stream_audio_files(
                websocket,
                audio_files,
                config,
                progress,
                assert_no_interruption,
                parent_span=stream_span,
                trace=test_trace,
            )

            # Set the final status of the stream span
            stream_span.set_status(SpanStatus.OK)
            stream_span.end()

            # Evaluate assertions if any
            assertion_results = []
            if assertions:
                assertion_results = await evaluate_assertions(
                    assertions, responses, config.system_prompt, progress
                )
                all_passed = all(result.passed for result in assertion_results)
            else:
                all_passed = True

            # Set the final status of the test span
            if all_passed:
                test_span.set_status(SpanStatus.OK)
            else:
                test_span.set_status(SpanStatus.ERROR, "Some assertions failed")
            test_span.end()
            test_trace.end()

            result = TestResult(
                test_name=test_name,
                audio_files=audio_files,
                responses=responses,
                iteration=iteration,
                success=all_passed,
                assertions=assertions,
                run_id=run_id,
                assertion_results=assertion_results,
                global_run_id=global_run_id,
                trace=test_trace,
            )

            return result

    except Exception as e:
        error_msg = str(e)
        test_span.set_status(SpanStatus.ERROR, error_msg)
        test_span.end()
        test_trace.end()

        return TestResult(
            test_name=test_name,
            audio_files=audio_files,
            responses=[],
            success=False,
            error=error_msg,
            run_id=run_id,
            iteration=iteration,
            assertions=assertions,
            global_run_id=global_run_id,
            trace=test_trace,
        )


class ConversationEntry(TypedDict):
    role: str
    text: str
    timestamp: str


class Conversation(TypedDict):
    test_name: str
    timestamp: str
    conversation: List[ConversationEntry]


def save_transcripts_from_responses(
    test_dir: Path, responses: List[Dict[str, Any]]
) -> Conversation:
    """
    Extract transcripts from responses and save them to a YAML file.

    Args:
        test_dir: Path to the test directory
        responses: List of responses from the server

    Returns:
        Dictionary containing the conversation data
    """
    # Extract transcripts and responses
    conversation: List[ConversationEntry] = []
    current_user_transcript = ""
    transcript_timestamp = ""

    for response in responses:
        try:
            # Try to parse as AgentOutput
            output = TypeAdapter(AgentOutput).validate_python(response)

            if isinstance(output, AgentOutputTranscript):
                current_user_transcript = output.transcript
                # Store the timestamp of the first transcript for this user message
                if not transcript_timestamp:
                    transcript_timestamp = response.get("timestamp", "")
                # We don't add the user message yet, as it might be updated by subsequent transcripts

            elif isinstance(output, AgentOutputDone):
                # Add the final user transcript if we have one
                if current_user_transcript:
                    conversation.append(
                        {
                            "role": "user",
                            "text": current_user_transcript,
                            "timestamp": transcript_timestamp,
                        }
                    )
                    current_user_transcript = ""
                    transcript_timestamp = ""  # Reset for next user message

                # Add the assistant message
                conversation.append(
                    {
                        "role": "assistant",
                        "text": output.text,
                        "timestamp": response.get("timestamp", ""),
                    }
                )
        except ValidationError:
            # Handle non-AgentOutput messages
            if response.get("object") == "conversation.end":
                # Handle end of conversation event
                conversation.append(
                    {
                        "role": "system",
                        "text": "End of conversation",
                        "timestamp": response.get("timestamp", ""),
                    }
                )

    # Add any remaining user transcript
    if current_user_transcript:
        conversation.append(
            {
                "role": "user",
                "text": current_user_transcript,
                "timestamp": transcript_timestamp
                or datetime.now(timezone.utc).isoformat(),
            }
        )

    # Create the transcript data structure
    transcript_data: Conversation = {
        "test_name": test_dir.name,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "conversation": conversation,
    }

    return transcript_data


async def run_all_tests(
    tests_dir: str,
    config: EchoFireConfig,
    global_run_id: str = None,
    repeat: int = 5,
    test_name: str = None,
) -> List[TestResult]:
    """
    Run all tests in the tests directory concurrently, repeating each test multiple times.

    Args:
        tests_dir: Path to the directory containing test directories
        websocket_url: URL of the websocket server
        pause_ms: Pause duration in milliseconds between files
        play_audio: Whether to play the audio files on the device
        global_run_id: Global ID for the entire test run (used to correlate multiple test results)
        repeat: Number of times to repeat each test

    Returns:
        List of TestResult objects
    """
    tests_path = Path(tests_dir)

    # Find all test directories
    test_dirs = [d for d in tests_path.iterdir() if d.is_dir()]

    if test_name:
        test_dirs = [d for d in test_dirs if d.name == test_name]

    if not test_dirs:
        console.print(f"[bold red]No test directories found in {tests_dir}[/bold red]")
        return []

    # Define an async wrapper to handle each test individually
    async def run_single_test(test_dir: Path, iteration: int, progress, task_id):
        # Update progress description
        progress.update(
            task_id,
            description=f"Test: {test_dir.name} (Iteration {iteration + 1}/{repeat})",
        )

        # Generate a unique human-readable ID for this run
        run_id = generate_id(word_count=4)

        result = await run_test(
            str(test_dir),
            config,
            run_id,
            global_run_id,
            iteration,
            progress,
        )

        # Save transcript to run directory

        # Save this test's results immediately
        save_test_results(
            config,
            [result],
            test_dir,
            global_run_id,
        )

        # Update progress with success/failure status
        status = "[green]✓ PASSED[/green]" if result.success else "[red]✗ FAILED[/red]"
        progress.update(
            task_id,
            description=f"Test: {test_dir.name} (Iteration {iteration + 1}/{repeat}) {status}",
        )
        progress.advance(task_id)

        return result

    # Calculate total number of test runs
    total_tests = len(test_dirs) * repeat

    # Create a custom progress display
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,  # This makes the progress bars disappear when done
    ) as progress:
        # Create a main task for overall progress
        overall_task = progress.add_task(
            "[yellow]Running all tests...", total=total_tests
        )

        # Create individual tasks for each test/iteration
        tasks = []
        task_ids = []

        for test_dir in test_dirs:
            for iteration in range(repeat):
                task_description = (
                    f"Test: {test_dir.name} (Iteration {iteration + 1}/{repeat})"
                )
                task_id = progress.add_task(task_description, total=1)
                task_ids.append(task_id)
                tasks.append(run_single_test(test_dir, iteration, progress, task_id))

        # Run all tasks concurrently and update the overall progress
        results = await asyncio.gather(*tasks)
        progress.update(overall_task, completed=total_tests)

    # After progress bars are done (they'll be removed due to transient=True)
    console.print(f"[bold green]Completed {total_tests} test runs![/bold green]")

    return results


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def save_test_results(
    config: EchoFireConfig,
    results: List[TestResult],
    test_dir: str,
    global_run_id: str = None,
):
    """
    Save test results to files and update global CSV tracking file

    Args:
        results: List of test results to save
        output_dir: Directory to save results to
        global_run_id: Global ID for the entire test run (used to correlate multiple test results)
        pause_ms: Pause duration in milliseconds between files
        play_audio: Whether to play the audio files on the device
        websocket_url: URL of the websocket server
    """
    # Path to global CSV file
    global_csv_path = Path(test_dir).parent / "test-runs.csv"
    global_csv_path.parent.mkdir(exist_ok=True, parents=True)

    # Define CSV headers
    csv_headers = [
        "timestamp",
        "test_name",
        "global_run_id",
        "run_id",
        "success",
        "error",
        "assertions",
        "assertions_passed",
        "assertions_total",
        "assertions_details",
        "test_arguments",
        "test_arguments_json",
        "system_prompt",
        "avg_asr_latency_ms",
        "min_asr_latency_ms",
        "max_asr_latency_ms",
        "is_ci",
        "trace_data",
        "transcript",
    ]

    # Check if CSV exists and create with headers if it doesn't
    csv_exists = global_csv_path.exists()

    # Prepare rows for the CSV
    csv_rows = []

    # Save individual test results
    for result in results:
        # Generate timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        # Get run ID from output directory
        run_id = result.run_id

        # Format assertion details for CSV
        assertion_details = ""
        if result.assertion_results:
            assertion_lines = []
            for i, ar in enumerate(result.assertion_results, 1):
                status = "PASSED" if ar.passed else "FAILED"
                # Handle case where description is None by using a default
                assertion_lines.append(
                    f"{i}. {ar.assertion.root.description or f'Assertion {i}'} ({status}): {ar.details}"
                )
            assertion_details = "\n".join(assertion_lines)

        # Create row for CSV
        test_arguments = f"pause_ms={config.pause_ms}, play_audio={config.play_audio}, websocket_url={config.original_websocket_url}"

        test_arguments_json = {
            "pause_ms": config.pause_ms,
            "play_audio": config.play_audio,
            "websocket_url": config.original_websocket_url,
        }

        # Calculate latency statistics from responses
        asr_latencies = [
            r.get("latency_ms") for r in result.responses if "latency_ms" in r
        ]
        avg_latency = sum(asr_latencies) / len(asr_latencies) if asr_latencies else None
        min_latency = min(asr_latencies) if asr_latencies else None
        max_latency = max(asr_latencies) if asr_latencies else None

        # Extract transcripts from responses
        transcript_data = save_transcripts_from_responses(
            Path(test_dir), result.responses
        )

        csv_row = {
            "timestamp": timestamp,
            "test_name": result.test_name,
            "run_id": run_id,
            "global_run_id": global_run_id,
            "success": "TRUE" if result.success else "FALSE",
            "error": result.error or "",
            "assertions": json.dumps(
                [ar.model_dump() for ar in (result.assertion_results or [])]
            ),
            "assertions_passed": sum(
                1 for ar in (result.assertion_results or []) if ar.passed
            ),
            "assertions_total": len(result.assertion_results or []),
            "assertions_details": assertion_details,
            "test_arguments": test_arguments,
            "test_arguments_json": json.dumps(test_arguments_json),
            "system_prompt": config.system_prompt,
            "avg_asr_latency_ms": (
                f"{avg_latency:.2f}" if avg_latency is not None else ""
            ),
            "min_asr_latency_ms": (
                f"{min_latency:.2f}" if min_latency is not None else ""
            ),
            "max_asr_latency_ms": (
                f"{max_latency:.2f}" if max_latency is not None else ""
            ),
            "is_ci": is_ci(),
            "trace_data": (
                json.dumps(result.trace.model_dump(), cls=DateTimeEncoder)
                if result.trace
                else ""
            ),
            "transcript": (
                json.dumps(transcript_data, cls=DateTimeEncoder)
                if transcript_data
                else ""
            ),
        }

        csv_rows.append(csv_row)

    # Append to the global CSV file
    with open(global_csv_path, mode="a+", newline="") as csv_file:
        # Check if existing file has the correct headers
        if csv_exists:
            # Move to beginning of file to read headers
            csv_file.seek(0)
            reader = csv.reader(csv_file)
            try:
                existing_headers = next(reader)

                # If headers don't match, we need to update the file
                if existing_headers != csv_headers:
                    console.print(
                        f"[yellow]Warning: CSV headers mismatch. Updating file format.[/yellow]"
                    )

                    # Read all existing rows
                    csv_file.seek(0)
                    dict_reader = csv.DictReader(csv_file)
                    existing_rows = list(dict_reader)

                    # Fix existing rows to match new headers
                    for row in existing_rows:
                        for header in csv_headers:
                            if header not in row:
                                row[header] = ""

                    # Rewrite the file with correct headers and all rows
                    csv_file.seek(0)
                    csv_file.truncate()
                    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                    writer.writeheader()
                    writer.writerows(existing_rows)

                    # Move to end of file to append new rows
                    csv_file.seek(0, 2)
            except StopIteration:
                # Empty file, just write headers
                csv_file.seek(0)
                writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                writer.writeheader()
        else:
            # New file, write headers
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()

        # Write new rows
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writerows(csv_rows)


async def execute_all_tests(
    config: EchoFireConfig,
    tests_dir: str,
    repeat: int = 5,
    test_name: str = None,
):

    # Generate a global run ID for this test execution
    global_run_id = generate_id(word_count=4)
    console.print(
        f"[bold cyan]Global test run ID:[/bold cyan] [yellow]{global_run_id}[/yellow]"
    )

    # Run all tests
    results = await run_all_tests(
        tests_dir,
        config,
        global_run_id,
        repeat,
        test_name,
    )

    # Print summary
    total = len(results)
    passed = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    # Calculate overall latency statistics
    all_latencies = []
    for result in results:
        latencies = [r.get("latency_ms") for r in result.responses if "latency_ms" in r]
        all_latencies.extend(latencies)

    if all_latencies:
        avg_latency = sum(all_latencies) / len(all_latencies)
        min_latency = min(all_latencies)
        max_latency = max(all_latencies)
        console.rule("[bold]ASR Latency Summary")
        console.print(
            f"[bold cyan]Average ASR Latency:[/bold cyan] {avg_latency:.2f}ms"
        )
        console.print(f"[bold cyan]Min ASR Latency:[/bold cyan] {min_latency:.2f}ms")
        console.print(f"[bold cyan]Max ASR Latency:[/bold cyan] {max_latency:.2f}ms")
        console.print(
            f"[bold cyan]Total Measurements:[/bold cyan] {len(all_latencies)}"
        )

    console.rule("[bold]Test Summary")
    if failed == 0:
        console.print(
            f"[bold green]All tests passed![/bold green] {passed}/{total} tests successful"
        )
    else:
        console.print(
            f"[bold yellow]Test Results:[/bold yellow] [green]{passed}[/green]/[blue]{total}[/blue] tests passed, [red]{failed}[/red] failed"
        )

    # Print detailed assertion summary
    console.rule("[bold]Detailed Assertion Summary")

    for result in results:
        status_color = "green" if result.success else "red"
        status_icon = "✓" if result.success else "✗"

        console.print(
            f"\n[bold {status_color}]{status_icon} Test:[/bold {status_color}] [cyan]{result.test_name}[/cyan] - [bold {status_color}]{'PASSED' if result.success else 'FAILED'}[/bold {status_color}] (iteration {result.iteration + 1}/{repeat}, run ID: {result.run_id})"
        )

        if result.error:
            console.print(f"  [bold red]Error:[/bold red] {result.error}")
            continue

        if not result.assertion_results:
            console.print("  [italic]No assertions defined for this test[/italic]")
            continue

        passed_assertions = [ar for ar in result.assertion_results if ar.passed]
        failed_assertions = [ar for ar in result.assertion_results if not ar.passed]

        console.print(
            f"  [bold]Assertions:[/bold] [green]{len(passed_assertions)}[/green]/[blue]{len(result.assertion_results)}[/blue] passed"
        )

        if failed_assertions:
            console.print("  [bold red]Failed assertions:[/bold red]")
            for i, ar in enumerate(failed_assertions, 1):
                console.print(
                    f"    {i}. [yellow]{ar.assertion.root.description}[/yellow]"
                )
                console.print(f"       [dim]Type:[/dim] {ar.assertion.root.type}")
                console.print(f"       [dim]Details:[/dim] {ar.details}")

    # Exit with non-zero code if any tests failed
    if failed > 0:
        sys.exit(1)
