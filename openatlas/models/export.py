from __future__ import annotations

import hashlib
import operator
import os
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, cast

from flask import Response, g, url_for
from rdflib import Graph

from config.default import ACDH, ACDHI
from openatlas import app
from openatlas.api.api_v04.endpoints.endpoint import Endpoint
from openatlas.api.api_v04.formats.rdf import rdf_export_to_file
from openatlas.api.api_v04.resources.api_entity import ApiEntity
from openatlas.api.api_v04.resources.util import (
    filter_by_type, get_reference_systems)
from openatlas.api.api_v1.util.files import get_license_url_mapping
from openatlas.api.external.arche import (
    add_arche_collection_to_graph, add_arche_file_metadata_to_graph,
    add_arche_top_collection_to_graph)
from openatlas.api.external.arche_class import (
    ArcheCollection, ArcheFileMetadata, ArcheTopCollection, get_arche_slug,
    get_arche_top_uri, normalize_extension, slugify_arche_segment)
from openatlas.display.image_processing import get_binary_path
from openatlas.models.entity import Entity


def current_date_for_filename() -> str:
    today = datetime.today()
    return \
        f'{today.year}-{today.month:02}-{today.day:02}_' \
        f'{today.hour:02}{today.minute:02}'


def sql_export(format_: str, postfix: Optional[str] = '') -> bool:
    dump_file = app.config['SQL_PATH'] \
        / f'{current_date_for_filename()}_export{postfix}.{format_}'
    pg_dump_path = get_binary_path('pg_dump', required=True)
    if not pg_dump_path:  # pragma: no cover
        return False
    command = [
        pg_dump_path,
        '-h', app.config['DATABASE_HOST'],
        '-d', app.config['DATABASE_NAME'],
        '-U', app.config['DATABASE_USER'],
        '-p', str(app.config['DATABASE_PORT']),
        '-f', str(dump_file)]
    if format_ == 'dump':
        command.insert(1, '-Fc')
    try:
        subprocess.run(
            command,
            env={
                'PGPASSWORD': app.config['DATABASE_PASS'],
                'SYSTEMROOT': os.environ.get('SYSTEMROOT', '')},
            check=True,
            capture_output=True,
            text=True)
        seven_zip_path = get_binary_path('7z', required=False)
        if seven_zip_path:
            archive_file = f'{dump_file}.7z'
            try:
                with open(os.devnull, 'w', encoding='utf8') as null:
                    subprocess.run(
                        [seven_zip_path, 'a', archive_file, str(dump_file)],
                        stdout=null,
                        check=True                )
                dump_file.unlink()
            except subprocess.CalledProcessError as e:  # pragma: no cover
                g.logger.log(
                    'warn',
                    'database',
                    f'7zip compression failed: {e.stderr}')
    except subprocess.CalledProcessError as e:  # pragma: no cover
        g.logger.log('error', 'database', f'pg_dump failed: {e.stderr}')
        return False
    except Exception as e:  # pragma: no cover
        g.logger.log('error', 'database', f'Unexpected backup error: {str(e)}')
        return False
    return True


