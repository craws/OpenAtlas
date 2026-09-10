import mimetypes
from typing import Any, cast
from uuid import UUID

from flask import g, url_for
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas.api.api_v04.resources.util import to_camel_case
from openatlas.api.api_v1.error_handlers import abort_not_found, \
    register_error_handlers
from openatlas.api.api_v1.formatters.lod_util import (
    EntityLinks, get_iiif_manifest_and_path, get_license_type,
    get_links_for_entities)
from openatlas.api.api_v1.models.files import FileItem, LicenseItem
from openatlas.api.api_v1.openapi_tags import vocabulary_tag
from openatlas.api.api_v1.models.util import (
    ExternalReferenceSystemModel, MatchTypeEnum, OpenAtlasClassEnum,
    ReferenceModel, TypeCategoryEnum)
from openatlas.api.api_v1.responses.vocabulary import \
    vocabulary_flat_response, vocabulary_list_response, \
    vocabulary_standard_by_class_response, vocabulary_tree_response
from openatlas.api.api_v1.models.vocabulary import (
    LinkedTypeItem, VocabularyFlatItem, VocabularyTreeItem,
    VocabularyFlatResponse,
    VocabularyStandardQuery,
    VocabularyTreeResponse, VocabularyStandardResponse)
from openatlas.api.api_v1.util.date_util import get_timespan_dict
from openatlas.database.api import get_vocab_ids_for_case_study
from openatlas.models.entity import Entity, Link

api_v1_vocabulary = APIBlueprint(
    'api_v1_vocabulary',
    __name__,
    url_prefix='/api/1/vocabulary')
register_error_handlers(api_v1_vocabulary)


class VocabularyTreePath(BaseModel):
    openatlas_class: OpenAtlasClassEnum = Field(
        ...,
        description="Filter the tree by a specific OpenAtlas class.")


class VocabularyId(BaseModel):
    id: int = Field(
        ...,
        description="ID of a type")


# todo: add license url
def _get_license_item(entity: Entity) -> LicenseItem:
    return LicenseItem(id=entity.id, name=entity.name)


def _get_file_item(entity: Entity) -> FileItem:
    file_ = g.files.get(entity.id)
    mimetype, _ = mimetypes.guess_type(file_) if file_ else (None, None)
    iiif = get_iiif_manifest_and_path(entity.id)
    license_ = get_license_type(entity)
    return FileItem(
        id=entity.id,
        name=entity.name,
        uuid=cast(UUID, entity.uuid),
        public_shareable=entity.public,
        license=_get_license_item(license_) if license_ else None,
        mimetype=mimetype,
        extension=file_.suffix if file_ else None,
        file_url=url_for(
            'api_v1_files.display_file', id=entity.id, _external=True),
        thumbnail_url=url_for(
            'api_v1_files.display_thumbnail', id=entity.id, _external=True),
        iiif_manifest_url=iiif['IIIFManifest'] or None,
        iiif_base_url=iiif['IIIFBasePath'] or None)


def _get_reference_item(link_: Link) -> ReferenceModel:
    entity = link_.domain
    return ReferenceModel(
        id=entity.id,
        name=entity.name,
        class_name=entity.class_.name,
        type=entity.standard_type.name if entity.standard_type else None,
        pages=link_.description or None,
        citation=entity.description)


def _get_match_type(link_: Link) -> MatchTypeEnum:
    assert link_.type
    return MatchTypeEnum(to_camel_case(g.types[link_.type.id].name))


def _get_external_reference_item(
        link_: Link,
        entity: Entity) -> ExternalReferenceSystemModel:
    return ExternalReferenceSystemModel(
        id=entity.id,
        name=entity.name,
        match_type=_get_match_type(link_),
        identifier=f'{entity.resolver_url or ''}{link_.description}',
        description=entity.description,
        system_url=entity.website_url,
        url=entity.resolver_url)


def _get_vocab_flat_item(
        type_: Entity,
        links: dict[int, EntityLinks]) -> VocabularyFlatItem:
    root_enntities = [g.types[id_] for id_ in type_.root] if type_.root else []
    root_entity = g.types[type_.root[0]] if type_.root else None
    type_classes = root_entity.classes if root_entity else type_.classes
    sub_entities = [g.types[id_] for id_ in type_.subs] if type_.subs else []
    inverse_links = links[type_.id].links_inverse
    image = next(
        (_get_file_item(link_.domain) for link_ in inverse_links
         if link_.domain.class_.name == 'file'),
        None)
    external_references = []
    for link_ in inverse_links:
        if link_.type and \
                (entity := g.reference_systems.get(link_.domain.id)):
            external_references.append(
                _get_external_reference_item(link_, entity))
    references = [
        _get_reference_item(link_) for link_ in inverse_links
        if link_.domain.class_.group.get('name') == 'reference'
           and link_.property.code == 'P67']
    return VocabularyFlatItem(
        id=type_.id,
        uuid=cast(UUID, type_.uuid),
        name=type_.name,
        description=type_.description,
        classes=type_classes,
        selectable=type_.selectable,
        image=image,
        external_references=external_references,
        references=references,
        timespan=get_timespan_dict(type_.dates),
        parents=[LinkedTypeItem(id=e.id, name=e.name) for e in root_enntities],
        sub_types=[LinkedTypeItem(id=e.id, name=e.name) for e in sub_entities],
        entity_count=type_.count,
        entity_count_subs=type_.count_subs,
        category=TypeCategoryEnum(type_.category))


