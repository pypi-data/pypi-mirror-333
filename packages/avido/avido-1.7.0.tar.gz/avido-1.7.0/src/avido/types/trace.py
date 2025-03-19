# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .run import Run
from .._models import BaseModel

__all__ = ["Trace"]


class Trace(BaseModel):
    id: str
    """Unique Trace ID (UUID)."""

    timestamp: str
    """ISO-8601 datetime when the trace was created."""

    metadata: Optional[Dict[str, object]] = None
    """Arbitrary metadata (e.g., userId, source).

    String inputs are parsed as JSON or wrapped in { raw: val }.
    """

    run: Optional[Run] = None
    """A Run represents a batch of tests triggered by a single task"""
