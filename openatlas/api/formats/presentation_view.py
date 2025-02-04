import mimetypes
from typing import Any

from flask import g, url_for

from openatlas.api.resources.util import get_iiif_manifest_and_path, \
    get_license_name, get_location_link, \
    get_value_for_types
from openatlas.display.util import get_file_path
from openatlas.models.entity import Entity, Link


def get_presentation_types(
        entity: Entity,
        links: list[Link]) -> list[dict[str, Any]]:
    types = []
    if entity.class_.view == 'place':
        entity.types.update(get_location_link(links).range.types)
    for type_ in entity.types:
        type_dict = {
            'id': type_.id,
            'title': type_.name,
            'descriptions': type_.description,
            'isStandard': entity.standard_type.id == type_.id,
            'typeHierarchy': [{
                'label': g.types[root].name,
                'descriptions': g.types[root].description,
                'identifier': url_for(
                    'api.entity', id_=g.types[root].id, _external=True)}
                for root in type_.root]}
        type_dict.update(get_value_for_types(type_, links))
        types.append(type_dict)
    return types


def get_presentation_files(links_inverse: list[Link]) -> list[dict[str, str]]:
    files = []
    for link in links_inverse:
        if link.domain.class_.name != 'file':
            continue
        img_id = link.domain.id
        path = get_file_path(img_id)
        mime_type = None
        if path:
            mime_type, _ = mimetypes.guess_type(path)
        data = {
            'id': img_id,
            'title': link.domain.name,
            'license': get_license_name(link.domain),
            'creator': link.domain.creator,
            'licenseHolder': link.domain.license_holder,
            'publicShareable': link.domain.public,
            'mimetype': mime_type,
            'url': url_for(
                'api.display',
                filename=path.stem,
                _external=True) if path else "N/A"}
        data.update(get_iiif_manifest_and_path(img_id))
        files.append(data)
    return files