@api_v1_vocabulary.get(
    '',
    summary="Get flat types list",
    responses=vocabulary_list_response,
    tags=[vocabulary_tag])
def get_vocabulary_list() -> dict[str, Any]:
    """Retrieves a flat list of all OpenAtlas types."""
    vocab_dict: dict[str, VocabularyFlatItem] = {}
    links = get_links_for_entities(list(g.types.values()))
    for id_, type_ in g.types.items():
        vocab_dict[str(id_)] = _get_vocab_flat_item(type_, links)
    return VocabularyFlatResponse(types=vocab_dict).model_dump(by_alias=True)


@api_v1_vocabulary.get(
    '<int:id>',
    summary="Get information of one type",
    responses=vocabulary_flat_response,
    tags=[vocabulary_tag])
def get_vocabulary_item(path: VocabularyId) -> dict[str, Any]:
    """Retrieves information of one types."""
    type_ = g.types.get(path.id)
    if not type_:
        abort_not_found(path.id)
    links = get_links_for_entities([type_])
    return _get_vocab_flat_item(type_, links).model_dump(by_alias=True)


def _walk_tree(
        vocab_ids: list[int],
        used_vocab_ids: set[int] | None = None) -> list[VocabularyTreeItem]:
    """Recursively builds the type tree from a list of type IDs. Prunes
    branches if used_vocab_ids is provided."""
    items = []
    for id_ in vocab_ids:
        item = g.types[id_]
        children = _walk_tree(item.subs, used_vocab_ids)

        if used_vocab_ids is not None:
            if id_ not in used_vocab_ids and not children:
                continue

        items.append(VocabularyTreeItem(
            id=item.id,
            uuid=item.uuid,
            name=item.name.replace("'", "&apos;"),
            selectable=item.selectable,
            classes=item.classes,
            entity_count=item.count,
            entity_count_subs=item.count_subs,
            children=children))
    return items


def _generate_vocabulary_tree(
        openatlas_class: str | None = None) -> dict[str, Any]:
    vocab_tree_dict: dict[str, list[VocabularyTreeItem]] = {
        'standard': [], 'custom': [], 'place': [],
        'value': [], 'system': [], 'tools': []}

    for category in vocab_tree_dict:
        root_ids = []
        for type_ in g.types.values():
            if not type_.root and getattr(type_, 'category', None) == category:
                if openatlas_class and type_.classes \
                        and openatlas_class not in type_.classes:
                    continue
                root_ids.append(type_.id)

        vocab_tree_dict[category] = _walk_tree(root_ids)

    return VocabularyTreeResponse(**vocab_tree_dict).model_dump(by_alias=True)


@api_v1_vocabulary.get(
    '/tree',
    summary="Get types tree",
    responses=vocabulary_tree_response,
    tags=[vocabulary_tag])
def get_vocabulary_tree() -> dict[str, Any]:
    """Retrieves all OpenAtlas types sorted hierarchically into standard,
    place, custom, value, and system categories."""
    return _generate_vocabulary_tree()


@api_v1_vocabulary.get(
    '/tree/<string:openatlas_class>',
    summary="Get types tree by OpenAtlas class",
    responses=vocabulary_tree_response,
    tags=[vocabulary_tag])
def get_vocabulary_tree_by_class(path: VocabularyTreePath) -> dict[str, Any]:
    """Retrieves all OpenAtlas types filtered by a specific OpenAtlas class."""
    class_ = path.openatlas_class
    if hasattr(path.openatlas_class, 'value'):
        class_ = path.openatlas_class.value

    return _generate_vocabulary_tree(openatlas_class=class_)


@api_v1_vocabulary.get(
    '/standard/<string:openatlas_class>',
    summary="Get standard types tree by OpenAtlas class",
    responses=vocabulary_standard_by_class_response,
    tags=[vocabulary_tag])
def get_vocabulary_standard_by_class(
        path: VocabularyTreePath,
        query: VocabularyStandardQuery) -> dict[str, Any]:
    """Retrieves standard OpenAtlas types filtered by a specific
    OpenAtlas class, formatted for hierarchical UI components."""

    class_ = path.openatlas_class
    if hasattr(path.openatlas_class, 'value'):
        class_ = path.openatlas_class.value

    used_vocab_ids = None
    if query.case_study:
        used_vocab_ids = get_vocab_ids_for_case_study(query.case_study)

    root_ids = []
    for type_ in g.types.values():
        if not type_.root and getattr(type_, 'category', None) == 'standard':
            if class_ and type_.classes and class_ not in type_.classes:
                continue
            root_ids.append(type_.id)

    standard_vocab = _walk_tree(root_ids, used_vocab_ids)

    return VocabularyStandardResponse(
        results=standard_vocab).model_dump(by_alias=True)
