# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .topic import Topic
from .._models import BaseModel
from .application import Application

__all__ = ["Task", "Definition"]


class Definition(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    modified_at: str = FieldInfo(alias="modifiedAt")

    name: str

    type: Literal["GEVAL", "STYLE", "BLACKLIST"]
    """Type of evaluation. Valid options: GEVAL, STYLE, BLACKLIST."""

    global_config: Optional[object] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class Task(BaseModel):
    id: str
    """The unique identifier of the task"""

    application: Application
    """Application configuration and metadata"""

    baseline: Optional[float] = None
    """The baseline score of the task"""

    created_at: str = FieldInfo(alias="createdAt")
    """The date and time the task was created"""

    definitions: List[Definition]

    description: str
    """The task description"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """The date and time the task was last updated"""

    title: str
    """The title of the task"""

    topic: Topic
    """Details about a single Topic"""
