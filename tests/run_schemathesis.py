import sys
from collections.abc import Iterator
from functools import cache
from pathlib import Path
from typing import Any

from flask import g

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import schemathesis
from schemathesis.cli import schemathesis as schemathesis_cli
from schemathesis.generation.modes import GenerationMode

from openatlas import app
from openatlas.api.api_v1.models.util import OpenAtlasClassEnum
from openatlas.api.api_v1.util.files import (
    get_display_extensions, get_multiple_file_paths, get_public_share_yes_id,
    get_valid_license_ids, iiif_file_exists)
from openatlas.display.image_processing import (
    check_iiif_activation, is_supported_image, safe_resize_image)
from openatlas.models.entity import Entity
from openatlas.models.rights_holder import RightsHolder

SCHEMATHESIS_ARGUMENTS = (
    'run',
    'http://localhost:5000/api/1/docs/openapi.json',
    '--url',
    'http://localhost:5000',
    '--phases',
    'examples,coverage,fuzzing',
    '--checks',
    ('not_a_server_error,status_code_conformance,content_type_conformance,'
     'response_headers_conformance,positive_data_acceptance'))


def has_file_access(file_entity: Entity) -> bool:
    file_type_ids = {type_.id for type_ in file_entity.types if type_}
    has_license = bool(file_type_ids & get_valid_license_ids())
    is_public_shareable = get_public_share_yes_id() in file_type_ids
    return has_license and is_public_shareable


def prepare_thumbnails(
        files: list[Entity],
        paths: dict[int, Path],
        thumbnail_dir: Path) -> list[int]:
    thumbnails = []
    extensions = get_display_extensions()
    for file_ in files[:30]:
        path = paths.get(file_.id)
        if (not path
                or path.suffix.lower() not in extensions
                or not is_supported_image(path)):
            continue
        resized = safe_resize_image(
            str(file_.id),
            path.suffix.lower(),
            app.config['IMAGE_SIZE']['thumbnail'],
            True)
        if resized and any(thumbnail_dir.glob(f'{file_.id}.*')):
            thumbnails.append(file_.id)
            if len(thumbnails) == 3:
                break
    return thumbnails


@cache
def get_database_examples() -> dict[str, Any]:
    with app.test_request_context():
        app.preprocess_request()
        classes = {}
        for class_ in OpenAtlasClassEnum:
            if class_.value == 'type':
                continue
            if entities := Entity.get_by_class(class_.value):
                classes[class_.value] = entities[0]

        case_studies = Entity.get_hierarchy('Case study').subs
        files = Entity.get_by_class('file', types=True)
        existing = get_multiple_file_paths(
            [file_.id for file_ in files],
            app.config['UPLOAD_PATH'])
        public_files = [
            file_ for file_ in files
            if file_.id in existing and has_file_access(file_)]

        thumbnail_dir = (
            app.config['RESIZED_IMAGES']
            / app.config['IMAGE_SIZE']['thumbnail'])
        existing_thumbnails = get_multiple_file_paths(
            [file_.id for file_ in public_files],
            thumbnail_dir)
        thumbnails = [
            file_.id for file_ in public_files
            if file_.id in existing_thumbnails]
        if not thumbnails and g.settings.get('iiif') and check_iiif_activation():
            thumbnails = [
                file_.id for file_ in public_files[:100]
                if iiif_file_exists(file_.id)]
        if not thumbnails:
            thumbnails = prepare_thumbnails(
                public_files,
                existing,
                thumbnail_dir)

        annotations = []
        files_by_id = {file_.id: file_ for file_ in files}
        g.cursor.execute(
            'SELECT id, image_id FROM model.annotation_image ORDER BY id;')
        for row in g.cursor:
            file_ = files_by_id.get(row['image_id'])
            if file_ and has_file_access(file_):
                annotations.append(row['id'])
                if len(annotations) == 3:
                    break

        file_entities = [e.id for e in classes.values()]
        if public_files:
            g.cursor.execute(
                """
                SELECT DISTINCT range_id FROM model.link
                WHERE domain_id IN %(file_ids)s AND property_code = 'P67'
                ORDER BY range_id LIMIT 3;
                """,
                {'file_ids': tuple(e.id for e in public_files)})
            if linked_ids := [row['range_id'] for row in g.cursor]:
                file_entities = linked_ids

        return {
            'classes': classes,
            'types': list(g.types),
            'type_entities': list(g.types.values()),
            'case_studies': case_studies,
            'agents': [e.id for e in RightsHolder.get_rights_holders()],
            'files': [e.id for e in public_files],
            'file_entities': file_entities,
            'thumbnails': thumbnails,
            'annotations': annotations}


def get_path_examples(path: str) -> Iterator[dict[str, Any]]:
    if path.startswith('/api/1/iiif/'):
        if path == '/api/1/iiif/{id}/annotation/{version}':
            for id_ in get_database_examples()['annotations']:
                yield {'id': id_, 'version': '2'}
        return

    data = get_database_examples()
    ext_param = {'ext': 'json'} if '{ext}' in path else {}

    if '{uuid}' in path:
        for entity in [*data['classes'].values(), *data['type_entities'][:3]]:
            if entity.uuid:
                yield {'uuid': str(entity.uuid), **ext_param}
    elif '{entity_class}' in path:
        for class_ in data['classes']:
            yield {'entity_class': class_}
    elif '{openatlas_class}' in path:
        for class_ in data['classes']:
            yield {'openatlas_class': class_}
    elif '{id}' in path:
        if path == '/api/1/files/entity/{id}':
            ids = data['file_entities']
        elif path.startswith('/api/1/files/'):
            ids = (
                data['thumbnails'] if path.endswith('/thumbnail')
                else data['files'])
        elif path.startswith('/api/1/case-studies/'):
            ids = data['case_studies']
        elif path.startswith('/api/1/agents/'):
            ids = data['agents']
        elif path.startswith('/api/1/vocabulary/'):
            ids = data['types']
        else:
            ids = []
        for id_ in ids[:3]:
            yield {'id': id_, **ext_param}
    else:
        yield {}


@schemathesis.hook
def before_add_examples(context: Any, examples: list[Any]) -> None:
    path = context.operation.path
    if (path.startswith('/api/1/iiif/')
            and path != '/api/1/iiif/{id}/annotation/{version}'):
        return
    case_studies = get_database_examples()['case_studies']
    for params in get_path_examples(path):
        kwargs: dict[str, Any] = {}
        if params:
            kwargs['path_parameters'] = params
        if path.startswith('/api/1/entities/'):
            kwargs['query'] = {'limit': 5, 'page': 1}
        elif (path in (
                '/api/1/vocabulary/standard/{openatlas_class}',
                '/api/1/system/count/entities')
                and case_studies):
            kwargs['query'] = {'caseStudy': case_studies[0]}
        examples.append(context.operation.Case(**kwargs))


@schemathesis.hook
def map_case(_context: Any, case: Any) -> Any:
    if (case.meta
            and case.meta.generation.mode == GenerationMode.POSITIVE
            and case.path_parameters
            and (examples := list(get_path_examples(case.operation.path)))):
        skip = {'ext', 'version', 'entity_class', 'openatlas_class'}
        for name, value in examples[0].items():
            if name in case.path_parameters and name not in skip:
                valid = {ex[name] for ex in examples if name in ex}
                if case.path_parameters[name] not in valid:
                    case.path_parameters[name] = value
    return case


def main() -> None:
    schemathesis_cli.main(
        args=SCHEMATHESIS_ARGUMENTS,
        prog_name='schemathesis')


if __name__ == '__main__':
    main()
