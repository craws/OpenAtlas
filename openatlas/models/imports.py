from typing import Any, Optional

from flask import g
from flask_login import current_user
from shapely import wkt
from shapely.errors import WKTReadingError

from openatlas.api.import_scripts.util import get_match_types, \
    get_reference_system_by_name
from openatlas.database import imports as db
from openatlas.display.util2 import sanitize
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


class Project:
    def __init__(self, row: dict[str, Any]) -> None:
        self.id = row['id']
        self.name = row['name']
        self.count = row['count']
        self.description = row['description'] or ''
        self.created = row['created']
        self.modified = row['modified']


class Import:
    @staticmethod
    def insert_project(name: str, description: Optional[str] = None) -> int:
        return db.insert_project(
            name,
            description.strip() if description else None)

    @staticmethod
    def get_all_projects() -> list[Project]:
        return [Project(row) for row in db.get_all_projects()]

    @staticmethod
    def get_project_by_id(id_: int) -> Project:
        return Project(db.get_project_by_id(id_))

    @staticmethod
    def get_project_by_name(name: str) -> Optional[Project]:
        row = db.get_project_by_name(name)
        return Project(row) if row else None

    @staticmethod
    def delete_project(id_: int) -> None:
        db.delete_project(id_)

    @staticmethod
    def get_origin_ids(project: Project, origin_ids: list[str]) -> list[str]:
        return db.check_origin_ids(project.id, origin_ids)

    @staticmethod
    def check_duplicates(class_: str, names: list[str]) -> list[str]:
        return db.check_duplicates(class_, names)

    @staticmethod
    def update_project(project: Project) -> None:
        db.update_project(
            project.id,
            project.name,
            sanitize(project.description, 'text'))

    @staticmethod
    def check_type_id(type_id: str, class_: str) -> bool:
        if not type_id.isdigit() or int(type_id) not in g.types:
            return False
        if class_ not in g.types[
            g.types[int(type_id)].root[-1]].classes:  # pragma: no cover
            return False
        return True  # pragma: no cover

    @staticmethod
    def import_data(project: Project, class_: str, data: list[Any]) -> None:
        for row in data:
            entity = Entity.insert(
                class_,
                row['name'],
                row.get('description'))
            db.import_data(
                project.id,
                entity.id,
                current_user.id,
                origin_id=row.get('id'))

            # Dates
            entity.update({'attributes': {
                'begin_from': row.get('begin_from'),
                'begin_to': row.get('begin_to'),
                'begin_comment': row.get('begin_comment'),
                'end_from': row.get('end_from'),
                'end_to': row.get('end_to'),
                'end_comment': row.get('end_comment')}})

            # Types
            if row.get('type_ids'):
                for type_id in str(row['type_ids']).split():
                    if not Import.check_type_id(type_id, class_):
                        continue
                    entity.link('P2', g.types[int(type_id)])  # pragma no cover

            match_types = get_match_types()
            if row.get('external_reference_system'):
                for reference in row['external_reference_system'].split():
                    values = reference.split(';')
                    if (values[0] in g.reference_systems
                            and values[2] in match_types):
                        if reference_system := g.reference_systems[int(
                                values[0])]:  # pragma no cover
                            reference_system.link(
                                'P67',
                                entity,
                                values[1],
                                type_id=match_types[values[2]].id)

            if wikidata := row.get('wikidata'):
                values = wikidata.split(';')
                if len(values) == 2 and values[1] in match_types:
                    wikidata = get_reference_system_by_name('Wikidata')
                    wikidata.link(
                        'P67',
                        entity,
                        values[0],
                        type_id=match_types[values[1]].id)

            if geonames := row.get('geonames'):
                values = geonames.split(';')
                if len(values) == 2 and values[1] in match_types:
                    wikidata = get_reference_system_by_name('GeoNames')
                    wikidata.link(
                        'P67',
                        entity,
                        values[0],
                        type_id=match_types[values[1]].id)
            # Alias
            if class_ in ['place', 'person', 'group']:
                if aliases := row.get('alias'):
                    for alias_ in aliases.split(";"):
                        entity.link('P1', Entity.insert('appellation', alias_))

            # GIS
            if class_ in ['place', 'artifact']:
                location = Entity.insert(
                    'object_location',
                    f"Location of {row['name']}")
                entity.link('P53', location)
                try:
                    wkt_ = wkt.loads(row['wkt'])
                except WKTReadingError:  # pragma no cover
                    wkt_ = None
                if wkt_:
                    Gis.insert_wkt(
                        entity=entity,
                        location=location,
                        project=project,
                        wkt_=wkt_)
