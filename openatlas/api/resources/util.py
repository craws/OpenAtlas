from typing import Any, Optional

from flask import g, json, url_for

from openatlas.api.resources.api_entity import ApiEntity
from openatlas.display.util import check_iiif_activation, check_iiif_file_exist
from openatlas.models.entity import Entity, Link
from openatlas.models.gis import Gis


def get_license_name(entity: Entity) -> Optional[str]:
    license_ = ''
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            license_ = type_.name
            break
    return license_


def get_license_type(entity: Entity) -> Optional[Entity]:
    license_ = None
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            license_ = type_
            break
    return license_


def get_license_url(entity: Entity) -> Optional[str]:
    url = ''
    for type_ in entity.types:
        if g.types[type_.root[0]].name == 'License':
            for link_ in type_.get_links('P67', inverse=True):
                if link_.domain.class_.name == "external_reference":
                    url = link_.domain.name
            break
    return url


def get_license_ids_with_links() -> dict[int, str]:
    type_ids = Entity.get_hierarchy('License').get_sub_ids_recursive()
    license_links = Entity.get_links_of_entities(type_ids, 'P67', inverse=True)
    url_dict = {}
    for link_ in license_links:
        if link_.domain.class_.name == "external_reference":
            url_dict[link_.range.id] = link_.domain.name
    return url_dict


def to_camel_case(i: str) -> str:
    return (i[0] + i.title().translate(" ")[1:] if i else i).replace(" ", "")


def replace_empty_list_values_in_dict_with_none(
        data: dict[str, Any]) -> dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, list) and not data[key]:
            data[key] = None
    return data


def get_linked_entities_api(id_: int | list[int]) -> list[Entity]:
    domain = [link_.range for link_ in Entity.get_links_of_entities(id_)]
    range_ = [
        link_.domain for link_ in
        Entity.get_links_of_entities(id_, inverse=True)]
    return [*range_, *domain]


def get_linked_entities_id_api(id_: int) -> list[Entity]:
    domain_ids = [
        link_.range.id for link_ in Entity.get_links_of_entities(id_)]
    range_ids = [
        link_.domain.id for link_ in
        Entity.get_links_of_entities(id_, inverse=True)]
    return [*range_ids, *domain_ids]


def get_entities_linked_to_special_type(id_: int) -> list[Entity]:
    domain_ids = [
        link_['domain_id'] for link_ in Link.get_links_by_type(g.types[id_])]
    range_ids = [
        link_['range_id'] for link_ in Link.get_links_by_type(g.types[id_])]
    return ApiEntity.get_by_ids(
        range_ids + domain_ids,
        types=True,
        aliases=True)


def get_entities_linked_to_special_type_recursive(
        id_: int,
        data: list[int]) -> list[int]:
    for link_ in Link.get_links_by_type(g.types[id_]):
        data.append(link_['domain_id'])
        data.append(link_['range_id'])
    for sub_id in g.types[id_].subs:
        get_entities_linked_to_special_type_recursive(sub_id, data)
    return data


def get_entities_linked_to_type_recursive_(
        id_: int,
        data: list[int]) -> list[int]:
    for sub_id in g.types[id_].subs:
        data.append(sub_id)
        get_entities_linked_to_type_recursive_(sub_id, data)
    return data


def get_entities_from_type_with_subs(id_: int) -> list[Entity]:
    type_ids = get_entities_linked_to_type_recursive_(id_, [id_])
    entity_ids = Link.get_entity_ids_by_type_ids(type_ids)
    return ApiEntity.get_by_ids(
        [link_ for link_ in entity_ids if link_ not in type_ids],
        types=True,
        aliases=True)


def remove_duplicate_entities(entities: list[Entity]) -> list[Entity]:
    seen: set[int] = set()
    seen_add = seen.add  # Do not change, faster than always call seen.add()
    return [e for e in entities if not (e.id in seen or seen_add(e.id))]


def remove_spaces_dashes(string: str) -> str:
    return string.replace(' ', '').replace('-', '')


def get_reference_systems(links_inverse: list[Link]) -> list[dict[str, Any]]:
    ref = []
    for link_ in links_inverse:
        if isinstance(link_.domain, Entity) and link_.type:
            system = g.reference_systems[link_.domain.id]
            ref.append({
                'referenceURL': system.website_url,
                'id': link_.description,
                'resolverURL': system.resolver_url,
                'identifier':
                    f"{system.resolver_url or ''}{link_.description}",
                'type': to_camel_case(g.types[link_.type.id].name),
                'referenceSystem': system.name})
    return ref


