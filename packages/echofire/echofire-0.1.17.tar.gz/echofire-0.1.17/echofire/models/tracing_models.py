"""
Pydantic models for trace and span data structures.
"""

from datetime import datetime, UTC
from enum import Enum
import random
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator

# OpenTelemetry ID constants
SPAN_ID_LENGTH = 8  # 8 bytes, 16 hex chars
TRACE_ID_LENGTH = 16  # 16 bytes, 32 hex chars

def generate_trace_id() -> str:
    """Generate a trace ID as a 32-character hex string."""
    return '{:032x}'.format(random.getrandbits(128))

def generate_span_id() -> str:
    """Generate a span ID as a 16-character hex string."""
    return '{:016x}'.format(random.getrandbits(64))


class SpanKind(str, Enum):
    """Enum representing the kind of span in a trace.
    
    The span kind describes the relationship between the span, its parents, and its children in a Trace.
    It indicates whether the span represents an internal operation, a server operation, a client operation,
    or a message bus operation (producer/consumer).

    Kinds:
        INTERNAL: Default value. Represents operations that happen within a service, such as data processing,
                 computation, or internal state changes. Use for operations that don't cross service boundaries.
                 Example: Processing audio data, evaluating assertions, or calculating metrics.

        SERVER: Represents the handling of an incoming request from a remote component. The span documents 
               the server-side handling of an RPC or other remote request. The parent span is typically a 
               CLIENT span from a remote service.
               Example: Handling an incoming websocket connection or HTTP request.

        CLIENT: Represents a synchronous outgoing request to a remote service. The span documents the client-side
               of an RPC or other remote API call. May have a SERVER span as its child.
               Example: Making an API call to an LLM service or establishing a websocket connection.

        PRODUCER: Represents the creation or queueing of a message to be processed asynchronously by a CONSUMER.
                 Used when sending messages/events that may be handled later.
                 Example: Sending audio data over a websocket or publishing a message to a queue.

        CONSUMER: Represents the processing of a message received asynchronously from a PRODUCER.
                 Used when handling messages/events that were sent earlier.
                 Example: Processing received websocket messages or consuming messages from a queue.
    """
    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class SpanStatus(str, Enum):
    """Enum representing the status of a span."""
    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


class Event(BaseModel):
    """Model representing an event that occurred during a span."""
    name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    attributes: Dict[str, Any] = Field(default_factory=dict)


class Link(BaseModel):
    """Model representing a link to another span."""
    trace_id: str  # 32-char hex string
    span_id: str   # 16-char hex string
    attributes: Dict[str, Any] = Field(default_factory=dict)


class W3CTraceContext(BaseModel):
    """W3C Trace Context format for trace propagation."""
    version: str = "00"
    trace_id: str  # 32-char hex string
    span_id: str   # 16-char hex string
    trace_flags: str = "00"  # 2-char hex string
    
    @property
    def traceparent(self) -> str:
        """Get the traceparent header value."""
        return f"{self.version}-{self.trace_id}-{self.span_id}-{self.trace_flags}"
    
    @classmethod
    def from_traceparent(cls, traceparent: str) -> "W3CTraceContext":
        """Create a W3CTraceContext from a traceparent header."""
        parts = traceparent.split("-")
        if len(parts) != 4:
            raise ValueError(f"Invalid traceparent format: {traceparent}")
        return cls(
            version=parts[0],
            trace_id=parts[1],
            span_id=parts[2],
            trace_flags=parts[3]
        )


