# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["LlmStepParam", "Token"]


class Token(TypedDict, total=False):
    completion_tokens: Annotated[Optional[float], PropertyInfo(alias="completionTokens")]
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Annotated[Optional[float], PropertyInfo(alias="promptTokens")]
    """Number of prompt tokens used by the LLM."""


class LlmStepParam(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    model_id: Required[Annotated[str, PropertyInfo(alias="modelId")]]
    """Model ID or name used for the LLM call."""

    timestamp: Required[str]
    """ISO-8601 datetime for when the step occurred."""

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["llm"]]

    token: Optional[Token]
    """Number of input and output tokens used by the LLM."""

    event: Optional[str]
    """Event label (e.g., 'start', 'end'). Specific to LLM traces."""

    input: Union[Dict[str, object], Iterable[object], None]
    """JSON input for this LLM trace event (e.g., the prompt)."""

    metadata: Optional[Dict[str, object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    output: Union[Dict[str, object], Iterable[object], None]
    """JSON describing the output.

    String inputs are parsed or wrapped in { message: val }.
    """

    params: Union[Dict[str, object], Iterable[object], None]
    """Arbitrary LLM params (temperature, top_p, etc.)."""
