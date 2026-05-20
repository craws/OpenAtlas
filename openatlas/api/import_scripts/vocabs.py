from typing import Any, Optional

from flask import g

from openatlas.api.import_scripts.util import (
    get_exact_match, get_match_types, vocabs_requests)
from openatlas.models.entity import (
    Entity, get_reference_system_by_name_safe, insert)


def import_vocabs_data(
        id_: str,
        form_data: dict[str, Any],
        details: dict[str, Any],
        category: str) -> tuple[list[Any], list[Any]]:
    return fetch_top_level(id_, details, form_data) \
        if category == 'hierarchy' \
        else (fetch_top_groups(id_, details, form_data))


def fetch_top_groups(
        id_: str,
        details: dict[str, Any],
        form_data: dict[str, Any]) -> tuple[list[Any], list[Any]]:
    count = []
    duplicates = []
    if ref := get_vocabs_reference_system(details):
        for group in form_data['choices']:
            if not Entity.check_hierarchy_exists(group[1]) and \
                    group[0] in form_data['top_concepts']:
                hierarchy = insert({
                    'openatlas_class_name': 'type',
                    'name': group[1],
                    'description':
                        f'Automatically imported from {details["title"]}'})
                Entity.insert_hierarchy(
                    hierarchy,
                    'custom', form_data['classes'],
                    form_data['multiple'])
                exact_match_id = get_exact_match().id
                name = group[0].rsplit('/', 1)[-1]
                ref.link('P67', hierarchy, name, type_id=exact_match_id)
                import_member(
                    group[0],
                    id_,
                    form_data['language'],
                    ref,
                    hierarchy)
                count.append(group[0])
            if Entity.check_hierarchy_exists(group[1]) \
                    and group[0] in form_data['top_concepts']:
                duplicates.append(group[1])
    return count, duplicates


def import_member(
        uri: str,
        id_: str,
        lang: str,
        ref: Entity,
        super_: Optional[Entity], ) -> bool:
    req = vocabs_requests(id_, 'groupMembers', {'uri': uri, 'lang': lang})
    child = None
    for member in req['members']:
        name = member['uri'].rsplit('/', 1)[-1]
        if super_:
            child = insert({
                'openatlas_class_name': 'type',
                'name': member['prefLabel']})
            child.link('P127', super_)
            ref.link('P67', child, name, type_id=get_exact_match().id)
        if member['hasMembers']:
            import_member(member['uri'], id_, lang, ref, child)
    return True


def fetch_top_level(
        id_: str,
        details: dict[str, Any],
        form_data: dict[str, Any]) -> tuple[list[Any], list[Any]]:
    req = vocabs_requests(id_, 'topConcepts', {'lang': form_data['language']})
    count = []
    duplicates = []
    vocabulary = None
    if form_data['vocabulary']:
        if Entity.check_hierarchy_exists(details['title']):
            return [], [details['title']]
        vocabulary = insert({
            'openatlas_class_name': 'type',
            'name': details['title'],
            'description':
                f'Automatically imported from {details['title']}'})
        Entity.insert_hierarchy(
            vocabulary,
            'custom', form_data['classes'],
            form_data['multiple'])
    if ref := get_vocabs_reference_system(details):
        for entry in req['topconcepts']:
            if entry['uri'] in form_data['top_concepts']:
                if not vocabulary and \
                        Entity.check_hierarchy_exists(entry['label']):
                    duplicates.append(entry['label'])
                    continue
                top_concept = insert({
                    'openatlas_class_name': 'type',
                    'name': entry['label'],
                    'description': '' if vocabulary else \
                        f'Automatically imported from {details["title"]}'})
                if vocabulary:
                    top_concept.link('P127', vocabulary)
                else:
                    Entity.insert_hierarchy(
                        top_concept,
                        'custom', form_data['classes'],
                        form_data['multiple'])
                exact_match_id = get_exact_match().id
                name = entry['uri'].rsplit('/', 1)[-1]
                ref.link('P67', top_concept, name, type_id=exact_match_id)
                entry['subs'] = import_children(
                    entry['uri'],
                    id_,
                    form_data['language'],
                    ref,
                    top_concept)
                count.append(entry)
    return count, duplicates


