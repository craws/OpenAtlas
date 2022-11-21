from typing import Any

from flask import url_for


def get_loud_entities(
        data: dict[str, Any],
        parser: dict[str, Any]) -> Any:
    properties_dict: dict[str, list] = {}
    for link in data['links']:
        property_name = link.property.i18n['en'].replace(' ', '_')
        properties_dict.setdefault(property_name, [])
        properties_dict[property_name].append(
            {
                'id': url_for('view', id_=link.range.id, _external=True),
                'type': link.range.cidoc_class.name,
                '_label': link.range.name
            }
        )
    for link in data['links_inverse']:
        property_name = link.property.i18n['en']
        property_name = property_name.replace(' ', '_')
        properties_dict.setdefault(property_name, [])
        properties_dict[property_name].append(
            {
                'id': url_for('view', id_=link.domain.id, _external=True),
                'type': link.domain.cidoc_class.name,
                '_label': link.domain.name
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