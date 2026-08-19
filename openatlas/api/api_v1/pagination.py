import math
from typing import Any
from urllib.parse import urlencode

from flask import request, url_for


def get_pagination(
        endpoint: str,
        total_items: int,
        page: int,
        limit: int,
        **endpoint_kwargs: Any) -> dict[str, Any]:
    base_url = url_for(endpoint, _external=True, **endpoint_kwargs)
    query_params = dict(request.args)

    def page_url(p: int) -> str:
        params = dict(query_params)
        params['page'] = p
        return f'{base_url}?{urlencode(params)}'

    total_pages = max(1, math.ceil(total_items / limit))
    pagination: dict[str, Any] = {
        'total_items': total_items,
        'id': page_url(page),
        'first': page_url(1),
        'last': page_url(total_pages)}
    if page > 1:
        pagination['previous'] = page_url(page - 1)
    if page < total_pages:
        pagination['next'] = page_url(page + 1)
    return pagination
