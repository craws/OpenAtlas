from __future__ import annotations

from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class AgentPath(BaseModel):
    id: int = Field(
        description="Filter by a specific Agent ID")


class AgentItem(BaseModel):
    id: int = Field(
        description="Unique ID of the agent.",
        examples=[123])
    name: str = Field(
        description="Full name or organizational label of the agent.",
        examples=["Jane Doe"])
    class_name: str | None = Field(
        None,
        serialization_alias="class",
        description="The OpenAtlas entity class (e.g. 'person', 'group').",
        examples=["person"])
    description: str | None = Field(
        None,
        description="Short description or biographical note.",
        examples=["Senior Archaeologist and Excavation Director"])


class AgentListResponse(BaseSchema):
    data: list[AgentItem] = Field(
        description="List of registered agents and rights holders.")
