from openatlas.api.api_v1.models.agent import AgentItem, AgentListResponse
from openatlas.api.api_v1.models.metadata import (
    CaseStudyItem,
    CaseStudyListResponse,
)
from openatlas.api.api_v1.models.util import ErrorResponse

case_studies_response = {200: CaseStudyListResponse}
case_study_response = {
    200: CaseStudyItem,
    404: {
        'description': 'Case study not found',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
agents_response = {200: AgentListResponse}
agent_response = {
    200: AgentItem,
    404: {
        'description': 'Agent not found',
        'content': {
            'application/json': {
                'schema': ErrorResponse.model_json_schema()}}}}
