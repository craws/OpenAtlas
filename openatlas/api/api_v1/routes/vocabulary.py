from flask import g
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from openatlas.api.api_v1.error_handlers import register_error_handlers
from openatlas.api.api_v1.openapi_tags import vocabulary_tag
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.database.entity import get_vocab_ids_for_case_study
from openatlas.api.api_v1.models.vocabulary import (
    VocabularyFlatItem, VocabularyTreeItem, VocabularyFlatResponse, VocabularyStandardQuery,
    VocabularyTreeResponse, VocabularyStandardResponse)

api_v1_vocabulary = APIBlueprint(
    'vocabulary',
    __name__,
    url_prefix='/api/1/vocabulary')
register_error_handlers(api_v1_vocabulary)


class VocabularyTreePath(BaseModel):
    openatlas_class: OpenAtlasClassEnum = Field(
        ...,
        description="Filter the tree by a specific OpenAtlas class.")


@api_v1_vocabulary.get(
    '',
    summary="Get flat types list",
    responses={200: VocabularyFlatResponse},
    tags=[vocabulary_tag])
def get_vocabulary_list() -> dict:
    """Retrieves a flat list of all OpenAtlas types."""
    vocab_dict = {}
    for id_, type_ in g.types.items():
        vocab_dict[str(id_)] = VocabularyFlatItem(
            id=type_.id,
            name=type_.name,
            description=type_.description,
            classes=type_.classes,
            selectable=type_.selectable,
            image_id=type_.image_id,
            first=type_.dates.first
            if hasattr(type_, 'dates') and type_.dates else None,
            last=type_.dates.last
            if hasattr(type_, 'dates') and type_.dates else None,
            root=type_.root,
            subs=type_.subs,
            count=type_.count,
            count_subs=type_.count_subs,
            category=getattr(type_, 'category', None))
    return VocabularyFlatResponse(types=vocab_dict).model_dump(by_alias=True)


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
            name=item.name.replace("'", "&apos;"),
            classes=item.classes or None,
            children=children))
    return items


def _generate_vocabulary_tree(openatlas_class: str | None = None) -> dict:
    vocab_tree_dict = {
        'standard': [], 'custom': [], 'place': [],
        'value': [], 'system': [], 'tools': []}

    for category in vocab_tree_dict.keys():
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
    responses={200: VocabularyTreeResponse},
    tags=[vocabulary_tag])
def get_vocabulary_tree() -> dict:
    """Retrieves all OpenAtlas types sorted hierarchically into standard,
    place, custom, value, and system categories."""
    return _generate_vocabulary_tree()


@api_v1_vocabulary.get(
    '/tree/<string:openatlas_class>',
    summary="Get types tree by OpenAtlas class",
    responses={200: VocabularyTreeResponse},
    tags=[vocabulary_tag])
def get_vocabulary_tree_by_class(path: VocabularyTreePath) -> dict:
    """Retrieves all OpenAtlas types filtered by a specific OpenAtlas class."""
    class_ = path.openatlas_class
    if hasattr(path.openatlas_class, 'value'):
        class_ = path.openatlas_class.value

    return _generate_vocabulary_tree(openatlas_class=class_)


@api_v1_vocabulary.get(
    '/standard/<string:openatlas_class>',
    summary="Get standard types tree by OpenAtlas class",
    responses={200: VocabularyStandardResponse},
    tags=[vocabulary_tag])
def get_vocabulary_standard_by_class(
        path: VocabularyTreePath,
        query: VocabularyStandardQuery) -> dict:
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
