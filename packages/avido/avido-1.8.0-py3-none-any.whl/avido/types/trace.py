# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = ["Trace", "Step", "StepLlmStep", "StepLlmStepUsage", "StepToolStep", "StepRetrieverStep", "StepLogStep"]


class StepLlmStepUsage(BaseModel):
    completion_tokens: Optional[float] = FieldInfo(alias="completionTokens", default=None)
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Optional[float] = FieldInfo(alias="promptTokens", default=None)
    """Number of prompt tokens used by the LLM."""


class StepLlmStep(BaseModel):
    id: str
    """UUID for the step."""

    api_model_id: str = FieldInfo(alias="modelId")
    """Model ID or name used for the LLM call."""

    timestamp: str
    """ISO-8601 datetime for when the step occurred."""

    trace_id: str = FieldInfo(alias="traceId")
    """UUID referencing the parent trace's ID."""

    type: Literal["llm"]

    event: Optional[str] = None
    """Event label (e.g., 'start', 'end'). Specific to LLM traces."""

    input: Union[Dict[str, object], List[object], None] = None
    """JSON input for this LLM trace event (e.g., the prompt)."""

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    output: Union[Dict[str, object], List[object], None] = None
    """JSON describing the output.

    String inputs are parsed or wrapped in { message: val }.
    """

    params: Union[Dict[str, object], List[object], None] = None
    """Arbitrary params for the step."""

    usage: Optional[StepLlmStepUsage] = None
    """Number of input and output tokens used by the LLM."""


class StepToolStep(BaseModel):
    id: str
    """UUID for the step."""

    timestamp: str
    """ISO-8601 datetime for when the step occurred."""

    trace_id: str = FieldInfo(alias="traceId")
    """UUID referencing the parent trace's ID."""

    type: Literal["tool"]

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    params: Union[Dict[str, object], List[object], None] = None
    """Arbitrary params for the step."""

    tool_input: Union[Dict[str, object], List[object], None] = FieldInfo(alias="toolInput", default=None)
    """JSON input for the tool call."""

    tool_output: Union[Dict[str, object], List[object], None] = FieldInfo(alias="toolOutput", default=None)
    """JSON output from the tool call."""


class StepRetrieverStep(BaseModel):
    id: str
    """UUID for the step."""

    timestamp: str
    """ISO-8601 datetime for when the step occurred."""

    trace_id: str = FieldInfo(alias="traceId")
    """UUID referencing the parent trace's ID."""

    type: Literal["retriever"]

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    params: Union[Dict[str, object], List[object], None] = None
    """Arbitrary params for the step."""

    query: Union[Dict[str, object], List[object], None] = None
    """Query used for RAG."""

    result: Union[Dict[str, object], List[object], None] = None
    """Retrieved data chunks, if any."""


class StepLogStep(BaseModel):
    id: str
    """UUID for the step."""

    timestamp: str
    """ISO-8601 datetime for when the step occurred."""

    trace_id: str = FieldInfo(alias="traceId")
    """UUID referencing the parent trace's ID."""

    type: Literal["log"]

    content: Optional[str] = None
    """The actual log message for this trace."""

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    params: Union[Dict[str, object], List[object], None] = None
    """Arbitrary params for the step."""


Step: TypeAlias = Annotated[
    Union[StepLlmStep, StepToolStep, StepRetrieverStep, StepLogStep], PropertyInfo(discriminator="type")
]


class Trace(BaseModel):
    id: str
    """Unique Trace ID (UUID)."""

    timestamp: str
    """ISO-8601 datetime when the trace was created."""

    metadata: Optional[Dict[str, object]] = None
    """Arbitrary metadata (e.g., userId, source).

    String inputs are parsed as JSON or wrapped in { raw: val }.
    """

    reference_id: Optional[str] = FieldInfo(alias="referenceId", default=None)
    """
    An optional reference ID to link the trace to an existing conversation or
    interaction in your own database.
    """

    steps: Optional[List[Step]] = None
    """The steps associated with the trace."""

    test_id: Optional[str] = FieldInfo(alias="testId", default=None)
    """The associated Test if this was triggered by an Avido eval"""
