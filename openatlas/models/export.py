from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Optional

from flask import g, url_for
from rdflib import Graph

from openatlas import app
from openatlas.api.endpoints.endpoint import Endpoint
from openatlas.api.external.arche import add_arche_file_metadata_to_graph
from config.default import ACDH
from openatlas.api.external.arche_class import ArcheFileMetadata
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.util import filter_by_type, get_reference_systems
from openatlas.models.entity import Entity


def current_date_for_filename() -> str:
    today = datetime.today()
    return \
        f'{today.year}-{today.month:02}-{today.day:02}_' \
        f'{today.hour:02}{today.minute:02}'


def sql_export(format_: str, postfix: Optional[str] = '') -> bool:
    file = app.config['EXPORT_PATH'] \
           / f'{current_date_for_filename()}_export{postfix}.{format_}'
    command: Any = [
        "pg_dump" if os.name == 'posix'
        else Path(str(shutil.which("pg_dump.exe")))]
    if format_ == 'dump':
        command.append('-Fc')
    command.extend([
        '-h', app.config['DATABASE_HOST'],
        '-d', app.config['DATABASE_NAME'],
        '-U', app.config['DATABASE_USER'],
        '-p', str(app.config['DATABASE_PORT']),
        '-f', file])
    try:
        root = os.environ['SYSTEMROOT'] if 'SYSTEMROOT' in os.environ else ''
        with subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                env={
                    'PGPASSWORD': app.config['DATABASE_PASS'],
                    'SYSTEMROOT': root}) as sub_process:
            sub_process.wait()
        with open(os.devnull, 'w', encoding='utf8') as null:
            with subprocess.Popen(
                    ['7z', 'a', f'{file}.7z', file],
                    stdout=null) as sub_process:
                sub_process.wait()
        file.unlink()
    except Exception:  # pragma: no cover
        return False

    return True


