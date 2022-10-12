from __future__ import annotations

import ast
from typing import Any, Optional, TYPE_CHECKING

from flask import g, json

from openatlas.database.gis import Gis as Db
from openatlas.models.type import Type
from openatlas.util.util import sanitize

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity
    from openatlas.models.imports import Project


class InvalidGeomException(Exception):
    pass


class Gis:

    @staticmethod
    def get_by_id(id_: int) -> list[dict[str, Any]]:
        return Db.get_by_id(id_)

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
            extra_ids = [
                objects[0].id if objects else 0] \
                + super_id \
                + subunit_ids \
                + sibling_ids
        object_ids = [x.id for x in objects] if objects else []
        place_root = Type.get_hierarchy('Place')
        for row in Db.get_all(extra_ids):
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
            if 'types' in row and row['types']:
                type_ids = ast.literal_eval(f"[{row['types']}]")
                for type_id in list(set(type_ids)):
                    type_ = g.types[type_id]
                    if type_.root and type_.root[0] == place_root.id:
                        item['properties']['objectType'] = \
                            type_.name.replace('"', '\"')
                        break
            if structure \
                    and structure['supers'] \
                    and row['object_id'] == structure['supers'][-1].id:
                extra['supers'].append(item)
            elif row['object_id'] in object_ids:
                selected[shape].append(item)
            elif row['object_id'] in subunit_ids:  # pragma no cover
                extra['subs'].append(item)
            elif row['object_id'] in sibling_ids:  # pragma no cover
                extra['siblings'].append(item)
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
                elif row['object_id'] in subunit_ids:  # pragma no cover
                    extra['subs'].append(polygon_point_item)
                elif row['object_id'] in sibling_ids:  # pragma no cover
                    extra['siblings'].append(polygon_point_item)
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
            if shape not in data or not data[shape]:
                continue  # pragma: no cover
            for item in json.loads(data[shape]):
                if not item['geometry']['coordinates'] \
                        or item['geometry']['coordinates'] == [[]]:
                    continue  # pragma: no cover
                if item['properties']['shapeType'] != 'centerpoint' \
                        and not Db.test_geom(json.dumps(item['geometry'])):
                    raise InvalidGeomException
                Db.insert(
                    shape='linestring' if shape == 'line' else shape,
                    data={
                        'entity_id': entity.id,
                        'name': sanitize(item['properties']['name'], 'text'),
                        'description':
                            sanitize(
                                item['properties']['description'],
                                'text'),
                        'type': item['properties']['shapeType'],
                        'geojson': json.dumps(item['geometry'])})

    @staticmethod
    def insert_import(
            entity: Entity,
            location: Entity,
            project: Project,
            easting: float,
            northing: float) -> None:
        Db.insert_import({
            'entity_id': location.id,
            'description':
                f"Imported centerpoint of {sanitize(entity.name, 'text')} "
                f"from the {sanitize(project.name, 'text')} project",
            'geojson':
                f'{{"type":"Point", "coordinates": [{easting},{northing}]}}'})

    @staticmethod
    def delete_by_entity(entity: Entity) -> None:
        Db.delete_by_entity_id(entity.id)
