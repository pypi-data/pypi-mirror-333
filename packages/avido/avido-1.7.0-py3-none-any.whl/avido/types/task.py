# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .topic import Topic
from .._models import BaseModel
from .application import Application

__all__ = ["Task"]


class Task(BaseModel):
    id: str
    """The unique identifier of the task"""

    application: Application
    """Application configuration and metadata"""

    baseline: Optional[float] = None
    """The baseline score of the task"""

    created_at: datetime = FieldInfo(alias="createdAt")
    """The date and time the task was created"""

    description: str
    """The task description"""

    modified_at: datetime = FieldInfo(alias="modifiedAt")
    """The date and time the task was last updated"""

    title: str
    """The title of the task"""

    topic: Topic
    """Details about a single Topic"""
