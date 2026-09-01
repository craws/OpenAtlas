from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class AgentPath(BaseModel):
    id: int | None = Field(
        None,
        description="Filter by a specific Agent ID")


class AgentItem(BaseSchema):
    name: str
    type: Literal['person', 'group'] = Field(
        ...,
        description="If agent is a person or a group")
    description: str | None = None
    # external_url: list[ExtRefSystem] | None


class AgentListResponse(BaseSchema):
    agents: list[AgentItem]
