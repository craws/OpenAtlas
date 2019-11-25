# Created by Alexander Watzinger and others. Please see README.md for licensing information

from flask import g, request, url_for

from openatlas.models.entity import EntityMapper
from openatlas.util.util import format_date


class Api:

    @staticmethod
    def get_links(entity) -> list:
        # Todo: the same has to be done the other way round with an i at property e.g. crm:P55i_...
        sql = """
            SELECT l.id, l.property_code, l.range_id, e.name
            FROM model.link l
            JOIN model.entity e ON l.range_id = e.id AND l.domain_id = %(entity_id)s;"""

        g.execute(sql, {'entity_id': entity.id})
        result = g.cursor.fetchall()
        links = []
        for row in result:
            property_ = g.properties[row.property_code]
            links.append({
                'label': row.name,
                'relationTo': url_for('api_entity', id_=row.range_id, _external=True),
                'relationType': 'crm:' + property_.code + '_' + property_.name.replace(' ', '_')},)
        return links

    @staticmethod
    def get_entity(id_: int) -> dict:
        entity = EntityMapper.get_by_id(id_, nodes=True, aliases=True)
        type_ = 'unknown'
        if entity.class_.code == 'E18' and entity.system_type == 'place':
            type_ = 'FeatureCollection'
        elif entity.class_.code == 'E55':
            entity.view_name = 'node'
        nodes = []
        for node in entity.nodes:
            nodes.append({'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name})

        data = {
            'type': type_,  # Todo: what if it's a person, event, ...
            '@context': request.base_url,
            'features': [{  # Todo: what if it's a person, event, ...
                '@id': url_for(entity.view_name + '_view', id_=entity.id, _external=True),
                'type': entity.system_type,  # Todo: 'feature' if place but what if else
                'properties': {'title': entity.name},
                # Todo: add comments of dates?
                'when': {'timespans': [{
                    'start': {'earliest': format_date(entity.begin_from),
                              'latest': format_date(entity.begin_to),
                              'comment': entity.begin_comment},
                    'end': {'earliest': format_date(entity.end_from),
                            'latest': format_date(entity.end_to),
                            'comment': entity.end_comment}}]},
                'types': nodes,
                'relations': Api.get_links(entity),
                # 'links': [
                #     {
                #         'type': geonames,
                #         'identifier': geonames
                #     }
                # ]
                'descriptions': [
                    {'@id': 'https://thanados.openatlas.eu/api/v01/50505',
                     'value': '''...In the area of Obere Holzwiese 215 inhumation burials 
                              were  documented in different excavations. There might have been a 
                              wooden church in the north-western part of the areal, which might 
                              date back to the first half  of the 9th century...'''}],
                'depictions': [
                    {'@id': 'https://thanados.openatlas.eu/display/112760.png',
                     'title': 'Map of the cemetery',
                     'license': 'cc:by-nc-nd/4.0/',
                     '@context': 'https://thanados.openatlas.eu/api/v01/112760'}]}]}

        if type_ == 'FeatureCollection':
            # gis = GisMapper.get_all(entity)
            # location = entity.get_linked_entity('P53', nodes=True)
            # geonames = GeonamesMapper.get_geonames_link(entity)
            data['features'].append({'geometry': {
                'type': 'GeometryCollection',
                'geometries': [{
                    'type': 'Point',
                    'coordinates': [15.643286705017092, 48.586735522177],
                    'classification': 'centerpoint',
                    'description': 'Point in the center of the cemetery',
                    'title': 'Thunau centerpoint'}]}})

        return data