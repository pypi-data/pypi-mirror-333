# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["LlmStep", "Token"]


class Token(BaseModel):
    completion_tokens: Optional[float] = FieldInfo(alias="completionTokens", default=None)
    """Number of completion tokens used by the LLM."""

    prompt_tokens: Optional[float] = FieldInfo(alias="promptTokens", default=None)
    """Number of prompt tokens used by the LLM."""


class LlmStep(BaseModel):
    id: str
    """UUID for the step."""

    api_model_id: str = FieldInfo(alias="modelId")
    """Model ID or name used for the LLM call."""

    timestamp: str
    """ISO-8601 datetime for when the step occurred."""

    trace_id: str = FieldInfo(alias="traceId")
    """UUID referencing the parent trace's ID."""

    type: Literal["llm"]

    token: Optional[Token] = None
    """Number of input and output tokens used by the LLM."""

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
    """Arbitrary LLM params (temperature, top_p, etc.)."""
