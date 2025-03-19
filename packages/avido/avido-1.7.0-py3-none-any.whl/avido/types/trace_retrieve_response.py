# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Annotated, TypeAlias

from .trace import Trace
from .._utils import PropertyInfo
from .._models import BaseModel
from .llm_step import LlmStep
from .log_step import LogStep
from .tool_step import ToolStep
from .retriever_step import RetrieverStep

__all__ = ["TraceRetrieveResponse", "Data", "DataStep"]

DataStep: TypeAlias = Annotated[Union[LlmStep, ToolStep, RetrieverStep, LogStep], PropertyInfo(discriminator="type")]


class Data(Trace):
    steps: List[DataStep]


class TraceRetrieveResponse(BaseModel):
    data: Data
    """A trace grouping related steps (e.g. a user-agent interaction or conversation)."""
