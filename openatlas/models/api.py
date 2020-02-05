import os
from typing import List, Dict, Any

from flask import request, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.geonames import Geonames
from openatlas.models.gis import Gis
from openatlas.models.link import Link
from openatlas.util.util import format_date, get_file_path


class Api:

    @staticmethod
    def get_links(entity: Entity) -> List[Dict[str, str]]:
        links = []
        for link in Link.get_links(entity.id):
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.name.replace(' ', '_')}, )
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.name.replace(' ', '_')}, )

        return links

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, inverse=True):
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                filename = os.path.basename(path) if path else False
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': Api.get_license(link.domain.id),  # Todo: Search for licence
                              'url': url_for('display_file', filename=filename, _external=True)})

        return files

    @staticmethod
    def get_license(entity_id) -> List[Dict[str, str]]:
        file_license = ""
        for link in Link.get_links(entity_id):
            if link.property.code == "P2":
                file_license = link.range.name

        return file_license

    @staticmethod
    def get_entity(id_: int) -> Dict[str, Any]:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        possible_types: dict = {'E53': 'Place', 'E21': 'Actor', 'E74': 'Actor', 'E40': 'Actor', 'E7': 'Event',
                                'E8': 'Event', 'E9': 'Event', 'E33': 'Source', 'E31': 'Document', 'E84': 'Object',
                                'E18': 'FeatureCollection'}  # Todo: find better vocabulary for types
        type_ = 'unknown'
        for t in possible_types:
            if t == entity.class_.code:
                type_ = possible_types.get(t)

        nodes = []
        for node in entity.nodes:
            nodes.append({'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name})
        geo = Geonames.get_geonames_link(entity)
        data: dict = {
            'type': type_,
            '@context': app.config['API_SCHEMA'],
            'features': [{
                '@id': url_for('entity_view', id_=entity.id, _external=True),
                'type': entity.system_type,
                'properties': {'title': entity.name},
                'when': {'timespans': [{
                    'start': {'earliest': format_date(entity.begin_from),
                              'latest': format_date(entity.begin_to),
                              'comment': entity.begin_comment},
                    'end': {'earliest': format_date(entity.end_from),
                            'latest': format_date(entity.end_to),
                            'comment': entity.end_comment}}]},
                'types': nodes,
                'relations': Api.get_links(entity),
                'descriptions': [
                    {'@id': request.base_url,
                     'value': entity.description}],
                'depictions': [
                    Api.get_file(entity)]}]}

        if type_ == 'FeatureCollection':
            link_type = geo.type.name if geo else ''
            identifier = app.config['GEONAMES_VIEW_URL'] + geo.domain.name if geo else ''
            data['features'].append({'links': [{'type': link_type, 'identifier': identifier}]})

            geometries = []
            for geo in Gis.get_by_id(entity.location.id):
                geometries.append({
                    'type': geo['shape'],
                    'coordinates': geo['geometry']['coordinates'],
                    'classification': geo['type'],
                    'description': geo['description'],
                    'title': geo['name']}
                )
            data['features'].append({'geometry': {
                'type': 'GeometryCollection',
                'geometries': geometries}})

        return data
