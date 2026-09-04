from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from openatlas.api.api_v1.models.util import BaseSchema


class CaseStudyItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    description: str | None = None
    sub_case_studies: list[CaseStudyItem] = Field(default_factory=list)
    # profile_image: FileItem
    # principal_investigators: list[str] = Field(default_factory=list)
    # employees: list[str] = Field(default_factory=list)
    # references: list[ReferenceItem] = Field(default_factory=list)
    # ext_references: list[ExtReferenceItem] = Field(default_factory=list)


class CaseStudyListResponse(BaseSchema):
    case_studies: list[CaseStudyItem]


class CaseStudyPath(BaseModel):
    id: int = Field(
        ...,
        description="Filter by a specific Case Study ID")
