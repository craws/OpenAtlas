from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.agent import AgentItem, AgentListResponse, AgentPath
from openatlas.api.api_v1.models.metadata import CaseStudyItem, \
    CaseStudyListResponse, \
    CaseStudyPath
from openatlas.api.api_v1.openapi_tags import metadata_tag

api_v1_metadata = APIBlueprint('metadata', __name__, url_prefix='/api/1')
register_error_handlers(api_v1_metadata)

@api_v1_metadata.get(
    '/case-studies',
    summary="Get case studies metadata",
    tags=[metadata_tag],
    responses={200: CaseStudyListResponse})
def get_case_studies():
    pass

@api_v1_metadata.get(
    '/case-studies/<int:id>',
    summary="Get case study metadata",
    tags=[metadata_tag],
    responses={200: CaseStudyItem})
def get_case_study_by_id(path: CaseStudyPath):

    pass

@api_v1_metadata.get(
    '/agents/',
    summary="Get agents information",
    tags=[metadata_tag],
    responses={200: AgentListResponse})
def get_agetns():
    pass

@api_v1_metadata.get(
    '/agents/<int:id>',
    summary="Get information about an agent",
    tags=[metadata_tag],
    responses={200: AgentItem})
def get_agent_by_id(path: AgentPath):

    pass

