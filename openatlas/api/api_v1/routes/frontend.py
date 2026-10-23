from typing import Any
from uuid import UUID

from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.entity import resolve_type_ids
from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.frontend import (
    SearchQuery, SearchResponse, SearchResultItem)
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.api.api_v1.openapi_tags import frontend_tag
from openatlas.api.api_v1.responses.frontend import search_response
from openatlas.api.api_v1.util.date_util import get_timespan_dict
from openatlas.api.api_v1.util.pagination import get_pagination
from openatlas.database.api import search_entities_api
from openatlas.models.dates import Dates

api_v1_frontend = APIBlueprint(
    'api_v1_frontend',
    __name__,
    url_prefix='/api/1',
    abp_security=[{'bearerAuth': []}])
register_error_handlers(api_v1_frontend)


@api_v1_frontend.get(
    '/search',
    summary='Search entities with phonetic fuzzy matching and filters',
    tags=[frontend_tag],
    responses=search_response)
def search_entities(query: SearchQuery) -> dict[str, Any]:
    """
    Searches entities across one or all OpenAtlas system classes using
    phonetic matching (`daitch_mokotoff`) when a `search` query is provided,
    ranking exact matches first, prefix matches second, and alphabetical
    matches third. Supports filtering by system class, historical date range,
    type ID/UUID, and case study ID/UUID.
    """
    type_ids = resolve_type_ids(query.type_id)
    case_study_ids = resolve_type_ids(query.case_study)

    if type_ids == [] or case_study_ids == []:
        rows: list[dict[str, Any]] = []
        total = 0
    else:
        classes = (
            [query.entity_class.value]
            if query.entity_class
            else [cls.value for cls in OpenAtlasClassEnum])
        order_by = f'{query.sort_by}_{query.sort}'
        rows, total = search_entities_api(
            classes=classes,
            order_by=order_by,
            limit=query.limit,
            offset=(query.page - 1) * query.limit,
            search_name=query.search,
            start_date=query.start_date,
            end_date=query.end_date,
            type_ids=type_ids,
            case_study_ids=case_study_ids)

    items = [
        SearchResultItem(
            id=row['id'],
            uuid=UUID(str(row['uuid'])),
            name=row['name'],
            system_class=row['openatlas_class_name'],
            description=row['description'],
            timespan=get_timespan_dict(Dates(row)))
        for row in rows]

    pagination = get_pagination(
        'api_v1_frontend.search_entities',
        total,
        query.page,
        query.limit)
    return SearchResponse(
        data=items,
        **pagination).model_dump(by_alias=True)
