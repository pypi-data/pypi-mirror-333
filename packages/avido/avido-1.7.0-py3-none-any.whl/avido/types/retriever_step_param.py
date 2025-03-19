# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["RetrieverStepParam"]


class RetrieverStepParam(TypedDict, total=False):
    id: Required[str]
    """UUID for the step."""

    timestamp: Required[str]
    """ISO-8601 datetime for when the step occurred."""

    trace_id: Required[Annotated[str, PropertyInfo(alias="traceId")]]
    """UUID referencing the parent trace's ID."""

    type: Required[Literal["retriever"]]

    metadata: Optional[Dict[str, object]]
    """Extra metadata about this trace event.

    String values are parsed as JSON if possible.
    """

    query: Union[Dict[str, object], Iterable[object], None]
    """Query used for RAG."""

    result: Union[Dict[str, object], Iterable[object], None]
    """Retrieved data chunks, if any."""
