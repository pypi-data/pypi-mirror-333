# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .task import Task
from .._models import BaseModel

__all__ = ["Run"]


class Run(BaseModel):
    id: str
    """Unique identifier of the run"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """When the run was created"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """When the run was last modified"""

    status: Literal["PENDING", "IN_PROGRESS", "PASSED", "COMPLETED", "FAILED"]
    """Status of the evaluation/test.

    Valid options: PENDING, IN_PROGRESS, PASSED, COMPLETED, FAILED.
    """

    task: Task
    """
    A task that represents a specific job-to-be-done by the LLM in the user
    application.
    """

    result: Optional[Literal["PASSED", "FAILED"]] = None
    """Result of the run (if completed)"""
