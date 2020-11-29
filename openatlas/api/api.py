import ast
from typing import Any, Dict, List, Optional, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.error import APIError
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference import Reference
from openatlas.util.display import format_date, get_file_path


class Api:

    @staticmethod
    def to_camelcase(string: str) -> str:  # pragma: nocover
        if not string:
            return ''
        words = string.split(' ')
        return words[0] + ''.join(x.title() for x in words[1:])

    @staticmethod
    def get_links(entity: Entity) -> List[Dict[str, str]]:
        links = []
        for link in Link.get_links(entity.id):
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_'
                                          + link.property.i18n['en'].replace(' ', '_')})

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + 'i_'
                                          + link.property.i18n['en'].replace(' ', '_')})
        return links

    @staticmethod
    def get_file(entity: Entity) -> Optional[List[Dict[str, str]]]:
        files = []
        for link in Link.get_links(entity.id, codes="P67", inverse=True):  # pragma: nocover
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': Api.get_license(link.domain.id),
                              'url': url_for('display_file_api',
                                             filename=path.name,
                                             _external=True) if path else "N/A"})
        return files if files else None

    @staticmethod
    def get_license(entity_id: int) -> str:  # pragma: nocover
        file_license = ""
        for link in Link.get_links(entity_id):
            if link.property.code == "P2":
                file_license = link.range.name
        return file_license

    @staticmethod
    def get_node(entity: Entity) -> Optional[List[Dict[str, str]]]:
        nodes = []
        for node in entity.nodes:
            nodes_dict = {'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name}
            for link in Link.get_links(entity.id):
                if link.range.id == node.id and link.description:  # pragma: nocover
                    nodes_dict['value'] = link.description
                    if link.range.id == node.id and node.description:
                        nodes_dict['unit'] = node.description
            if 'unit' not in nodes_dict and node.description:
                nodes_dict['description'] = node.description

            hierarchy = []
            for root in node.root:
                hierarchy.append(g.nodes[root].name)  # pragma: nocover
            hierarchy.reverse()
            nodes_dict['hierarchy'] = ' > '.join(map(str, hierarchy))
            nodes.append(nodes_dict)

        return nodes if nodes else None

    @staticmethod
    def get_time(entity: Entity) -> Dict[str, Any]:
        time = {}
        if entity.begin_from:
            start = {'earliest': format_date(entity.begin_from)}
            if entity.begin_to:
                start['latest'] = format_date(entity.begin_to)
            if entity.begin_comment:
                start['comment'] = entity.begin_comment
            time['start'] = start
        if entity.end_from:
            end = {'earliest': format_date(entity.end_from)}
            if entity.end_to:
                end['latest'] = format_date(entity.end_to)
            if entity.end_comment:
                end['comment'] = entity.end_comment
            time['end'] = end
        return time

    @staticmethod
    def get_geom_by_entity(entity: Entity) -> Union[Dict[str, Any], str]:
        if entity.class_.code != 'E53':  # pragma: nocover
            return 'Wrong class'
        geom = []
        for shape in ['point', 'polygon', 'linestring']:
            sql = """
                    SELECT
                        {shape}.id,
                        {shape}.name,
                        {shape}.description,
                        public.ST_AsGeoJSON({shape}.geom) AS geojson
                    FROM model.entity e
                    JOIN gis.{shape} {shape} ON e.id = {shape}.entity_id
                    WHERE e.id = %(entity_id)s;""".format(shape=shape)
            g.execute(sql, {'entity_id': entity.id})
            for row in g.cursor.fetchall():
                test = ast.literal_eval(row.geojson)
                test['title'] = row.name.replace('"', '\"') if row.name else ''
                test['description'] = row.description.replace('"',
                                                              '\"') if row.description else ''
                geom.append(test)
        if len(geom) == 1:
            return geom[0]
        else:
            return {'type': 'GeometryCollection', 'geometries': geom}

    @staticmethod
    def get_external(entity: Entity) -> Optional[List[Dict[str, Union[str, Any]]]]:
        ref = []
        for external in g.external:
            reference = Reference.get_link(entity, external)
            if reference:
                ref.append({'identifier': g.external[external]['url'] + reference.domain.name,
                            'type': Api.to_camelcase(reference.type.name)})
        return ref if ref else None

    @staticmethod
    def get_entity_by_id(id_: int) -> Entity:
        try:
            int(id_)
        except Exception:
            raise APIError('Invalid ID: ' + str(id_), status_code=404, payload="404b")
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            raise APIError('Entity ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                           payload="404a")
        return entity

    @staticmethod
    def get_entity(entity: Entity, meta: Dict[str, Any]) -> Dict[str, Any]:
        type_ = 'FeatureCollection'

        class_code = ''.join(entity.class_.code + " " + entity.class_.i18n['en']).replace(" ", "_")
        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': "crm:" + class_code,
                    'properties': {'title': entity.name},
                    'description': [{'value': entity.description}]
                    }

        # Relations
        if 'relations' in meta['show']:
            features['relations'] = Api.get_links(entity)

        # Types
        if 'types' in meta['show']:
            features['types'] = Api.get_node(entity)

        # Alias
        if entity.aliases and 'names' in meta['show']:  # pragma: nocover
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        # Depictions
        if 'depictions' in meta['show']:  # pragma: nocover
            features['depictions'] = Api.get_file(entity)

        # Time spans
        if 'when' in meta['show']:
            if entity.begin_from or entity.end_from:
                features['when'] = {'timespans': [Api.get_time(entity)]}

        # Geonames
        if 'geonames' in meta['show']:
            features['links'] = Api.get_external(entity)

        # Geometry
        if 'geometry' in meta['show'] and entity.class_.code == 'E53':
            features['geometry'] = Api.get_geom_by_entity(entity)
        elif 'geometry' in meta['show'] and entity.class_.code == 'E18':
            features['geometry'] = Api.get_geom_by_entity(Link.get_linked_entity(entity.id, 'P53'))

        data: Dict[str, Any] = {'type': type_,
                                '@context': app.config['API_SCHEMA'],
                                'features': [features]}
        return data