def arche_export() -> Path:
    external_metadata = app.config['ARCHE_METADATA']
    file_entities = Entity.get_by_class(['file'], types=True, aliases=True)
    type_ids = external_metadata.get('typeIds')
    if type_ids:
        file_entities = filter_by_type(file_entities, type_ids)

    license_urls = get_license_url_mapping()
    sorted_files = sort_files_by_types(file_entities, type_ids, license_urls)

    files_by_extension: dict[str, dict[str, set[Path]]] = defaultdict(
        lambda: defaultdict(set))
    for type_slug, path_set in sorted_files.items():
        for f in path_set:
            ext = normalize_extension(f.suffix)
            files_by_extension[type_slug][ext].add(f)

    slug = get_arche_slug(external_metadata)
    sql_filename = f'{slug}_database.sql' if slug else 'database.sql'
    rdf_filename = f'{slug}_rdf.ttl' if slug else 'rdf.ttl'
    metadata_filename = f'{slug}_metadata.ttl' if slug else 'metadata.ttl'
    archive_name = (
        f'{current_date_for_filename()}_{slug}.zip'
        if slug else f'{current_date_for_filename()}_arche.zip')

    arche_dir = app.config['ARCHE_PATH']
    arche_dir.mkdir(parents=True, exist_ok=True)
    final_archive_path = arche_dir / archive_name

    Path(app.config['TMP_PATH']).mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=app.config['TMP_PATH']) as temp_dir:
        temp_path = Path(temp_dir)
        tmp_archive_path = temp_path / archive_name
        failed_files_md = "\n".join(
            create_failed_files_md(check_files_for_arche(file_entities)))
        (temp_path / 'problematic_files.md').write_text(
            failed_files_md,
            encoding='utf-8')

        sql_dump_path = Path(open_tmp_sql_file())
        rdf_dump_path = temp_path / rdf_filename
        rdf_dump = cast(Response, Endpoint(
            ApiEntity.get_by_system_classes(['all']),
            {'type_id': type_ids, 'limit': 0, 'format': 'turtle'}).resolve())
        rdf_dump_path.write_text(
            rdf_dump.get_data(as_text=True),
            encoding='utf-8')

        metadata_ttl = get_arche_metadata_turtle(
            file_entities,
            set(type_ids) if type_ids else set(),
            files_by_extension,
            license_urls,
            [
                (sql_filename, sql_dump_path, 'Database SQL dump'),
                (rdf_filename, rdf_dump_path, 'Database RDF dump')])
        (temp_path / metadata_filename).write_text(
            metadata_ttl,
            encoding='utf-8')

        with zipfile.ZipFile(
                tmp_archive_path,
                'w',
                compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(sql_dump_path, arcname=f'data/{sql_filename}')
            archive.write(
                temp_path / 'problematic_files.md',
                arcname='debug/problematic_files.md')
            archive.write(
                temp_path / metadata_filename,
                arcname=f'metadata/{metadata_filename}')
            archive.write(rdf_dump_path, arcname=f'data/{rdf_filename}')

            for type_slug, ext_map in files_by_extension.items():
                for ext, files_set in ext_map.items():
                    for file_path in files_set:
                        arcname = (
                            f'data/{type_slug}/{ext}/{file_path.name}'
                            if type_slug else f'data/{ext}/{file_path.name}')
                        with file_path.open('rb') as file:
                            archive.writestr(arcname, file.read())

            infos = archive.infolist()
            staged_size = sum(info.file_size for info in infos)
            manifest_member_names = ['debug/file_statistic.md'] + [
                info.filename for info in infos if not info.is_dir()]

            manifest_size = 0
            for name in manifest_member_names:
                manifest_size += len(
                    format_checksum_line(name, '0' * 64).encode('utf-8'))

            all_entries = ['debug/file_statistic.md', 'checksums.sha256'] + [
                info.filename for info in infos]
            all_dirs: set[Path] = set()
            for entry_name in all_entries:
                all_dirs.update(Path(entry_name).parents)
            all_dirs.discard(Path('.'))

            total_entries = len(all_entries)
            total_files = sum(
                1 for name in all_entries if not name.endswith('/'))
            total_dirs = len(all_dirs)

            base_size = staged_size + manifest_size
            total_size = base_size
            stat_md = ''
            for _ in range(10):
                stat_md = (
                    f'# Archive Statistics\n'
                    f'- **Total size**: {total_size} bytes\n'
                    f'- **Total entries**: {total_entries}\n'
                    f'- **Files**: {total_files}\n'
                    f'- **Directories**: {total_dirs}\n')
                stat_size = len(stat_md.encode('utf-8'))
                new_total_size = base_size + stat_size
                if new_total_size == total_size:
                    break
                total_size = new_total_size

            archive.writestr('debug/file_statistic.md', stat_md)
            archive.writestr(
                'checksums.sha256',
                create_checksum_manifest(archive))

        shutil.move(str(tmp_archive_path), str(final_archive_path))
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


def get_place_and_actor_relations(
        entities: list[Entity]) -> dict[int, list[dict[str, Any]]]:
    linked_entities = Entity.get_links_of_entities(
        [e.id for e in entities],
        'P67')
    file_to_related_entity_ids: dict[int, list[int]] = defaultdict(list)
    places_and_actors: dict[int, dict[str, Any]] = {}
    for link in linked_entities:
        if (link.range.class_.group['name'] == 'actor'
                or link.range.class_.group['name'] == 'place'):
            places_and_actors[link.range.id] = {
                'entity': link.range,
                'links_inverse': [],
                'ref_systems': []}
            file_to_related_entity_ids[link.domain.id].append(
                link.range.id)

    if places_and_actors.keys():
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
        classes=g.class_groups['reference']['classes'],
        inverse=True)
    publications: dict[int, list[tuple[Entity, str]]] = defaultdict(list)
    for link in linked_publications:
        publications[link.range.id].append((link.domain, link.description))
    return dict(publications)


