import argparse
import asyncio
import io
import json
import sys
import traceback
import signal
import ssl
import os
import uuid
from datetime import datetime
from pathlib import Path
import wave
import numpy as np
import yaml
import urllib.parse

from typing import Optional

import sounddevice as sd
import websockets

from rich.align import Align
from rich.console import Console
from rich.console import Group
from rich.layout import Layout
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

# For Pydantic models
from pydantic import ValidationError, TypeAdapter

# Import models from the models directory
from echofire.models.config_model import EchoFireConfig
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
    ErrorResponse,
)

# --------------------------------------------------------
# Utility functions
# --------------------------------------------------------

# A global Rich console instance
console = Console()

# Only store exceptions here for debug mode
DEBUG_EXCEPTIONS = []

# Global flag to track if the first agent output has been received
FIRST_AGENT_OUTPUT_RECEIVED = False


def add_debug_exception(e: Exception):
    """
    Append the full traceback of the given exception into the global DEBUG_EXCEPTIONS list.
    """
    DEBUG_EXCEPTIONS.append(traceback.format_exc())


async def show_error_and_exit(conversation, error_message: str, debug: bool):
    """
    Render the conversation with the debug panel, print the error message,
    wait a few seconds if in debug mode, then exit.
    """
    render_interactive_conversation(conversation, debug=debug)
    console.print(f"[bold red]{error_message}[/bold red]")
    if debug:
        await asyncio.sleep(10)
    sys.exit(1)


# ----------------------------------------------------------------------------
# Sending audio to the server
# ----------------------------------------------------------------------------


async def send_audio(
    websocket,
    audio_queue: asyncio.Queue,
    audio_chunks_queue: asyncio.Queue,
    debug: bool,
    audio_dir: Optional[str] = None,
    sample_rate: int = 16000,
    channels: int = 1,
):
    """
    Continuously get audio chunks from the queue and send them as binary messages over the websocket.
    If audio_dir is not None, add chunks to the shared audio_chunks_queue for utterance creation.
    Only starts saving audio chunks after the first agent output is done.

    Args:
        websocket: The websocket connection
        audio_queue: Queue containing audio chunks from the microphone
        audio_chunks_queue: Shared queue for saving audio chunks
        debug: Whether debug mode is enabled
        audio_dir: Directory to save audio chunks (None if not saving)
        sample_rate: Audio sample rate
        channels: Number of audio channels
    """
    global FIRST_AGENT_OUTPUT_RECEIVED

    try:
        while True:
            try:
                chunk = await audio_queue.get()  # Wait for the next audio chunk
                await websocket.send(chunk)

                # Add to shared audio_chunks_queue for utterance creation if saving is enabled
                # and the first agent output has been received
                if audio_dir is not None and FIRST_AGENT_OUTPUT_RECEIVED:
                    await audio_chunks_queue.put(chunk)
            except asyncio.CancelledError:
                # Clean exit on cancellation
                raise
            except Exception as e:
                if debug:
                    add_debug_exception(e)
                raise
    except asyncio.CancelledError:
        # Clean exit on cancellation
        if debug:
            print("Audio sending task cancelled.")
        return


# ----------------------------------------------------------------------------
# Receiving messages from the server
# ----------------------------------------------------------------------------


