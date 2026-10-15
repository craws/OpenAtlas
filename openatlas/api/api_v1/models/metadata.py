from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class CaseStudyItem(BaseSchema):
    id: int = Field(
        description="Unique ID of the case study.",
        examples=[42])
    uuid: UUID = Field(
        description="Universally unique identifier of the case study.")
    name: str = Field(
        description="Name or title of the case study.",
        examples=["Cemetery Excavation 2024"])
    description: str | None = Field(
        None,
        description="Detailed description or abstract of the case study.")
    sub_case_studies: list[CaseStudyItem] = Field(
        default_factory=list,
        description="Nested child case studies or sub-projects.")


class CaseStudyListResponse(BaseSchema):
    data: list[CaseStudyItem] = Field(
        description="Hierarchical list of top-level case studies.")


class CaseStudyPath(BaseModel):
    id: int = Field(description="Filter by a specific Case Study ID")
