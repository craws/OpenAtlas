import json
import math
from typing import Any

from flask import g
from flask_openapi3 import APIBlueprint

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.models.geographic import BboxQuery
from openatlas.api.api_v1.openapi_tags import geographic_tag
from openatlas.api.api_v1.responses.geographic import bbox_response
from openatlas.api.api_v1.util.date_util import get_timespan_dict
from openatlas.database.api import get_by_bbox, get_clustered_by_bbox
from openatlas.models.dates import Dates

WEB_MERCATOR_CIRCUMFERENCE = 40075016.68557849
TILE_SIZE = 256
MAX_ZOOM = 25
DEFAULT_CLUSTER_RADIUS = 50
FULL_LON_SPAN = 360.0

api_v1_geographic = APIBlueprint(
    'api_v1_geographic',
    __name__,
    url_prefix='/api/1/geographic',
    abp_security=[{'bearerAuth': []}])
register_error_handlers(api_v1_geographic)


def estimate_zoom(bbox: tuple[float, float, float, float]) -> int:
    min_lon, min_lat, max_lon, max_lat = bbox
    span = max(max_lon - min_lon, max_lat - min_lat)
    if span <= 0:
        return MAX_ZOOM
    return max(0, min(MAX_ZOOM, round(math.log2(FULL_LON_SPAN / span)) + 1))


def grid_size_meters(zoom: int, cluster_radius: int) -> float:
    meters_per_pixel = WEB_MERCATOR_CIRCUMFERENCE / (TILE_SIZE * (2 ** zoom))
    return meters_per_pixel * max(1, cluster_radius)


def row_to_feature(row: dict[str, Any]) -> dict[str, Any]:
    has_dates = (
        row['begin_from']
        or row['begin_to']
        or row['begin_comment']
        or row['end_from']
        or row['end_to']
        or row['end_comment'])
    timespan = get_timespan_dict(Dates(row)) if has_dates else None
    return {
        'type': 'Feature',
        'geometry': json.loads(row['geometry']),
        'properties': {
            'id': row['id'],
            'uuid': str(row['uuid']),
            'name': row['name'],
            'systemClass': row['openatlas_class_name'],
            'description': row['description'],
            'timespan': timespan.model_dump(by_alias=True)
            if timespan else None,
            'locationId': row['location_id'],
            'geometryId': row['geometry_id'],
            'geometryName': row['geometry_name'],
            'geometryDescription': row['geometry_description'],
            'shapeType': row['shape_type']}}


def row_to_cluster_feature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        'type': 'Feature',
        'geometry': json.loads(row['geometry']),
        'properties': {
            'cluster': True,
            'pointCount': row['point_count'],
            'expansionBbox': [
                row['min_lon'],
                row['min_lat'],
                row['max_lon'],
                row['max_lat']]}}


@api_v1_geographic.get(
    '/bbox',
    summary='Get spatial entities within a bounding box',
    tags=[geographic_tag],
    responses=bbox_response)  # type: ignore[arg-type]
def get_bbox(query: BboxQuery) -> dict[str, Any]:
    """
    Returns all spatial entities intersecting a rectangular map viewport
    (`min_lon,min_lat,max_lon,max_lat` in WGS 84 / EPSG:4326) as a GeoJSON
    FeatureCollection. When `centroidOnly` (`centroid_only`) is true, polygons
    and linestrings are reduced to single center points to keep overview map
    payloads small. When `cluster` is true, nearby geometries are aggregated
    into grid clusters according to `zoom` (or estimated from `bbox`), falling
    back to individual features at `map_cluster_disable_at_zoom` and above.
    """
    bbox = query.bounds()
    if query.cluster:
        zoom = query.zoom if query.zoom is not None else estimate_zoom(bbox)
        disable_at = int(
            g.settings.get('map_cluster_disable_at_zoom', 0) or 0)
        if disable_at <= 0 or zoom < disable_at:
            radius = int(
                g.settings.get(
                    'map_cluster_max_radius',
                    DEFAULT_CLUSTER_RADIUS) or DEFAULT_CLUSTER_RADIUS)
            rows = get_clustered_by_bbox(
                bbox,
                grid_size_meters(zoom, radius),
                centroid_only=query.centroid_only)
            return {
                'type': 'FeatureCollection',
                'features': [
                    row_to_cluster_feature(row)
                    if row['point_count'] > 1
                    else row_to_feature(row)
                    for row in rows]}

    rows = get_by_bbox(bbox, centroid_only=query.centroid_only)
    return {
        'type': 'FeatureCollection',
        'features': [row_to_feature(row) for row in rows]}
