from openatlas.api.api_v1.models.metadata import CaseStudyItem, \
    CaseStudyListResponse

case_study_responses = {
    200: { CaseStudyItem.model_json_schema()},
    404: {
        'description': 'Case study not found',
        'content': {
            'application/json': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {
                            'type': 'string',
                            'example': 'Case study not found'}}}}}}}

case_studies_responses = {200: {CaseStudyListResponse.model_json_schema()}}
