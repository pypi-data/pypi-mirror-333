# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Eval", "Definition"]


class Definition(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    modified_at: datetime = FieldInfo(alias="modifiedAt")

    name: str

    type: Literal["GEVAL", "STYLE", "BLACKLIST"]
    """Type of evaluation. Valid options: GEVAL, STYLE, BLACKLIST."""

    global_config: Optional[object] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class Eval(BaseModel):
    id: str
    """Unique identifier of the evaluation"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the evaluation was created"""

    definition: Definition

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the evaluation was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this evaluation"""

    status: Literal["PENDING", "IN_PROGRESS", "PASSED", "COMPLETED", "FAILED"]
    """Status of the evaluation/test.

    Valid options: PENDING, IN_PROGRESS, PASSED, COMPLETED, FAILED.
    """

    results: Optional[object] = None
    """Results of the evaluation (structure depends on eval type)."""
