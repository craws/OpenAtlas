from __future__ import annotations

from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class AgentPath(BaseModel):
    id: int | None = Field(
        None,
        description="Filter by a specific Agent ID")


class AgentItem(BaseModel):
    id: int
    name: str
    class_name: str = Field(
        serialization_alias="class",
        description="The OpenAtlas entity class.")
    description: str | None = Field(
        description="Short description or biographical note.")
    # todo: external_url: list[ExtRefSystem] | None


class AgentListResponse(BaseSchema):
    agents: list[AgentItem]