def sort_files_by_types(
        entities: list[Entity],
        type_ids: set[int] | list[int] | None,
        license_urls: dict[int, list[str]] | None = None) \
        -> dict[str, set[Path]]:
    files_by_types: dict[str, set[Path]] = defaultdict(set)
    for entity in entities:
        file_path = g.files.get(entity.id)
        if not file_path or not entity.standard_type:
            continue
        if license_urls is not None and not license_urls.get(
                entity.standard_type.id):
            continue
        if type_ids:
            for type_ in entity.types:
                if type_.id in type_ids:
                    type_slug = (
                        slugify_arche_segment(g.types[type_.id].name)
                        or str(type_.id))
                    files_by_types[type_slug].add(file_path)
        else:
            files_by_types[''].add(file_path)
    return dict(files_by_types)


def hash_file(path: Path, chunk_size: int = 8192) -> str:
    sha256 = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def format_checksum_line(name: str, digest: str) -> str:
    escaped_name = name.replace('\\', '\\\\').replace('\n', '\\n')
    marker = '\\' if escaped_name != name else ''
    return f'{marker}{digest}\t{escaped_name}\n'


def create_checksum_manifest(
        archive: zipfile.ZipFile,
        manifest_filename: str = 'checksums.sha256',
        chunk_size: int = 8192) -> str:
    manifest_lines: list[str] = []

    infos = sorted(archive.infolist(), key=operator.attrgetter('filename'))

    for a, b in zip(infos, infos[1:], strict=False):
        if a.filename == b.filename:  # pragma: no cover
            raise ValueError(f'Duplicate ZIP member name: {a.filename}')

    for info in infos:
        if info.is_dir() or info.filename == manifest_filename:
            continue  # pragma: no cover

        sha256 = hashlib.sha256()
        with archive.open(info, 'r') as member_file:
            while chunk := member_file.read(chunk_size):
                sha256.update(chunk)

        digest = sha256.hexdigest()
        manifest_lines.append(format_checksum_line(info.filename, digest))

    return ''.join(manifest_lines)


def check_files_for_arche(
        entities: list[Entity]) -> dict[str, set[tuple[int, str]]]:
    missing = defaultdict(set)
    entity_ids = set()
    for entity in entities:
        entity_ids.add(entity.id)
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


def _format_extent(counts: dict[str, int]) -> str:
    return ', '.join(
        f'{count} {ext.upper()}' for ext, count in sorted(counts.items()))


def _build_arche_collections(
        type_ids: set[int] | list[int] | None,
        files_by_extension: dict[str, dict[str, set[Path]]],
        type_titles: dict[str, str],
        license_summary: str) -> list[ArcheCollection]:
    top_uri = get_arche_top_uri(app.config['ARCHE_METADATA'])
    collections: list[ArcheCollection] = []
    for type_slug, ext_map in sorted(files_by_extension.items()):
        parent_uri = top_uri
        if type_ids and type_slug:
            type_counts = {
                ext: len(paths) for ext, paths in ext_map.items()}
            type_uri = f'{top_uri}/{type_slug}'
            collections.append(ArcheCollection.construct(
                uri=type_uri,
                is_part_of=top_uri,
                filename=type_slug,
                title=type_titles.get(type_slug, type_slug),
                extent=_format_extent(type_counts),
                license_summary=license_summary))
            parent_uri = type_uri
        for ext, paths in sorted(ext_map.items()):
            collections.append(ArcheCollection.construct(
                uri=f'{parent_uri}/{ext}',
                is_part_of=parent_uri,
                filename=ext,
                title=ext.upper(),
                extent=f'{len(paths)} {ext.upper()}',
                license_summary=license_summary))
    return collections


