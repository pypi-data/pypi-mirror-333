# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .llm_step_param import LlmStepParam
from .log_step_param import LogStepParam
from .tool_step_param import ToolStepParam
from .retriever_step_param import RetrieverStepParam

__all__ = ["IngestCreateParams", "Event", "EventIngestTrace"]


class IngestCreateParams(TypedDict, total=False):
    events: Required[Iterable[Event]]
    """Array of events to be ingested, which can be threads or traces."""


class EventIngestTrace(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 datetime when the trace was created."""

    type: Required[Literal["trace"]]
    """Type of the event (always `trace` for traces)."""

    id: str
    """Unique Trace ID (UUID).

    If not provided, it will be generated server-side. We recommend using the same
    ID as you have for the conversation or interaction in your own database.
    """

    metadata: Optional[Dict[str, object]]
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Optional run ID for the trace if this was an Avido triggered run.

    It will be provided in the body of the eval webhook.
    """


Event: TypeAlias = Union[EventIngestTrace, LlmStepParam, ToolStepParam, RetrieverStepParam, LogStepParam]