def get_iiif_manifest_and_path(img_id: int) -> dict[str, str]:
    iiif_manifest = ''
    iiif_base_path = ''
    if check_iiif_activation() and check_iiif_file_exist(img_id):
        iiif_manifest = url_for(
            'api.iiif_manifest',
            version=g.settings['iiif_version'],
            id_=img_id,
            _external=True)
        if g.files.get(img_id):
            iiif_base_path = \
                f"{g.settings['iiif_url']}{img_id}{g.files[img_id].suffix}"
    return {'IIIFManifest': iiif_manifest, 'IIIFBasePath': iiif_base_path}


def get_location_link(links: list[Link]) -> Link:
    return [l_ for l_ in links if l_.property.code == 'P53'][0]


def geometry_to_geojson(
        geoms: Optional[list[dict[str, Any]]] = None) \
        -> Optional[dict[str, Any]]:
    if not geoms:
        return None
    if len(geoms) == 1:
        return geoms[0]
    return {'type': 'GeometryCollection', 'geometries': geoms}


def geometry_to_feature_collection(
        geoms: Optional[list[dict[str, Any]]] = None) \
        -> Optional[dict[str, Any]]:
    if not geoms:
        return None
    features = [generate_feature(geom) for geom in geoms]
    if len(features) == 1:
        return features[0]
    return {'type': 'FeatureCollection', 'features': features}


def generate_feature(geom: dict[str, Any]) -> dict[str, Any]:
    return {
        'type': 'Feature',
        'geometry': {
            'type': geom['type'],
            'coordinates': geom['coordinates']},
        'properties': {
            'title': geom['title'],
            'description': geom['description'],
            'shapeType': geom['shapeType'],
            'entityId': geom['placeId'],
            'locationId': geom['locationId']}}


def get_geometries(parser: dict[str, Any]) -> list[dict[str, Any]]:
    choices = [
        'gisPointAll', 'gisPointSupers', 'gisPointSubs',
        'gisPointSibling', 'gisLineAll', 'gisPolygonAll']
    all_geoms = Gis.get_all()
    out = []
    for item in choices \
            if 'gisAll' in parser['geometry'] else parser['geometry']:
        for geom in json.loads(all_geoms[item]):
            out.append(geom)
    return out


def date_to_str(date: Any) -> Optional[str]:
    return str(date) if date else None


def get_crm_relation(link_: Link, inverse: bool = False) -> str:
    property_ = f"i {link_.property.i18n_inverse['en']}" \
        if inverse and link_.property.i18n_inverse['en'] \
        else f" {link_.property.i18n['en']}"
    return f"crm:{link_.property.code}{property_}"


def get_crm_relation_label_x(link_: Link, inverse: bool = False) -> str:
    if inverse and link_.property.name_inverse:
        return link_.property.name_inverse
    return link_.property.name


def get_crm_relation_x(link_: Link, inverse: bool = False) -> str:
    property_ = f"_{link_.property.i18n['en']}"
    if inverse and link_.property.i18n_inverse['en']:
        property_ = f"i_{link_.property.i18n_inverse['en']}"
    return f"crm:{link_.property.code}{property_.replace(' ', '_')}"


def get_crm_code(link_: Link, inverse: bool = False) -> str:
    name = link_.range.cidoc_class.i18n['en']
    if inverse:
        name = link_.domain.cidoc_class.i18n['en']
    code = link_.range.cidoc_class.code
    if inverse:
        code = link_.domain.cidoc_class.code
    return f"crm:{code} {name}"


def flatten_list_and_remove_duplicates(list_: list[Any]) -> list[Any]:
    return [item for sublist in list_ for item in sublist if item not in list_]


def get_value_for_types(type_: Entity, links: list[Link]) -> dict[str, str]:
    type_dict = {}
    for link in links:
        if link.range.id == type_.id and link.description:
            type_dict['value'] = link.description
            if link.range.id == type_.id and type_.description:
                type_dict['unit'] = type_.description
    return type_dict


def filter_by_type(
        entities: list[Entity],
        type_ids: list[int]) -> list[Entity]:
    result = []
    for entity in entities:
        if any(
                id_ in [type_.id for type_ in entity.types]
                for id_ in type_ids):
            result.append(entity)
    return result
