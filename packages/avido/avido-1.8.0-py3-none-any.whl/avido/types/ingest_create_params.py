# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "IngestCreateParams",
    "Event",
    "EventIngestTrace",
    "EventIngestLlmStep",
    "EventIngestLlmStepUsage",
    "EventIngestToolStep",
    "EventIngestRetrieverStep",
    "EventIngestLogStep",
]


class IngestCreateParams(TypedDict, total=False):
    events: Required[Iterable[Event]]
    """Array of events to be ingested, which can be threads or traces."""


class EventIngestTrace(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["trace"]]

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary params for the step."""

    reference_id: Annotated[str, PropertyInfo(alias="referenceId")]
    """Unique Trace ID (UUID).

    If not provided, it will be generated server-side. We recommend using the same
    ID as you have for the conversation or interaction in your own database.
    """

    test_id: Annotated[Optional[str], PropertyInfo(alias="testId")]
    """Optional test ID for the trace if this was an Avido triggered run.

    It will be provided in the body of the webhook.
    """


class EventIngestLlmStepUsage(TypedDict, total=False):
    completion_tokens: Annotated[Optional[float], PropertyInfo(alias="completionTokens")]
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Annotated[Optional[float], PropertyInfo(alias="promptTokens")]
    """Number of prompt tokens used by the LLM."""


class EventIngestLlmStep(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["llm"]]

    event: Optional[Literal["start", "end"]]
    """The event type (e.g., 'start', 'end')."""

    input: Union[Dict[str, object], Iterable[object], None]
    """The input for the LLM step."""

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    model_id: Annotated[Optional[str], PropertyInfo(alias="modelId")]
    """The model ID (e.g., 'gpt-4o-2024-08-06')."""

    output: Union[Dict[str, object], Iterable[object], None]
    """The output for the LLM step."""

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary params for the step."""

    trace_id: Annotated[Optional[str], PropertyInfo(alias="traceId")]
    """
    Add the Trace ID to link the step to a trace if no trace is included as an event
    """

    usage: Optional[EventIngestLlmStepUsage]
    """Number of input and output tokens used by the LLM."""


class EventIngestToolStep(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["tool"]]

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary params for the step."""

    tool_input: Annotated[Union[Dict[str, object], Iterable[object], None], PropertyInfo(alias="toolInput")]
    """The input for the tool step."""

    tool_output: Annotated[Union[Dict[str, object], Iterable[object], None], PropertyInfo(alias="toolOutput")]
    """The output for the tool step."""

    trace_id: Annotated[Optional[str], PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestRetrieverStep(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["retriever"]]

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary params for the step."""

    query: Union[Dict[str, object], Iterable[object], None]
    """The query for the retriever step."""

    result: Union[Dict[str, object], Iterable[object], None]
    """The result for the retriever step."""

    trace_id: Annotated[Optional[str], PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


class EventIngestLogStep(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["log"]]

    content: Optional[str]
    """The content for the log step."""

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary params for the step."""

    trace_id: Annotated[Optional[str], PropertyInfo(alias="traceId")]
    """The trace ID (UUID)."""


Event: TypeAlias = Union[
    EventIngestTrace, EventIngestLlmStep, EventIngestToolStep, EventIngestRetrieverStep, EventIngestLogStep
]
