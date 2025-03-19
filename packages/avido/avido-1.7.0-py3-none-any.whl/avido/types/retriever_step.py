# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["RetrieverStep"]


class RetrieverStep(BaseModel):
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

    query: Union[Dict[str, object], List[object], None] = None
    """Query used for RAG."""

    result: Union[Dict[str, object], List[object], None] = None
    """Retrieved data chunks, if any."""
