from collections import defaultdict
from typing import Any, Dict, List, Union

import pandas as pd
from flask import Response

from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.link import Link


class ApiExportCSV:

    @staticmethod
    def export_entities(entities: List[Entity], name: str) -> Response:
        data = []
        for entity in entities:
            data.append(ApiExportCSV.build_dataframe(entity))
        index = []
        for d in data:
            for k in d.keys():
                if k not in index:
                    index.append(k)
        return Response(pd.DataFrame(data=data).to_csv(),
                        mimetype='text/csv',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + name + '.csv'
                        })

    @staticmethod
    def build_dataframe(entity: Entity) -> Dict[str, List[Union[str, int]]]:
        geom = ApiExportCSV.get_geom_entry(entity)
        data = {
            'id': str(entity.id),
            'name': entity.name,
            'description': entity.description,
            'begin_from': entity.begin_from,
            'begin_to': entity.begin_to,
            'begin_comment': entity.begin_comment,
            'end_from': entity.end_from,
            'end_to': entity.end_to,
            'end_comment': entity.end_comment,
            'cidoc_class': entity.cidoc_class.name,
            'system_class': entity.class_.name,
            'note': entity.note,
            'geom_type': geom['type'],
            'coordinates': geom['coordinates']}
        for k, v in ApiExportCSV.get_links(entity).items():
            data[k] = ' | '.join(list(map(str, v)))
        return data

    @staticmethod
    def export_entity(entity: Entity) -> Response:
        return Response(pd.DataFrame.from_dict(data=ApiExportCSV.build_dataframe(entity),
                                               orient='index').T.to_csv(),
                        mimetype='text/csv',
                        headers={
                            'Content-Disposition': 'attachment;filename=' + str(
                                entity.name) + '.csv'
                        })

    @staticmethod
    def get_links(entity: Entity) -> Dict[Any, list]:
        d = defaultdict(list)
        for link in Link.get_links(entity.id):
            d[link.property.i18n['en'].replace(' ', '_')].append(link.range.name)
        for link in Link.get_links(entity.id, inverse=True):
            d[link.property.i18n_inverse['en'].replace(' ', '_') if link.property.i18n_inverse[
                'en'] else link.property.i18n['en'].replace(' ', '_')].append(link.domain.name)
        return d

    @staticmethod
    def get_geom_entry(entity: Entity) -> Dict[str, None]:
        geom = {'type': None, 'coordinates': None}
        if entity.class_.view == 'place' or entity.class_.name in ['find', 'artifact']:
            geom = ApiExportCSV.get_geometry(Link.get_linked_entity(entity.id, 'P53'))
        elif entity.class_.name == 'object_location':
            geom = ApiExportCSV.get_geometry(entity)
        return geom

    @staticmethod
    def get_geometry(entity: Entity) -> Dict[str, None]:
        if entity.cidoc_class.code != 'E53':  # pragma: nocover
            return {'type': None, 'coordinates': None}
        geoms = Gis.get_by_id(entity.id)
        if geoms:
            return {key: [d[key] for d in geoms] for key in geoms[0]}
        return {'type': None, 'coordinates': None}
