from collections import defaultdict

import pandas as pd

from openatlas.models.entity import Entity
from openatlas.models.link import Link


class ApiExportCSV:

    @staticmethod
    def export_entity(entity: Entity):
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
            'note': entity.note}

        for k, v in ApiExportCSV.get_links(entity).items():
            data[k] = ' | '.join(list(map(str, v)))
        print(data)
        df = pd.DataFrame.from_dict(data=data, orient='index').T
        print(df)
        df.to_csv('test.csv')
        return data

    @staticmethod
    def get_links(entity: Entity):
        d = defaultdict(list)
        for link in Link.get_links(entity.id):
            d[link.property.i18n['en'].replace(' ', '_')].append(link.range.name)
        for link in Link.get_links(entity.id, inverse=True):
            d[link.property.i18n_inverse['en'].replace(' ', '_') if link.property.i18n_inverse[
                'en'] else link.property.i18n['en'].replace(' ', '_')].append(link.domain.name)
        return d
