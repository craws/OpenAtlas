import os
import shutil
import subprocess
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from flask import g, url_for
from rdflib import Graph

from openatlas import app
from openatlas.api.endpoints.endpoint import Endpoint
from openatlas.api.external.arche import ACDH, ArcheFileMetadata, \
    add_arche_file_metadata_to_graph
from openatlas.api.resources.api_entity import ApiEntity
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


def arche_export() -> Any:
    ext_metadata = app.config['ARCHE_METADATA']
    file_entities = Entity.get_by_class(['file'], types=True, aliases=True)
    if ext_metadata.get('typeIds'):
        file_entities = filter_by_type(
            file_entities,
            ext_metadata.get('typeIds'))
    arche_metadata = get_arche_metadata(file_entities)
    files_by_extension = defaultdict(list)
    for f in arche_metadata['files_path']:
        files_by_extension[normalize_extension(f.suffix)].append(f)

    rdf_dump = Endpoint(
        ApiEntity.get_by_system_classes(['all']),
        {'type_id': ext_metadata.get('typeIds'),
         'limit': 0,
         'format': 'turtle'}).resolve_entities()

    with tempfile.NamedTemporaryFile(
            mode='w+',
            suffix='.md',
            delete=False) as tmp_md:
        tmp_md.write("\n".join(
            create_failed_files_md(arche_metadata['missing'])))
        tmp_md_path = tmp_md.name

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
        tmp_sql_path = tmp_sql.name

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        md_path = temp_path / 'problematic_files.md'
        md_path.write_text(
            Path(tmp_md_path).read_text(encoding='utf-8'), encoding='utf-8')

        ttl_path = temp_path / 'files.ttl'
        ttl_path.write_text(arche_metadata['graph'])

        rdf_path = temp_path / 'rdf_dump.ttl'
        rdf_path.write_text(rdf_dump.get_data(as_text=True))

        for ext, files_list in files_by_extension.items():
            ext_dir = temp_path / ext
            ext_dir.mkdir(parents=True, exist_ok=True)
            for file_path in files_list:
                (ext_dir / file_path.name).write_bytes(
                    Path(file_path).read_bytes())

        export_path = app.config['EXPORT_PATH']
        export_path.mkdir(parents=True, exist_ok=True)

        archive_name = (
            f"{current_date_for_filename()}_"
            f"{ext_metadata['topCollection'].replace(' ', '_')}.zip")
        archive_file = export_path / archive_name

        with zipfile.ZipFile(archive_file, 'w') as archive:
            archive.write(md_path, arcname='problematic_files.md')
            archive.write(ttl_path, arcname='files.ttl')
            archive.write(tmp_sql_path, arcname='database_dump.sql')
            archive.write(rdf_path, arcname='rdf_dump.ttl')
            for ext, files_list in files_by_extension.items():
                for file_path in files_list:
                    archive.write(
                        temp_path / ext / file_path.name,
                        arcname=f'{ext}/{file_path.name}')
        return archive_file


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


def get_arche_metadata(entities: list[Entity]) -> dict[str, Any]:
    ext_metadata = app.config['ARCHE_METADATA']
    license_urls = {}
    arche_metadata_list = []
    missing = defaultdict(set)
    files_path = set()
    for entity in entities:
        if not g.files.get(entity.id):
            missing['No files'].add((entity.id, entity.name))
            continue
        if not entity.public:
            missing['Not public'].add((entity.id, entity.name))
        if not entity.standard_type:
            missing['No license'].add((entity.id, entity.name))
            continue
        if not entity.creator:
            missing['No creator'].add((entity.id, entity.name))
        if not entity.license_holder:
            missing['No license holder'].add((entity.id, entity.name))
        if entity.standard_type.id not in license_urls:
            for link_ in (
                    entity.standard_type.get_links('P67', inverse=True)):
                if link_.domain.class_.name == "external_reference":
                    license_urls[entity.standard_type.id] = (
                        link_.domain.name)
                    break
            if entity.standard_type.id not in license_urls:
                continue
        arche_metadata_list.append(
            ArcheFileMetadata.construct(
                entity,
                ext_metadata,
                license_urls[entity.standard_type.id]))
        files_path.add(g.files.get(entity.id))

    graph = Graph()
    graph.bind("acdh", ACDH)
    for metadata_obj in arche_metadata_list:
        add_arche_file_metadata_to_graph(graph, metadata_obj)
    return {
        'graph': graph.serialize(format="turtle"),
        'missing': missing,
        'files_path': files_path}
