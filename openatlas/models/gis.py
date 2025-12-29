from __future__ import annotations

import ast
import re
from collections import defaultdict
from typing import Any, Optional, TYPE_CHECKING

from flask import g, json

from openatlas import app
from openatlas.database import gis as db
from openatlas.display.util2 import sanitize

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


class InvalidGeomException(Exception):
    pass


class Gis:
    @staticmethod
    def get_by_id(id_: int) -> list[dict[str, Any]]:
        return db.get_by_id(id_)

    @staticmethod
    def get_by_entities(
            entities: list[Entity]) -> defaultdict[int, list[dict[str, Any]]]:
        return db.get_by_entity_ids([e.id for e in entities])

    @staticmethod
    def get_centroids_by_entities(
            entities: list[Entity]) -> defaultdict[int, list[Any]]:
        return db.get_centroids_by_entities([e.id for e in entities])

    @staticmethod
    def get_wkt_by_id(id_: int) -> list[dict[str, Any]]:
        return db.get_wkt_by_id(id_)

    @staticmethod
    def get_all(
            objects: Optional[list[Entity]] = None,
            structure: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        if not objects:
            objects = []
        all_: dict[str, list[Any]] = {
            'point': [],
            'linestring': [],
            'polygon': []}
        extra: dict[str, list[Any]] = {
            'supers': [],
            'subs': [],
            'siblings': []}
        selected: dict[str, list[Any]] = {
            'point': [],
            'linestring': [],
            'polygon': [],
            'polygon_point': []}

        # Include GIS of subunits which would be otherwise omitted
        subunit_ids = []
        sibling_ids = []
        extra_ids = [0]
        if structure:
            subunit_ids = [e.id for e in structure['subunits']]
            sibling_ids = [e.id for e in structure['siblings']]
            super_id = [structure['supers'][-1].id] \
                if structure['supers'] else []
            extra_ids = [objects[0].id if objects else 0] \
                + super_id \
                + subunit_ids \
                + sibling_ids
        object_ids = [x.id for x in objects] if objects else []
        for row in db.get_all(extra_ids):
            description = row['description'].replace('"', '\"') \
                if row['description'] else ''
            object_desc = row['object_desc'].replace('"', '\"') \
                if row['object_desc'] else ''
            if row['point']:
                shape = 'point'
                geojson = row['point']
            elif row['linestring']:
                shape = 'linestring'
                geojson = row['linestring']
            else:
                shape = 'polygon'
                geojson = row['polygon']
            item = {
                'type': 'Feature',
                'geometry': json.loads(geojson),
                'properties': {
                    'objectId': row['object_id'],
                    'objectName': row['object_name'].replace('"', '\"'),
                    'objectDescription': object_desc,
                    'locationId': row['location_id'],
                    'id': row['id'],
                    'name': row['name'].replace('"', '\"')
                    if row['name'] else '',
                    'description': description,
                    'shapeType': row['type']}}
            color_map = app.config['MAP_TYPE_COLOR']
            item["properties"]["color"] = color_map.get('default')
            if 'types' in row and row['types']:
                type_ids = ast.literal_eval(f"[{row['types']}]")
                for id_, color in color_map.items():
                    if id_ != 'default' \
                            and int(id_) in type_ids \
                            and re.match(r"^(#)?[A-Fa-f0-9]+$", color):
                        item["properties"]["color"] = color  # pragma: no cover
                        break  # pragma: no cover
                for type_id in list(set(type_ids)):
                    type_ = g.types[type_id]
                    if type_.root and g.types[type_.root[0]].name == 'Place':
                        item['properties']['objectType'] = \
                            type_.name.replace('"', '\"')
                        break
            if structure \
                    and structure['supers'] \
                    and row['object_id'] == structure['supers'][-1].id:
                extra['supers'].append(item)
            if row['object_id'] in object_ids:
                selected[shape].append(item)
            elif row['object_id'] in subunit_ids:
                extra['subs'].append(item)  # pragma: no cover
            elif row['object_id'] in sibling_ids:
                extra['siblings'].append(item)  # pragma: no cover
            else:
                all_[shape].append(item)
            if row['polygon_point']:
                polygon_point_item = dict(item)  # Make a copy
                polygon_point_item['geometry'] = json.loads(
                    row['polygon_point'])
                if row['object_id'] in object_ids:
                    selected['polygon_point'].append(polygon_point_item)
                elif row['object_id'] \
                        and structure \
                        and structure['supers'] \
                        and row['object_id'] == structure['supers'][-1].id:
                    extra['supers'].append(polygon_point_item)
                elif row['object_id'] in subunit_ids:
                    extra['subs'].append(
                        polygon_point_item)  # pragma: no cover
                elif row['object_id'] in sibling_ids:
                    extra['siblings'].append(
                        polygon_point_item)  # pragma: no cover
                else:
                    all_['point'].append(polygon_point_item)
        return {
            'gisPointAll': json.dumps(all_['point']),
            'gisPointSelected': json.dumps(selected['point']),
            'gisPointSupers': json.dumps(extra['supers']),
            'gisPointSubs': json.dumps(extra['subs']),
            'gisPointSibling': json.dumps(extra['siblings']),
            'gisLineAll': json.dumps(all_['linestring']),
            'gisLineSelected': json.dumps(selected['linestring']),
            'gisPolygonAll': json.dumps(all_['polygon']),
            'gisPolygonSelected': json.dumps(selected['polygon']),
            'gisPolygonPointSelected': json.dumps(selected['polygon_point']),
            'gisAllSelected': json.dumps(
                selected['polygon']
                + selected['linestring']
                + selected['point'])}

    @staticmethod
    def insert(entity: Entity, data: dict[str, Any]) -> None:
        for shape in ['point', 'line', 'polygon']:
            if not data.get(shape):
                continue
            for item in json.loads(data[shape]):
                if item['properties']['shapeType'] != 'centerpoint' \
                        and not db.test_geom(json.dumps(item['geometry'])):
                    raise InvalidGeomException
                db.insert(
                    shape='linestring' if shape == 'line' else shape,
                    data={
                        'entity_id': entity.id,
                        'name': sanitize(item['properties']['name']),
                        'description':
                            sanitize(item['properties']['description']),
                        'type': item['properties']['shapeType'],
                        'geojson': json.dumps(item['geometry'])})

    @staticmethod
    def delete_by_entity(entity: Entity) -> None:
        db.delete_by_entity_id(entity.id)