async def receive_messages(
    websocket,
    mode: str,
    debug: bool,
    audio_chunks_queue: asyncio.Queue,
    test_dir: Optional[str] = None,
    sample_rate: int = 16000,
    channels: int = 1,
    transcript_file: Optional[str] = None,
):
    """
    Continuously receive messages from the websocket and handle them according to the selected mode (raw or interactive).
    This version strips the "data:" prefix (used by SSE) before parsing the JSON.
    It handles new agent streaming events:
      • "agent.output.delta": incrementally update the assistant message.
      • "agent.output.done": finalize the assistant message and clear any intent message.

    If audio_dir is not None, it will save combined audio files when agent.output.generating is received
    using chunks from the shared audio_chunks_queue.

    Args:
        websocket: The websocket connection
        mode: Display mode ("raw" or "interactive")
        debug: Whether debug mode is enabled
        audio_chunks_queue: Shared queue containing audio chunks
        test_dir: Directory to save test data (None if not saving)
        sample_rate: Audio sample rate
        channels: Number of audio channels
        transcript_file: Path to save transcript (None if not saving)
    """
    global FIRST_AGENT_OUTPUT_RECEIVED

    conversation = []
    utterance_counter = 0
    current_session_dir = None
    transcript_path = None
    transcript_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "conversation": [],
    }

    # Create session directory if saving audio
    if test_dir is not None:
        current_session_dir = Path(test_dir) / "utterances"
        current_session_dir.mkdir(parents=True, exist_ok=True)
        print(f"Saving utterances to: {current_session_dir}")

    # Initialize transcript file if path is provided
    if transcript_file:
        transcript_path = Path(transcript_file)
        # Create parent directories if they don't exist
        if transcript_path.parent:
            transcript_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Will save transcript to: {transcript_path}")

    try:
        while True:
            try:
                raw_msg = await websocket.recv()
            except asyncio.CancelledError:
                # Clean exit on cancellation
                raise
            except Exception as e:
                if debug:
                    add_debug_exception(e)
                await show_error_and_exit(
                    conversation, "Unexpected exception. Terminating.", debug
                )

            if isinstance(raw_msg, bytes):
                decoded_msg = raw_msg.decode("utf-8", errors="replace")
            else:
                decoded_msg = raw_msg

            # Strip "data:" prefix if present (as in SSE streams)
            if decoded_msg.startswith("data:"):
                decoded_msg = decoded_msg.partition("data:")[2].strip()

            if mode == "raw":
                print(decoded_msg)
                continue

            try:
                data = json.loads(decoded_msg)
            except json.JSONDecodeError as e:
                if debug:
                    add_debug_exception(e)
                await show_error_and_exit(
                    conversation, "JSON decode error. Terminating.", debug
                )

            if "error" in data:
                await show_error_and_exit(
                    conversation,
                    f"Error from server: {data['error']['message']}",
                    debug,
                )

            try:
                output = TypeAdapter(AgentOutput).validate_python(data)
            except Exception as e:
                if debug:
                    add_debug_exception(
                        ValueError(
                            f"Unknown message type: {data.get('object', 'unknown')}"
                        )
                    )
                await show_error_and_exit(
                    conversation,
                    f"Unknown message type: {data.get('object', 'unknown')}. Terminating.",
                    debug,
                )

            if isinstance(output, AgentOutputTranscript):
                # Remove any trailing intent status so it doesn't split the transcript.
                if conversation and conversation[-1]["role"] == "intent":
                    conversation.pop()
                if conversation and conversation[-1]["role"] == "user":
                    conversation[-1]["text"] = output.transcript
                else:
                    conversation.append({"role": "user", "text": output.transcript})

                # Save transcript to data structure if enabled
                if transcript_file and output.transcript.strip():
                    # Check if we already have a user message in progress
                    if (
                        transcript_data["conversation"]
                        and transcript_data["conversation"][-1]["role"] == "user"
                    ):
                        # Update the existing user message
                        transcript_data["conversation"][-1]["text"] = output.transcript
                    else:
                        # Add a new user message
                        transcript_data["conversation"].append(
                            {
                                "role": "user",
                                "text": output.transcript,
                                "timestamp": datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S"
                                ),
                            }
                        )

                    # Write the updated YAML file
                    with open(transcript_path, "w") as f:
                        yaml.dump(
                            transcript_data,
                            f,
                            default_flow_style=False,
                            sort_keys=False,
                        )

            elif isinstance(output, AgentOutputDelta):
                # Accumulate delta text into the assistant message
                if (
                    conversation
                    and conversation[-1]["role"] == "assistant"
                    and conversation[-1].get("incomplete", True)
                ):
                    conversation[-1]["text"] += output.delta
                else:
                    conversation.append(
                        {
                            "role": "assistant",
                            "text": output.delta,
                            "incomplete": True,
                        }
                    )

            elif isinstance(output, AgentOutputDone):
                # Finalize the assistant message
                if (
                    conversation
                    and conversation[-1]["role"] == "assistant"
                    and conversation[-1].get("incomplete", True)
                ):
                    conversation[-1]["text"] = output.text  # update with complete text
                    conversation[-1]["incomplete"] = False
                else:
                    conversation.append(
                        {
                            "role": "assistant",
                            "text": output.text,
                            "incomplete": False,
                        }
                    )
                # Clear any intent message (e.g., "<generating...>")
                conversation[:] = [
                    msg for msg in conversation if msg["role"] != "intent"
                ]

                # Save transcript to data structure if enabled
                if transcript_file and output.text.strip():
                    # Add the assistant message
                    transcript_data["conversation"].append(
                        {
                            "role": "assistant",
                            "text": output.text,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )

                    # Write the updated YAML file
                    with open(transcript_path, "w") as f:
                        yaml.dump(
                            transcript_data,
                            f,
                            default_flow_style=False,
                            sort_keys=False,
                        )

                # If this is the first agent output, set the global flag
                if not FIRST_AGENT_OUTPUT_RECEIVED:
                    FIRST_AGENT_OUTPUT_RECEIVED = True
                    if debug:
                        print(
                            "First agent output received. Starting to save audio chunks."
                        )

            elif isinstance(output, AgentOutputWaiting):
                new_status = "<waiting...>"
                if conversation and conversation[-1]["role"] == "intent":
                    conversation[-1]["text"] = new_status
                else:
                    conversation.append({"role": "intent", "text": new_status})

            elif isinstance(output, AgentOutputGenerating):
                new_status = "<generating...>"
                if conversation and conversation[-1]["role"] == "intent":
                    conversation[-1]["text"] = new_status
                else:
                    conversation.append({"role": "intent", "text": new_status})

                # When we receive agent.output.generating, save the combined audio file
                # Only if the first agent output has been received
                if (
                    test_dir is not None
                    and current_session_dir
                    and FIRST_AGENT_OUTPUT_RECEIVED
                ):
                    # Collect all chunks from the queue
                    all_audio_data = bytearray()
                    chunks_collected = 0

                    # Drain the queue to get all chunks
                    while not audio_chunks_queue.empty():
                        try:
                            chunk = audio_chunks_queue.get_nowait()
                            all_audio_data.extend(chunk)
                            chunks_collected += 1
                        except asyncio.QueueEmpty:
                            break

                    # Only save if we collected chunks
                    if chunks_collected > 0:
                        # Create a combined WAV file for the current utterance
                        utterance_file = (
                            current_session_dir
                            / f"utterance_{utterance_counter:04d}.wav"
                        )

                        with wave.open(str(utterance_file), "wb") as wf:
                            wf.setnchannels(channels)
                            wf.setsampwidth(2)  # 16-bit audio
                            wf.setframerate(sample_rate)
                            wf.writeframes(all_audio_data)

                        print(
                            f"Saved utterance to: {utterance_file} ({chunks_collected} chunks)"
                        )

                        # Increment utterance counter
                        utterance_counter += 1

            render_interactive_conversation(conversation, debug=debug)
    except asyncio.CancelledError:
        # Clean exit on cancellation
        if debug:
            print("Message receiving task cancelled.")
        return
    except Exception as e:
        if debug:
            add_debug_exception(e)
        raise


# ----------------------------------------------------------------------------
# Dynamically fitting conversation output to the screen
# ----------------------------------------------------------------------------


def measure_conversation_height(conversation) -> int:
    buffer = io.StringIO()
    temp_console = Console(file=buffer, width=console.size.width, record=True)
    temp_console.print(build_conversation_renderable(conversation))
    text_output = buffer.getvalue()
    return len(text_output.splitlines())


def fit_conversation_to_screen(conversation, debug: bool):
    total_height = console.size.height
    if debug:
        max_convo_height = int(total_height * 0.75) - 4
    else:
        max_convo_height = total_height - 4
    if max_convo_height < 1:
        return []
    convo_subset = conversation[:]
    while convo_subset:
        height_needed = measure_conversation_height(convo_subset)
        if height_needed <= max_convo_height:
            return convo_subset
        convo_subset.pop(0)
    return []


# ----------------------------------------------------------------------------
# Rendering the conversation
# ----------------------------------------------------------------------------


def build_conversation_renderable(conversation):
    if not conversation:
        return Text("No conversation yet.", style="dim")
    items = []
    for msg in conversation:
        role = msg["role"]
        text = msg["text"]
        if role == "user":
            items.append(Text(f"User: {text}", style="bold green"))
        elif role == "assistant":
            items.append(Text("Assistant:", style="bold cyan"))
            items.append(Markdown(text))
        elif role == "intent":
            items.append(Text(text, style="italic yellow"))
        else:
            items.append(Text(f"{role}: {text}"))
    return Group(*items)


def render_interactive_conversation(conversation, debug=False):
    intent_message = None
    non_intent_convo = []
    for msg in conversation:
        if msg["role"] == "intent":
            intent_message = msg["text"]
        else:
            non_intent_convo.append(msg)
    conversation_renderable = build_conversation_renderable(non_intent_convo)
    total_height = console.size.height
    conversation_area_height = total_height - 4 - 1
    if conversation_area_height < 1:
        conversation_area_height = 1
    conversation_align = Align(
        conversation_renderable, vertical="bottom", height=conversation_area_height
    )
    intent_text = Text(
        intent_message if intent_message is not None else "", style="italic yellow"
    )
    intent_align = Align(intent_text, vertical="middle", height=1)
    content_group = Group(conversation_align, intent_align)
    conversation_panel = Panel(
        content_group,
        title="Conversation",
        expand=True,
        padding=(0, 1),
        border_style="white",
    )
    if debug:
        if DEBUG_EXCEPTIONS:
            exception_text = "\n".join(
                f"[bold red]Exception #{i + 1}:[/bold red]\n{exc}"
                for i, exc in enumerate(DEBUG_EXCEPTIONS)
            )
            debug_panel = Panel(
                exception_text,
                title="Exceptions (Debug Mode)",
                expand=True,
                style="red",
            )
        else:
            debug_panel = Panel(
                "No exceptions captured.", title="Debug Mode", style="dim"
            )
        layout = Layout()
        layout.split_column(
            Layout(conversation_panel, name="conversation", ratio=3),
            Layout(debug_panel, name="debug", ratio=1),
        )
        console.print(layout)
    else:
        console.print(conversation_panel)


# ----------------------------------------------------------------------------
# Optional: handle terminal resize (SIGWINCH)
# ----------------------------------------------------------------------------


def handle_winch(signum, frame):
    pass


import signal

signal.signal(signal.SIGWINCH, handle_winch)

# ----------------------------------------------------------------------------
# Audio callback
# ----------------------------------------------------------------------------


def audio_callback(indata, frames, time_, status, loop, audio_queue: asyncio.Queue):
    data_bytes = indata.tobytes()
    loop.call_soon_threadsafe(audio_queue.put_nowait, data_bytes)


# ----------------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------------

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def start_interactive_session(
    mode: str,
    config: EchoFireConfig,
    device: Optional[int] = None,
    save_test: Optional[str] = None,
    config_path: Optional[str] = None,
):
    loop = asyncio.get_running_loop()

    test_dir = None
    transcript_file = None
    # Handle --save-test flag by setting up the save directory in ./tests/
    if save_test:
        # Create the tests directory if it doesn't exist, relative to this file
        tests_dir = config_path.parent / "tests"
        tests_dir.mkdir(exist_ok=True)

        # Create a directory for this test, adding sequence number if needed
        base_test_dir = tests_dir / save_test
        test_dir = base_test_dir
        counter = 1
        while test_dir.exists():
            test_dir = tests_dir / f"{save_test}_{counter}"
            counter += 1
        test_dir.mkdir()

        # Set save_transcript to transcript.json in the test directory
        transcript_file = str(test_dir / "transcript.yaml")
        print(f"Will save transcript to {transcript_file}")

        # Create save directory if it doesn't exist
        os.makedirs(test_dir, exist_ok=True)
        # Save args to file in the test directory
        args_file = test_dir / "session_args.json"
        with open(args_file, "w") as f:
            args_dict = {
                "websocket_url": config.original_websocket_url,
                "debug": config.debug,
                "sample_rate": config.sample_rate,
                "channels": config.channels,
                "device": device,
                "save_test": save_test,
                "system_prompt": config.system_prompt,
            }
            json.dump(args_dict, f, indent=4)
        print(f"Arguments saved to {args_file}")

        # Create a default assertions.yaml file if it doesn't exist
        assertions_file = test_dir / "assertions.yaml"
        if not assertions_file.exists():
            with open(assertions_file, "w") as f:
                f.write(
                    """# Test assertions for evaluating the output transcription
name: {}
description: "Test case for voice agent"
assertions:
  - type: "contains"
    text: "expected phrase"
    description: "The transcription should contain this phrase"
  - type: "llm-as-judge"
    description: "Check if the agent was helpful"
    prompt: "Did the agent provide a helpful response to the user's query?"
    return_type: "boolean"
    condition: "is true"
  - type: "llm-as-judge"
    description: "Rate the agent's politeness"
    prompt: "On a scale of 1-5, rate how polite the agent was in the conversation."
    return_type: "integer"
    condition: "greater than 3"
""".format(
                        save_test
                    )
                )
            print(f"Created default assertions file at {assertions_file}")

    # Hide the terminal cursor
    print("\033[?25l", end="", flush=True)
    render_interactive_conversation([], debug=config.debug)

    audio_queue: asyncio.Queue = asyncio.Queue()
    stream = sd.InputStream(
        samplerate=config.sample_rate,
        channels=config.channels,
        dtype="int16",
        callback=lambda indata, frames, time_, status: audio_callback(
            indata, frames, time_, status, loop, audio_queue
        ),
    )
    stream.start()

    try:
        # Determine if we need SSL based on the URL scheme
        use_ssl = config.websocket_url.startswith("wss://")
        ws_kwargs = {"ssl": ssl_context} if use_ssl else {}
        
        if config.debug:
            print(f"Connecting to WebSocket: {config.websocket_url}")
            print(f"Using SSL: {use_ssl}")
            
        async with websockets.connect(config.websocket_url, **ws_kwargs) as websocket:
            # If a system prompt is provided, send it as an agent.state.configure message
            if config.system_prompt is not None:
                config_msg = AgentStateConfigure(
                    event_id=str(uuid.uuid4()),
                    config_id=str(uuid.uuid4()),
                    answer=AnswerConfig(system_prompt=config.system_prompt),
                )
                await websocket.send(json.dumps(config_msg.model_dump()))
                if config.debug:
                    print("Sent agent.state.configure with system_prompt.")
            else:
                # raise an error
                raise ValueError("No system prompt provided.")

            # Create a shared queue for audio chunks
            audio_chunks_queue = asyncio.Queue()

            # Create tasks but don't start them yet
            send_task = asyncio.create_task(
                send_audio(
                    websocket,
                    audio_queue,
                    audio_chunks_queue,
                    config.debug,
                    save_test,
                    config.sample_rate,
                    config.channels,
                )
            )

            receive_task = asyncio.create_task(
                receive_messages(
                    websocket,
                    mode,
                    config.debug,
                    audio_chunks_queue,
                    test_dir,
                    config.sample_rate,
                    config.channels,
                    transcript_file,
                )
            )

            try:
                # Wait for either task to complete or for KeyboardInterrupt
                await asyncio.gather(send_task, receive_task)
            except asyncio.CancelledError:
                # This will be raised when tasks are cancelled
                raise KeyboardInterrupt
            finally:
                # Cancel both tasks
                send_task.cancel()
                receive_task.cancel()
                # Wait for tasks to finish cancellation
                await asyncio.gather(send_task, receive_task, return_exceptions=True)

    except Exception as e:
        print(f"Error with WebSocket connection: {e}", file=sys.stderr)
        if config.debug:
            add_debug_exception(e)
            console.print("\n[bold red]Captured exceptions (Debug Mode):[/bold red]")
            for idx, exc_text in enumerate(DEBUG_EXCEPTIONS, start=1):
                console.print(f"[bold red]#{idx}[/bold red]\n{exc_text}")
    finally:
        stream.stop()
        print("Audio stream stopped.")
        print("\033[?25h", end="", flush=True)
