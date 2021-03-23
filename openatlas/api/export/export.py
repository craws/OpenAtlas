import collections
from collections import defaultdict
from typing import Any, Dict, List, Optional

from flask import url_for
import pandas as pd
from openatlas.api.v02.resources.geojson_entity import GeoJsonEntity
from openatlas.models.entity import Entity
from openatlas.models.link import Link


class ApiExport:

    @staticmethod
    def api_export(entity):
        data = collections.OrderedDict()

        data['id'] = str(entity.id)
        data['name'] = entity.name,

        # if entity.aliases:
        #     data['aliases'] = []
        #     for key, value in entity.aliases.items():
        #         data['aliases'].append(value)
        data['description'] = entity.description,
        data['begin_from'] = str(entity.begin_from),
        data['begin_to'] = str(entity.begin_to),
        data['begin_comment'] = entity.begin_comment,
        data['end_from'] = str(entity.end_from),
        data['end_to'] = str(entity.end_to),
        data['end_comment'] = entity.end_comment,
        #data['links'] = ApiExport.get_links(entity)
        data['cidoc_class'] = entity.cidoc_class.name
        data['system_class'] = entity.class_.name
        data['note'] = entity.note
        l = ApiExport.get_links(entity)
        for k, v in l.items():
            data[k] = v
        df = pd.DataFrame.from_dict(data=data).T
        df.to_csv('test.csv')
        return data

    @staticmethod
    def get_links(entity: Entity):
        d = defaultdict(list)
        for link in Link.get_links(entity.id):
            d[link.property.i18n['en'].replace(' ', '_')].append(link.range.name)

        for link in Link.get_links(entity.id, inverse=True):
            d[link.property.i18n_inverse['en'].replace(' ', '_')].append(link.domain.name)

        return d