def import_children(
        uri: str,
        id_: str,
        lang: str,
        ref: Entity,
        super_: Optional[Entity], ) -> list[dict[str, Any]]:
    req = vocabs_requests(id_, 'narrower', {'uri': uri, 'lang': lang})
    exact_match_id = get_exact_match().id
    children = []
    child = None
    for entry in req['narrower']:
        if not entry['prefLabel']:
            g.logger.log(
                'warn',
                'import',
                f'{entry["uri"]} has no prefLabel assigned to it')
            continue
        name = entry['uri'].rsplit('/', 1)[-1]
        if super_:
            child = insert({
                'openatlas_class_name': 'type',
                'name': get_pref_label(entry['prefLabel'], id_, entry['uri'])})
            child.link('P127', super_)
            ref.link('P67', child, name, type_id=exact_match_id)
            ext_ref_systems = get_external_references_from_mapping(
                id_,
                entry['uri'],
                lang)
            for link, system, type_ in ext_ref_systems:
                child.link(
                    'P67',
                    system,
                    description=link,
                    type_id=type_.id,
                    inverse=True)
        entry['subs'] = import_children(entry['uri'], id_, lang, ref, child)
        children.append(entry)
    return children


def get_external_references_from_mapping(
        id_: str,
        uri: str,
        lang: str) -> list[tuple[str, Entity, Entity]]:
    req = vocabs_requests(
        id_,
        'mappings',
        {'uri': uri, 'lang': lang, 'external': 'true'})
    out = []
    for mapping in req.get('mappings', []):
        type_ = mapping['type'][0]
        if 'exactMatch' in type_:
            type_ = 'exact_match'
        else:
            type_ = 'close_match'
        match_type = get_match_types().get(type_)
        if not match_type:
            continue

        # Add addtional reference systems if available
        match mapping['vocabName']:
            case 'www.wikidata.org':
                link_name = str(mapping['hrefLink'].rsplit('/', 1)[-1])
                if ref_system := get_reference_system_by_name_safe('Wikidata'):
                    out.append((link_name, ref_system, match_type))
    return out


def get_pref_label(label: str, id_: str, uri: str) -> str:
    if not label:
        req = vocabs_requests(id_, 'label', {'uri': uri})
        label = req['prefLabel']
    return label


def get_vocabs_reference_system(details: dict[str, Any], ) -> Entity:
    title = details['title']
    system = None
    for system_ in g.reference_systems.values():
        if system_.name == f'{title} vocabulary':
            system = system_
    if not system:
        system = insert({
            'name': f'{title} vocabulary',
            'openatlas_class_name': 'reference_system',
            'description': f'Import of {title} vocabulary (autogenerated)',
            'website_url': g.settings['vocabs_base_url'],
            'resolver_url': f'{details['conceptUri'].rsplit('/', 1)[0]}/',
            'example_id': None,
            'reference_system_classes': ['type']})
    return system


def get_vocabularies() -> list[dict[str, Any]]:
    req = vocabs_requests(endpoint='vocabularies', parameter={'lang': 'en'})
    out = []
    for voc in req['vocabularies']:
        out.append(voc | fetch_vocabulary_details(voc['uri']))
    return out


def fetch_vocabulary_details(id_: str) -> dict[str, str]:
    data = vocabs_requests(id_, parameter={'lang': 'en'})
    return {
        'id': data['id'],
        'title': data['title'],
        'defaultLanguage': data['defaultLanguage'],
        'languages': data['languages'],
        'conceptUri':
            data['conceptschemes'][0]['uri'] if data['conceptschemes'] else ''}


def fetch_top_concept_details(id_: str) -> list[Any]:
    req = vocabs_requests(id_, 'topConcepts', parameter={'lang': 'en'})
    return [
        (concept['uri'], concept['label']) for concept in req['topconcepts']]


def fetch_top_group_details(id_: str) -> list[Any]:
    req = vocabs_requests(id_, 'groups', parameter={'lang': 'en'})
    all_groups = []
    child_groups = []

    for group in req['groups']:
        all_groups.append((group['uri'], group['prefLabel']))
        if 'childGroups' in group:
            child_groups.extend(group['childGroups'])
    return [group for group in all_groups if group[0] not in child_groups]
