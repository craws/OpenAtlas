from flask import g
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import abort_not_found, \
    register_error_handlers
from openatlas.api.api_v1.models.agent import AgentItem, AgentListResponse, \
    AgentPath
from openatlas.api.api_v1.models.metadata import CaseStudyItem, \
    CaseStudyListResponse, \
    CaseStudyPath
from openatlas.api.api_v1.openapi_tags import metadata_tag
from openatlas.models.entity import Entity

api_v1_metadata = APIBlueprint(
    'api_v1_metadata',
    __name__,
    url_prefix='/api/1')
register_error_handlers(api_v1_metadata)

def _walk_case_studies(ids: list[int]) -> list[CaseStudyItem]:
    items = []
    for id_ in ids:
        item = g.types[id_]
        items.append(CaseStudyItem(
            id=item.id,
            uuid=item.uuid,
            name=item.name,
            description=item.description,
            sub_case_studies=_walk_case_studies(item.subs)))
    return items

@api_v1_metadata.get(
    '/case-studies',
    summary="Get case studies metadata",
    tags=[metadata_tag],
    responses={200: CaseStudyListResponse})
def get_case_studies():
    case_study_ids = g.types[g.case_study_type.id].subs
    case_studies = _walk_case_studies(case_study_ids)
    return CaseStudyListResponse(case_studies=case_studies).model_dump(
        by_alias=True)

@api_v1_metadata.get(
    '/case-studies/<int:id>',
    summary="Get case study metadata",
    tags=[metadata_tag],
    responses={200: CaseStudyItem})
def get_case_study_by_id(path: CaseStudyPath):
    case_study = g.types[path.id]
    if not case_study:
        abort_not_found(path.id)
    return CaseStudyItem(
        id=case_study.id,
        uuid=case_study.uuid,
        name=case_study.name,
        description=case_study.description,
        sub_case_studies=_walk_case_studies(case_study.subs)
    ).model_dump(by_alias=True)

@api_v1_metadata.get(
    '/agents/',
    summary="Get agents information",
    tags=[metadata_tag],
    responses={200: AgentListResponse})
def get_agents():
    return AgentListResponse(agents=[]).model_dump(by_alias=True)

@api_v1_metadata.get(
    '/agents/<int:id>',
    summary="Get information about an agent",
    tags=[metadata_tag],
    responses={200: AgentItem})
def get_agent_by_id(path: AgentPath):
    entity = Entity.get_by_id(path.id)
    if not entity:
        abort_not_found(path.id)
    return AgentItem(
        name=entity.name,
        type='person' if entity.class_.name == 'person' else 'group',
        description=entity.description).model_dump(by_alias=True)
