import ast
from typing import Any, Dict, List, Union

from flask import g, url_for

from openatlas import app
from openatlas.api.v02.resources.error import Error
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.reference import Reference
from openatlas.util.display import format_date, get_file_path


class GeoJsonEntity:

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
            if link.property.code == 'P53':
                entity.location = link.range

        for link in Link.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + 'i_'
                                          + link.property.i18n['en'].replace(' ', '_')})
        return links if links else None

    @staticmethod
    def get_file(entity: Entity) -> List[Dict[str, str]]:
        files = []
        for link in Link.get_links(entity.id, codes="P67", inverse=True):  # pragma: nocover
            if link.domain.system_type == 'file':
                path = get_file_path(link.domain.id)
                files.append({'@id': url_for('api_entity', id_=link.domain.id, _external=True),
                              'title': link.domain.name,
                              'license': GeoJsonEntity.get_license(link.domain.id),
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
    def get_node(entity: Entity) -> List[Dict[str, Any]]:
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
        return time if time else None

    @staticmethod
    def get_geom_by_entity(entity: Entity) -> Union[str, Dict[str, Any]]:
        if entity.class_.code != 'E53':
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
    def get_external(entity: Entity) -> List[Dict[str, Union[str, Any]]]:
        ref = []
        for external in g.external:
            reference = Reference.get_link(entity, external)
            if reference:
                ref.append({'identifier': g.external[external]['url'] + reference.domain.name,
                            'type': GeoJsonEntity.to_camelcase(reference.type.name)})
        return ref if ref else None

    @staticmethod
    def get_entity_by_id(id_: int) -> Entity:
        try:
            entity = Entity.get_by_id(id_, nodes=True, aliases=True)
        except Exception:
            # Todo: Eliminate Error
            raise Error('Entity ID ' + str(id_) + ' doesn\'t exist', status_code=404,
                        payload="404a")
        return entity

    @staticmethod
    def get_entity(entity: Entity, parser: Dict[str, Any]) -> Dict[str, Any]:
        type_ = 'FeatureCollection'

        class_code = ''.join(entity.class_.code + " " + entity.class_.i18n['en']).replace(" ", "_")
        features = {'@id': url_for('entity_view', id_=entity.id, _external=True),
                    'type': 'Feature',
                    'crmClass': "crm:" + class_code,
                    'properties': {'title': entity.name}}

        # Descriptions
        if entity.description:
            features['description'] = [{'value': entity.description}]

        # Alias
        if entity.aliases and 'names' in parser['show']:
            features['names'] = []
            for key, value in entity.aliases.items():
                features['names'].append({"alias": value})

        # Relations
        # if GeoJsonEntity.get_links(entity) and 'relations' in parser['show']:
        #     features['relations'] = GeoJsonEntity.get_links(entity)
        features['relations'] = GeoJsonEntity.get_links(entity) if 'relations' in parser[
            'show'] else None

        # Types
        # if GeoJsonEntity.get_node(entity) and 'types' in parser['show']:
        #     features['types'] = GeoJsonEntity.get_node(entity)
        features['types'] = GeoJsonEntity.get_node(entity) if 'types' in parser['show'] else None


        # Depictions
        # if GeoJsonEntity.get_file(entity) and 'depictions' in parser['show']:  # pragma: nocover
        #     features['depictions'] = GeoJsonEntity.get_file(entity)
        features['depictions'] = GeoJsonEntity.get_file(entity) if 'depictions' in parser['show'] else None

        # Time spans
        # if GeoJsonEntity.get_time(entity) and 'when' in parser['show']:
        #     if entity.begin_from or entity.end_from:
        #         features['when'] = {'timespans': [GeoJsonEntity.get_time(entity)]}

        if entity.begin_from or entity.end_from:
            features['when'] = {'timespans': [GeoJsonEntity.get_time(entity)]} if'when' in parser['show'] else None

        # Geonames
        # if GeoJsonEntity.get_external(entity) and 'links' in parser['show']:
        #     features['links'] = [GeoJsonEntity.get_external(entity)]
        features['links'] = GeoJsonEntity.get_external(entity) if 'links' in parser['show'] else None

        # Geometry
        if 'geometry' in parser['show'] and entity.class_.code == 'E53':
            features['geometry'] = GeoJsonEntity.get_geom_by_entity(entity)
        elif 'geometry' in parser['show'] and entity.location:
            features['geometry'] = GeoJsonEntity.get_geom_by_entity(entity.location)

        data: Dict[str, Any] = {'type': type_,
                                '@context': app.config['API_SCHEMA'],
                                'features': [features]}
        return data