def get_arche_metadata_turtle(
        entities: list[Entity],
        type_ids: set[int] | list[int] | None,
        files_by_extension: dict[str, dict[str, set[Path]]],
        license_urls: dict[int, list[str]],
        dump_files: list[tuple[str, Path, str]]) -> str:
    graph = Graph()
    graph.bind('acdh', ACDH)
    graph.bind('acdhi', ACDHI)
    emitted: set[str] = set()

    total_counts: dict[str, int] = defaultdict(int)
    for ext_map in files_by_extension.values():
        for ext, paths in ext_map.items():
            total_counts[ext] += len(paths)
    for _name, path, _title in dump_files:
        total_counts[normalize_extension(path.suffix)] += 1

    license_names = sorted({
        e.standard_type.name
        for e in entities
        if g.files.get(e.id)
        and e.standard_type
        and license_urls.get(e.standard_type.id)})
    license_summary = ', '.join(license_names) or 'See individual resources'
    type_titles = {
        slugify_arche_segment(g.types[id_].name) or str(id_):
            g.types[id_].name
        for id_ in (type_ids or [])
        if id_ in g.types}

    top = ArcheTopCollection.construct(
        _format_extent(total_counts),
        license_summary)
    add_arche_top_collection_to_graph(graph, top, emitted)

    for collection in _build_arche_collections(
            type_ids,
            files_by_extension,
            type_titles,
            license_summary):
        add_arche_collection_to_graph(graph, collection, emitted)

    for dump_name, dump_path, dump_title in dump_files:
        add_arche_file_metadata_to_graph(
            graph,
            ArcheFileMetadata.construct_dump(dump_name, dump_path, dump_title),
            emitted)

    for metadata_obj in get_arche_file_metadata(
            entities,
            type_ids,
            license_urls):
        add_arche_file_metadata_to_graph(graph, metadata_obj, emitted)

    return graph.serialize(format="turtle")


def get_arche_file_turtle_graph(
        entities: list[Entity],
        type_ids: set[int] | list[int] | None) -> str:
    graph = Graph()
    graph.bind("acdh", ACDH)
    graph.bind("acdhi", ACDHI)
    emitted: set[str] = set()
    metadata = get_arche_file_metadata(entities, type_ids)
    for metadata_obj in metadata:
        add_arche_file_metadata_to_graph(graph, metadata_obj, emitted)
    return graph.serialize(format="turtle")


def get_arche_file_metadata(
        entities: list[Entity],
        type_ids: set[int] | list[int] | None,
        license_urls: dict[int, list[str]] | None = None) \
        -> list[ArcheFileMetadata]:
    publications = get_publications(entities)
    relations = get_place_and_actor_relations(entities)
    if license_urls is None:
        license_urls = get_license_url_mapping()
    arche_metadata_list = []
    for entity in entities:
        if not g.files.get(entity.id):
            continue
        standard_type = entity.standard_type
        if not standard_type:
            continue
        license_url_list = license_urls.get(standard_type.id)
        if not license_url_list:  # pragma: no cover
            continue

        if type_ids:
            for type_ in entity.types:
                if type_.id in type_ids:
                    type_slug = (
                        slugify_arche_segment(g.types[type_.id].name)
                        or str(type_.id))
                    arche_metadata_list.append(
                        ArcheFileMetadata.construct(
                            entity,
                            type_slug,
                            relations.get(entity.id, []),
                            publications.get(entity.id, []),
                            license_url_list))
        else:
            arche_metadata_list.append(
                ArcheFileMetadata.construct(
                    entity,
                    None,
                    relations.get(entity.id, []),
                    publications.get(entity.id, []),
                    license_url_list))
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
        if len(files) <= 1:
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
    pg_dump_bin = get_binary_path('pg_dump', required=True)
    if not pg_dump_bin:  # pragma: no cover
        raise FileNotFoundError("pg_dump binary not found")
    Path(app.config['TMP_PATH']).mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
            mode='w+',
            suffix='.sql',
            dir=app.config['TMP_PATH'],
            delete=False) as tmp_sql:

        tmp_sql.write("CREATE EXTENSION IF NOT EXISTS postgis;\n\n")
        tmp_sql.flush()

        command = [
            pg_dump_bin,
            '-h', app.config['DATABASE_HOST'],
            '-d', app.config['DATABASE_NAME'],
            '-U', app.config['DATABASE_USER'],
            '-p', str(app.config['DATABASE_PORT']),
            '--schema=model',
            '--schema=import']
        try:
            subprocess.run(
                command,
                stdout=tmp_sql,
                env={
                    'PGPASSWORD': app.config['DATABASE_PASS'],
                    'SYSTEMROOT': os.environ.get('SYSTEMROOT', '')},
                check=True,
                capture_output=False,
                text=True)
        except subprocess.CalledProcessError as e:  # pragma: no cover
            g.logger.log(
                'error',
                'database',
                f'pg_dump for temporary SQL file failed ({e.returncode})')
            if os.path.exists(tmp_sql.name):
                os.unlink(tmp_sql.name)
            raise e

        return tmp_sql.name

def rdf_export() -> str:
    return rdf_export_to_file(
        Endpoint(
            ApiEntity.get_by_system_classes(['all']),
            {'format': 'nt'}).prepare_rdf_export_data(),
        app.config['RDF_PATH'] / f'{current_date_for_filename()}_export.nt')
