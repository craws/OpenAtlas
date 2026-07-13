from __future__ import annotations

import requests

from openatlas import app
from openatlas.api.external.base import ExternalApi
from openatlas.display.util import link
from openatlas.models.entity import Entity


class GettyAAT(ExternalApi):  # pylint: disable=too-few-public-methods

    @staticmethod
    def get_info(id_: str, system: Entity) -> dict[str, object]:
        info: dict[str, object] = {}
        try:
            response = requests.get(
                f'https://vocab.getty.edu/aat/{id_}.json',
                headers={
                    'Accept': 'application/json',
                    **app.config['USER_AGENT']
                },
                proxies=app.config['PROXIES'],
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except Exception:  # pragma: no cover
            return info

        subject_uri = f'http://vocab.getty.edu/aat/{id_}'

        pref_label = None
        fallback_label = None
        scope_note = None
        broader_terms = []

        for item in data.get('@graph', []):
            if item.get('@id') == subject_uri:
                labels = item.get(
                    'http://www.w3.org/2008/05/skos-xl#prefLabel', [])

                skos_labels = item.get(
                    'http://www.w3.org/2004/02/skos/core#prefLabel', [])
                if not isinstance(skos_labels, list):
                    skos_labels = [skos_labels]

                for label_obj in skos_labels:
                    if isinstance(label_obj, dict):
                        lang = label_obj.get('@language')
                        val = label_obj.get('@value')
                        if lang == 'de':
                            pref_label = val
                        elif lang == 'en' and not fallback_label:
                            fallback_label = val
                    elif isinstance(label_obj, str):
                        fallback_label = label_obj

                notes = item.get(
                    'http://www.w3.org/2004/02/skos/core#scopeNote', [])
                if not isinstance(notes, list):
                    notes = [notes]
                for note in notes:
                    if isinstance(note, dict) and '@value' in note:
                        scope_note = note['@value']
                    elif isinstance(note, str):
                        scope_note = note

            elif item.get('@id') != subject_uri:
                label_obj = item.get(
                    'http://www.w3.org/2004/02/skos/core#prefLabel')
                if label_obj:
                    if isinstance(label_obj, list):
                        label_obj = label_obj[0]
                    val = label_obj.get('@value') if \
                        isinstance(label_obj,dict) else label_obj
                    if val and val not in broader_terms:
                        broader_terms.append(val)

        final_title = pref_label or fallback_label or f"AAT Concept {id_}"
        info['title'] = final_title

        if scope_note:
            info['description'] = scope_note

        if broader_terms:
            info['hierarchy'] = ' > '.join(broader_terms[:3])

        info['Getty AAT Link'] = link(
            id_,
            f'http://vocab.getty.edu/page/aat/{id_}',
            external=True)

        info['type'] = 'Getty AAT Thesaurus Term'

        return info
