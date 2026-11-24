import math
from typing import Any, Literal
from uuid import UUID

from pydantic import Field, field_validator

from openatlas.api.api_v1.models.util import BaseSchema, TimeSpan
from openatlas.models.overlay import Overlay

BBOX_PARTS_COUNT = 4


class BboxQuery(BaseSchema):
    bbox: str = Field(
        description=(
            'Bounding box as comma-separated WGS 84 coordinates: '
            'min_lon,min_lat,max_lon,max_lat.'),
        json_schema_extra={'example': '16.0,48.0,17.0,49.0'})
    centroid_only: bool = Field(
        False,
        description=(
            'Reduce polygons and linestrings to single center points '
            'to keep payload sizes small on overview maps.'))
    cluster: bool = Field(
        False,
        description=(
            'If true, aggregates nearby spatial geometries into grid '
            'clusters based on the zoom level.'))
    zoom: int | None = Field(
        None,
        ge=0,
        le=25,
        description=(
            'Map zoom level (0-25) controlling cluster grid size when '
            'cluster is true. If omitted, estimated from the bounding box '
            'span.'))

    @field_validator('bbox', mode='before')
    @classmethod
    def validate_bbox(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError(
                'bbox must be a comma-separated string: '
                'min_lon,min_lat,max_lon,max_lat.')
        parts = [part.strip() for part in value.split(',')]
        if len(parts) != BBOX_PARTS_COUNT:
            raise ValueError(
                'bbox must contain exactly 4 comma-separated numbers: '
                'min_lon,min_lat,max_lon,max_lat.')
        try:
            min_lon, min_lat, max_lon, max_lat = (float(p) for p in parts)
        except ValueError as err:
            raise ValueError(
                'bbox coordinates must be valid numbers.') from err
        if not all(
                math.isfinite(coord)
                for coord in (min_lon, min_lat, max_lon, max_lat)):
            raise ValueError('bbox coordinates must be finite numbers.')
        lon_min, lon_max = Overlay.LON_RANGE
        lat_min, lat_max = Overlay.LAT_RANGE
        if not (lon_min <= min_lon <= lon_max
                and lon_min <= max_lon <= lon_max):
            raise ValueError(
                'Longitude values must be between -180 and 180.')
        if not (lat_min <= min_lat <= lat_max
                and lat_min <= max_lat <= lat_max):
            raise ValueError(
                'Latitude values must be between -90 and 90.')
        if min_lon > max_lon:
            raise ValueError(
                'min_lon must be less than or equal to max_lon.')
        if min_lat > max_lat:
            raise ValueError(
                'min_lat must be less than or equal to max_lat.')
        return f'{min_lon},{min_lat},{max_lon},{max_lat}'

    def bounds(self) -> tuple[float, float, float, float]:
        min_lon, min_lat, max_lon, max_lat = (
            float(part) for part in self.bbox.split(','))
        return min_lon, min_lat, max_lon, max_lat


class GeoJsonPoint(BaseSchema):
    type: Literal['Point'] = 'Point'
    coordinates: list[float]


class GeoJsonLineString(BaseSchema):
    type: Literal['LineString'] = 'LineString'
    coordinates: list[list[float]]


class GeoJsonPolygon(BaseSchema):
    type: Literal['Polygon'] = 'Polygon'
    coordinates: list[list[list[float]]]


GeoJsonGeometry = GeoJsonPoint | GeoJsonLineString | GeoJsonPolygon


class GeoJsonFeatureProperties(BaseSchema):
    id: int
    uuid: UUID
    name: str
    system_class: str = Field(
        description='The OpenAtlas system class name.',
        examples=['place', 'feature'])
    description: str | None = None
    timespan: TimeSpan | None = None
    location_id: int | None = None
    geometry_id: int
    geometry_name: str | None = None
    geometry_description: str | None = None
    shape_type: str


class GeoJsonClusterProperties(BaseSchema):
    cluster: Literal[True] = True
    point_count: int = Field(
        description='Number of geometries aggregated in this cluster.',
        examples=[42])
    expansion_bbox: list[float] = Field(
        description=(
            'WGS 84 bounding box [min_lon, min_lat, max_lon, max_lat] '
            'covering all geometries in this cluster.'),
        examples=[[14.1, 46.4, 14.9, 46.8]])


class GeoJsonFeature(BaseSchema):
    type: Literal['Feature'] = 'Feature'
    geometry: GeoJsonGeometry
    properties: GeoJsonFeatureProperties | GeoJsonClusterProperties


class GeoJsonFeatureCollection(BaseSchema):
    type: Literal['FeatureCollection'] = 'FeatureCollection'
    features: list[GeoJsonFeature] = Field(default_factory=list)
