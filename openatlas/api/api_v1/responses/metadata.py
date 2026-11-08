from http import HTTPStatus

from openatlas.api.api_v1.models.agent import AgentItem, AgentListResponse
from openatlas.api.api_v1.models.metadata import \
    CaseStudyItem, CaseStudyListResponse
from openatlas.api.api_v1.models.util import ErrorResponse

case_studies_response = {HTTPStatus.OK: CaseStudyListResponse}
case_study_response = {
    HTTPStatus.OK: CaseStudyItem,
    HTTPStatus.NOT_FOUND: {
        'description': 'Case study not found',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
agents_response = {HTTPStatus.OK: AgentListResponse}
agent_response = {
    HTTPStatus.OK: AgentItem,
    HTTPStatus.NOT_FOUND: {
        'description': 'Agent not found',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
