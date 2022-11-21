from typing import Any

from flask import url_for


def get_loud_entities(
        data: dict[str, Any],
        parser: dict[str, Any]) -> Any:
    for link in data['links']:
        if link.property.code == 'P2':
            pass
        print(link.property.code)
        print(link.property.name)

    dict_ = {
        '@context': "https://linked.art/ns/v1/linked-art.json",
        'id': url_for('view', id_=data['entity'].id, _external=True),
        'type': f"{data['entity'].cidoc_class.i18n['en']}"
        .replace(' ', '').replace('-', ''),
        '_label': data['entity'].name
    }

    return dict_