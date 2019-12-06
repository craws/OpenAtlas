from flask import request, url_for

from openatlas import app
from openatlas.models.entity import EntityMapper, Entity
from openatlas.models.geonames import GeonamesMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import format_date


class Api:

    @staticmethod
    def get_links(entity: Entity) -> list:
        links = []
        for link in LinkMapper.get_links(entity.id):
            links.append({'label': link.range.name,
                          'relationTo': url_for('api_entity', id_=link.range.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.name.replace(' ', '_')}, )

        for link in LinkMapper.get_links(entity.id, inverse=True):
            links.append({'label': link.domain.name,
                          'relationTo': url_for('api_entity', id_=link.domain.id, _external=True),
                          'relationType': 'crm:' + link.property.code + '_' + link.property.name.replace(' ', '_')}, )
        return links

    @staticmethod
    def get_entity(id_: int) -> dict:
        entity = EntityMapper.get_by_id(id_, nodes=True, aliases=True)
        type_ = 'unknown'
        if entity.class_.code == 'E18' and entity.system_type == 'place':
            type_ = 'FeatureCollection'
        nodes = []
        for node in entity.nodes:
            nodes.append({'identifier': url_for('api_entity', id_=node.id, _external=True),
                          'label': node.name})
        geo = GeonamesMapper.get_geonames_link(entity)
        data: dict = {
            'type': type_,  # Todo: what if it's a person, event, ...
            '@context': request.base_url,
            'features': [{  # Todo: what if it's a person, event, ...
                '@id': url_for('entity_view', id_=entity.id, _external=True),
                'type': entity.system_type,  # Todo: 'feature' if place but what if else
                'properties': {'title': entity.name},
                'when': {'timespans': [{
                    'start': {'earliest': format_date(entity.begin_from),
                              'latest': format_date(entity.begin_to),
                              'comment': entity.begin_comment},
                    'end': {'earliest': format_date(entity.end_from),
                            'latest': format_date(entity.end_to),
                            'comment': entity.end_comment}}]},
                'types': nodes,
                #  Todo: Only add if Geo exists --> make a new if statement like the geometry
                'links': [{'type': geo.type.name if geo else '',
                           'identifier': app.config['GEONAMES_VIEW_URL'] + geo.domain.name if geo else '',
                           }],
                'relations': Api.get_links(entity),
                'descriptions': [
                    {'@id': request.base_url,
                     'value': entity.description}],
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
