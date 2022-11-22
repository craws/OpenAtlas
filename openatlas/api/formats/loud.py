from typing import Any

from flask import url_for

from openatlas.api.formats.linked_places import relation_type


def get_loud_entities(
        data: dict[str, Any],
        parser: dict[str, Any],
        loud: dict[str, str]) -> Any:
    properties_dict: dict[str, list] = {}
    # Set name to properties
    properties_dict['identified_by'] = [{
        "type": "Name",
        "content": data['entity'].name
    }]

    for link_ in data['links']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        property_name = loud[relation_type(link_).replace(' ', '_')]

        properties_dict[property_name].append(
            {
                'id': url_for('view', id_=link_.range.id, _external=True),
                'type': link_.range.cidoc_class.i18n['en'],
                '_label': link_.range.name
            }
        )
    for link_ in data['links_inverse']:
        if link_.property.code in ['OA7', 'OA8', 'OA9']:
            continue
        property_name = loud[relation_type(link_, True).replace(' ', '_')]
        properties_dict.setdefault(property_name, [])
        properties_dict[property_name].append(
            {
                'id': url_for('view', id_=link_.domain.id, _external=True),
                'type': link_.domain.cidoc_class.i18n['en'],
                '_label': link_.domain.name
            }
        )

    dict_ = {
        '@context': "https://linked.art/ns/v1/linked-art.json",
        'id': url_for('view', id_=data['entity'].id, _external=True),
        'type': f"{data['entity'].cidoc_class.i18n['en']}"
        .replace(' ', '').replace('-', ''),
        '_label': data['entity'].name,
        'content': data['entity'].description
    }

    return dict_ | properties_dict