class Span(BaseModel):
    """
    Model representing a single operation within a trace.
    
    A span represents a single operation or unit of work in a distributed system.
    Spans can be nested to form a trace tree. Each span is identified by a unique
    span_id and is associated with a trace via trace_id.
    """
    span_id: str = Field(default_factory=generate_span_id)  # 16-char hex string
    trace_id: str  # 32-char hex string
    parent_span_id: Optional[str] = None  # 16-char hex string
    name: str
    kind: SpanKind = SpanKind.INTERNAL
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_time: Optional[datetime] = None
    status: SpanStatus = SpanStatus.UNSET
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Event] = Field(default_factory=list)
    links: List[Link] = Field(default_factory=list)
    
    # Additional metadata that might be useful
    service_name: Optional[str] = None
    resource: Optional[str] = None
    
    # OpenTelemetry specific fields
    instrumentation_scope: Optional[Dict[str, str]] = None
    sampled: bool = True
    dropped_attributes_count: int = 0
    dropped_events_count: int = 0
    dropped_links_count: int = 0
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate the duration of the span in milliseconds."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an event to the span.
        
        Args:
            name: The name of the event
            attributes: Optional attributes for the event
        """
        self.events.append(Event(
            name=name,
            timestamp=datetime.now(UTC),
            attributes=attributes or {},
        ))
    
    def set_status(self, status: SpanStatus, description: Optional[str] = None) -> None:
        """
        Set the status of the span.
        
        Args:
            status: The status to set
            description: Optional description for the status
        """
        self.status = status
        if description:
            self.attributes["status.description"] = description
    
    def end(self, end_time: Optional[datetime] = None) -> None:
        """
        End the span.
        
        Args:
            end_time: Optional explicit end time
        """
        self.end_time = end_time or datetime.now(UTC)
    
    def to_w3c_context(self) -> W3CTraceContext:
        """Convert to W3C Trace Context format."""
        trace_flags = "01" if self.sampled else "00"
        return W3CTraceContext(
            trace_id=self.trace_id,
            span_id=self.span_id,
            trace_flags=trace_flags
        )
    
    def to_otlp(self) -> Dict[str, Any]:
        """Convert to OpenTelemetry protocol (OTLP) format."""
        status_code = {
            SpanStatus.OK: 1,     # OK in OTLP
            SpanStatus.ERROR: 2,  # ERROR in OTLP
            SpanStatus.UNSET: 0   # UNSET in OTLP
        }[self.status]
        
        # Convert to nanoseconds for OTLP
        start_time_ns = int(self.start_time.timestamp() * 1_000_000_000)
        end_time_ns = None
        if self.end_time:
            end_time_ns = int(self.end_time.timestamp() * 1_000_000_000)
        
        result = {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "trace_state": "",
            "parent_span_id": self.parent_span_id or "",
            "name": self.name,
            "kind": self.kind.upper(),  # OTLP uses uppercase
            "start_time_unix_nano": start_time_ns,
            "end_time_unix_nano": end_time_ns,
            "attributes": [{"key": k, "value": {"string_value": str(v)} if isinstance(v, (str, int, float, bool)) else {"string_value": str(v)}} 
                           for k, v in self.attributes.items()],
            "dropped_attributes_count": self.dropped_attributes_count,
            "events": [
                {
                    "time_unix_nano": int(event.timestamp.timestamp() * 1_000_000_000),
                    "name": event.name,
                    "attributes": [{"key": k, "value": {"string_value": str(v)}} for k, v in event.attributes.items()],
                    "dropped_attributes_count": 0
                } for event in self.events
            ],
            "dropped_events_count": self.dropped_events_count,
            "links": [
                {
                    "trace_id": link.trace_id,
                    "span_id": link.span_id,
                    "attributes": [{"key": k, "value": {"string_value": str(v)}} for k, v in link.attributes.items()],
                    "dropped_attributes_count": 0
                } for link in self.links
            ],
            "dropped_links_count": self.dropped_links_count,
            "status": {
                "code": status_code,
                "message": self.attributes.get("status.description", "")
            }
        }
        
        if self.service_name:
            result["service_name"] = self.service_name
            
        return result
    
    @classmethod
    def from_w3c_context(cls, context: W3CTraceContext, name: str, **kwargs) -> "Span":
        """Create a Span from W3C Trace Context."""
        sampled = context.trace_flags == "01"
        return cls(
            trace_id=context.trace_id,
            span_id=generate_span_id(),  # Generate a new span ID
            name=name,
            sampled=sampled,
            **kwargs
        )


class Trace(BaseModel):
    """
    Model representing a complete trace.
    
    A trace represents an end-to-end request flow through the system. It consists
    of one or more spans that show the path and processing of a request.
    """
    trace_id: str = Field(default_factory=generate_trace_id)  # 32-char hex string
    name: Optional[str] = None
    spans: List[Span] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    end_time: Optional[datetime] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate the duration of the trace in milliseconds."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() * 1000
    
    @property
    def root_span(self) -> Optional[Span]:
        """Get the root span of the trace."""
        for span in self.spans:
            if span.parent_span_id is None:
                return span
        return None if not self.spans else self.spans[0]
    
    def add_span(self, span: Span) -> None:
        """
        Add a span to the trace.
        
        Args:
            span: The span to add
        """
        if span.trace_id != self.trace_id:
            raise ValueError(f"Span trace_id {span.trace_id} does not match trace_id {self.trace_id}")
        self.spans.append(span)
    
    def end(self, end_time: Optional[datetime] = None) -> None:
        """
        End the trace.
        
        Args:
            end_time: Optional explicit end time
        """
        self.end_time = end_time or datetime.now(UTC)
        # Also end any spans that haven't been ended
        for span in self.spans:
            if span.end_time is None:
                span.end(self.end_time)
    
    def to_otlp(self) -> Dict[str, Any]:
        """Convert to OpenTelemetry protocol (OTLP) format."""
        return {
            "resource_spans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": k, "value": {"string_value": str(v)}} 
                            for k, v in self.attributes.items()
                        ]
                    },
                    "scope_spans": [
                        {
                            "scope": {
                                "name": self.name or "unnamed_trace",
                                "version": "1.0.0",
                            },
                            "spans": [span.to_otlp() for span in self.spans]
                        }
                    ]
                }
            ]
        }
