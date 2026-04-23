import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import fiona
from shapely import MultiPolygon
from shapely.geometry import mapping, shape

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.gis import insert_gis

BASE_DIR = Path(__file__).resolve().parent
GPKG_PATH = BASE_DIR / "churches.gpkg"
GPKG_STR = str(GPKG_PATH)


@dataclass
class ChurchRecord:
    osm_id: str
    openatlas_id: int
    name: Optional[str]
    geometry: dict[str, Any]

    @classmethod
    def from_fiona(cls, feature_: dict[str, Any]) -> 'ChurchRecord':
        props = feature_.get('properties', {})
        geom_input = feature_.get('geometry', {})
        poly_obj = shape(geom_input)
        if isinstance(poly_obj, MultiPolygon):
            poly_obj = max(poly_obj.geoms, key=lambda p: p.area)
        clean_geom = mapping(poly_obj)
        return cls(
            osm_id=props.get('osm_id'),
            openatlas_id=props.get('@id'),
            name=props.get('name_2'),
            geometry=clean_geom)


with app.test_request_context():
    app.preprocess_request()

    church_objects: list['ChurchRecord'] = []
    with fiona.open(GPKG_STR, layer=fiona.listlayers(GPKG_STR)[0]) as gpkg:
        for feature in gpkg:
            record = ChurchRecord.from_fiona(feature)
            church_objects.append(record)

    for church in church_objects:
        entity = Entity.get_by_id(church.openatlas_id)
        if not entity:
            continue

        geom = {
            "type": "Feature",
            "geometry": church.geometry,
            "properties": {
                "name": f"OSM: {church.osm_id}",
                "description": "Imported from OpenStreetMap",
                "id": -999999999,
                "shapeType": "shape"}}

        data = {
            'point': '[]',
            'line': '[]',
            'polygon': f'[{json.dumps(geom)}]'}

        insert_gis(entity.location, data)