def arche_export() -> bool:
    external_metadata = app.config['ARCHE_METADATA']
    file_entities = Entity.get_by_class(['file'], types=True, aliases=True)
    type_ids = external_metadata.get('typeIds')
    if type_ids:
        file_entities = filter_by_type(file_entities, type_ids)

    sorted_files = sort_files_by_types(
        file_entities,
        type_ids,
        external_metadata['topCollection'])

    files_by_extension: dict[str, dict[str, set]] = defaultdict(
        lambda: defaultdict(set))
    for entity_id, path_set in sorted_files.items():
        for f in path_set:
            ext = normalize_extension(f.suffix)
            files_by_extension[entity_id][ext].add(f)

    archive_name = (
        f"{current_date_for_filename()}_"
        f"{external_metadata['topCollection'].replace(' ', '_')}.zip")

    tempfile.tempdir = str(app.config['TMP_PATH'])
    export_dir = app.config['EXPORT_PATH']
    export_dir.mkdir(parents=True, exist_ok=True)
    final_archive_path = export_dir / archive_name
    tmp_archive_path = Path(tempfile.mkdtemp()) / archive_name

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        failed_files_md = "\n".join(
            create_failed_files_md(check_files_for_arche(file_entities)))
        (temp_path / 'problematic_files.md').write_text(
            failed_files_md,
            encoding='utf-8')

        if file_entities:
            files_arche_turtle = get_arche_file_turtle_graph(
                file_entities,
                set(type_ids) if type_ids else set(),
                external_metadata['topCollection'])
            (temp_path / 'files.ttl').write_text(
                files_arche_turtle,
                encoding='utf-8')

        rdf_dump = Endpoint(
            ApiEntity.get_by_system_classes(['all']),
            {'type_id': type_ids, 'limit': 0, 'format': 'turtle'}).resolve()
        rdf_content = rdf_dump.get_data(as_text=True)
        (temp_path / 'rdf_dump.ttl').write_text(rdf_content, encoding='utf-8')

        with zipfile.ZipFile(
                tmp_archive_path,
                'w',
                compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(open_tmp_sql_file(), arcname='data/database.sql')
            archive.write(
                temp_path / 'problematic_files.md',
                arcname='debug/problematic_files.md')
            if file_entities:
                archive.write(
                    temp_path / 'files.ttl',
                    arcname='metadata/files.ttl')
            archive.write(
                temp_path / 'rdf_dump.ttl',
                arcname='data/rdf_dump.ttl')

            for type_name, ext_map in files_by_extension.items():
                for ext, files_set in ext_map.items():
                    for file_path in files_set:
                        with file_path.open('rb') as f:
                            archive.writestr(
                                f'data/{type_name}/{ext}/{file_path.name}',
                                f.read())

            infos = archive.infolist()
            total_size = sum(info.file_size for info in infos)
            total_files = sum(1 for i in infos if not i.filename.endswith('/'))
            all_dirs: set[Path] = set()
            for info in infos:
                path = Path(info.filename)
                all_dirs.update(path.parents)
            all_dirs.discard(Path("."))
            total_dirs = len(all_dirs)
            total_entries = len(infos)

            stat_md = (
                f"# Archive Statistics\n"
                f"- **Total size**: {total_size} bytes\n"
                f"- **Total entries**: {total_entries}\n"
                f"- **Files**: {total_files}\n"
                f"- **Directories**: {total_dirs}\n")
            archive.writestr('debug/file_statistic.md', stat_md)

    tmp_archive_path.replace(final_archive_path)

    return final_archive_path


def create_failed_files_md(
        missing: dict[str, set[tuple[int, str]]]) -> list[str]:
    text = []
    for topic, entities in missing.items():
        text.append(f'# {topic} ({len(entities)})')
        for entity in entities:
            text.append(
                f'\t* {entity[0]} - {entity[1]} - '
                f'{url_for("view", id_=entity[0], _external=True)}')
    return text


def normalize_extension(ext: str) -> str:
    ext = ext.lower().lstrip('.')
    if ext == 'jpg':
        return 'jpeg'
    return ext


def get_place_and_actor_relations(
        entities: list[Entity]) -> dict[int, list[dict[str, Any]]]:
    linked_entities = Entity.get_links_of_entities(
        [e.id for e in entities],
        'P67')
    file_to_related_entity_ids: dict[int, list[int]] = defaultdict(list)
    places_and_actors: dict[int, dict[str, Any]] = {}
    for link in linked_entities:
        if (link.range.class_.view == 'actor'
                or link.range.class_.name == 'place'):
            places_and_actors[link.range.id] = {
                'entity': link.range,
                'links_inverse': [],
                'ref_systems': []}
            file_to_related_entity_ids[link.domain.id].append(
                link.range.id)

    inverse_links = Entity.get_links_of_entities(
        list(places_and_actors.keys()),
        'P67',
        inverse=True)

    for link_ in inverse_links:
        places_and_actors[link_.range.id]['links_inverse'].append(link_)

    for entity_dict in places_and_actors.values():
        places_and_actors[
            entity_dict['entity'].id]['ref_systems'].extend(
            get_reference_systems(entity_dict['links_inverse']))

    relations: defaultdict[int, list[dict[str, Any]]] = defaultdict(list)
    for file_id, entity_ids in file_to_related_entity_ids.items():
        for id_ in entity_ids:
            relations[file_id].append(places_and_actors[id_])

    return dict(relations)


def get_publications(
        entities: list[Entity]) -> dict[int, list[tuple[Entity, str]]]:
    linked_publications = Entity.get_links_of_entities(
        [e.id for e in entities],
        'P67',
        inverse=True)
    publications: dict[int, list[tuple[Entity, str]]] = defaultdict(list)
    for link in linked_publications:
        publications[link.range.id].append((link.domain, link.description))
    return dict(publications)


def sort_files_by_types(
        entities: list[Entity],
        type_ids: set[int],
        top_collection: str) -> dict[str, set[Path]]:
    files_by_types = defaultdict(set)
    for entity in entities:
        if not g.files.get(entity.id) or not entity.standard_type:
            continue
        if type_ids:
            for type_ in entity.types:
                if type_.id in type_ids:
                    type_name = g.types[type_.id].name.replace(' ', '_')
                    files_by_types[type_name].add(g.files.get(entity.id))
        else:
            files_by_types[top_collection].add(g.files.get(entity.id))
    return dict(files_by_types)


def hash_file(path: Path, chunk_size: int = 8192) -> str:
    """Generate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def check_files_for_arche(
        entities: list[Entity]) -> dict[str, set[tuple[int, str]]]:
    missing = defaultdict(set)
    entity_ids = set()
    for entity in entities:
        entity_ids.add(entity.id)
        # Todo: get without license to test
        print(entity.name)
        if not g.files.get(entity.id):
            missing['No files'].add((entity.id, entity.name))
        if not entity.public:
            missing['Not public'].add((entity.id, entity.name))
        if not entity.standard_type:
            missing['No license'].add((entity.id, entity.name))
        if not entity.creator:
            missing['No creator'].add((entity.id, entity.name))
        if not entity.license_holder:
            missing['No license holder'].add((entity.id, entity.name))
    for duplicate in find_duplicates(entity_ids):
        missing['Duplicates'].add(
            (duplicate[0], f'is duplicate of {duplicate[1]}'))
    return dict(missing)


def get_arche_file_turtle_graph(
        entities: list[Entity],
        type_ids: set[int],
        top_collection: str) -> str:
    graph = Graph()
    graph.bind("acdh", ACDH)
    metadata = get_arche_file_metadata(entities, type_ids, top_collection)
    for metadata_obj in metadata:
        add_arche_file_metadata_to_graph(graph, metadata_obj)
    return graph.serialize(format="turtle")


def get_arche_file_metadata(
        entities: list[Entity],
        type_ids: set[int],
        top_collection: str) -> list[ArcheFileMetadata]:
    publications = get_publications(entities)
    relations = get_place_and_actor_relations(entities)
    license_urls = {}
    arche_metadata_list = []
    for entity in entities:
        standard_type = entity.standard_type
        if not g.files.get(entity.id) or not standard_type:
            continue
        if standard_type.id in license_urls:
            continue
        url = None
        for link_ in standard_type.get_links('P67', inverse=True):
            if link_.domain.class_.name == "external_reference":
                url = link_.domain.name
                break
        if url is None:
            continue
        license_urls[standard_type.id] = url
        if type_ids:
            for type_ in entity.types:
                if type_.id in type_ids:
                    type_name = g.types[type_.id].name.replace(' ', '_')
                    arche_metadata_list.append(
                        ArcheFileMetadata.construct(
                            entity,
                            type_name,
                            relations.get(entity.id),
                            publications.get(entity.id),
                            license_urls[standard_type.id]))
        else:
            arche_metadata_list.append(
                ArcheFileMetadata.construct(
                    entity,
                    top_collection,
                    relations.get(entity.id),
                    publications.get(entity.id),
                    license_urls[standard_type.id]))
    return arche_metadata_list


def find_duplicates(entity_ids: set[int]) -> set[tuple[int, int]]:
    size_map = defaultdict(list)
    for file_id, path in g.files.items():
        if file_id not in entity_ids:
            continue
        size = path.stat().st_size
        size_map[size].append((file_id, path))

    duplicates = set()
    for files in size_map.values():
        if len(files) < 2:
            continue  # Only one file of this size — skip
        hash_map: dict[str, int] = {}
        for file_id, path in files:
            try:
                file_hash = hash_file(path)
            except Exception as e:  # pragma: no cover
                g.logger.log(
                    'info',
                    'hashing',
                    f'failed to hash filer{file_id}: {e}')
                continue
            if file_hash in hash_map:
                original_id = hash_map[file_hash]
                duplicates.add((file_id, original_id))
            else:
                hash_map[file_hash] = file_id
    return duplicates


def open_tmp_sql_file() -> str:
    with tempfile.NamedTemporaryFile(
            mode='w+',
            suffix='.sql',
            delete=False) as tmp_sql:
        command = [
            'pg_dump',
            '-h', app.config['DATABASE_HOST'],
            '-d', app.config['DATABASE_NAME'],
            '-U', app.config['DATABASE_USER'],
            '-p', str(app.config['DATABASE_PORT']),
            '--schema=model',
            '--schema=public',
            '--schema=import']
        subprocess.run(
            command,
            stdout=tmp_sql,
            env={
                'PGPASSWORD': app.config['DATABASE_PASS'],
                'SYSTEMROOT': os.environ[
                    'SYSTEMROOT'] if 'SYSTEMROOT' in os.environ else ''},
            check=True)
        return tmp_sql.name
