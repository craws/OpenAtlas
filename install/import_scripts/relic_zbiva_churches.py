import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from shapely import Point
from shapely.geometry import mapping

from openatlas import app
from openatlas.database.imports import import_data
from openatlas.models.entity import Entity, insert

FILE_PATH: Final = Path("install/import_scripts/Romanske_cerkve.csv")


# todo: first_source -> Modification: Mentioning of XXX with timespan of date


@dataclass
class Entry:
    id: int
    name: str
    esd: int
    description: str
    point: Point
    established: str
    first_source: str | None
    last_source: str | None
    citation: Any # dict[str, dict[str, str]]


def process_citation(citation_strings: list[str]) -> dict[str, str]:
    citation_output = {}
    for citation_string in citation_strings:
        # todo: maybe it is best to check and change the strings if needed
        citations = citation_string.split(';')
        succeeding_name = ''
        for citation in citations:
            if 'ARKAS' in citation:
                continue  # todo: handle ARKAS in a special function
            splitted_citation = re.split(r':\s*|,\s*', citation)
            name = splitted_citation[0]
            if name.isdigit():
                name = succeeding_name
            else:
                succeeding_name = name
            try:
                citation_output[name] = splitted_citation[1]
            # todo: there are many failed citations, handle them
            except Exception:
                continue
    return citation_output


def csv_to_datamodel() -> list[Entry]:
    entries_csv: list[Entry] = []
    with open(FILE_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            entries_csv.append(process_row(row))
    return entries_csv


def process_row(row: dict[str, str]) -> Entry:
    id_: str = row.get("ID", "").strip()
    name: str = row.get("Name", "").strip()
    description: str = row.get("Description", "").strip()
    esd: str = row.get("EŠD", "").strip()
    latitude: str = row.get("Latitude", "").strip().replace(',', '.')
    longitude: str = row.get("Longitude", "").strip().replace(',', '.')
    first_source: str = row.get("Church first written source", "").strip()
    established: str = row.get("Established", "").strip()

    citation_strings = re.findall(r'\((.*?)\)', description)
    # Todo: description sploi for references. Make good function
    citation = process_citation(citation_strings)

    modification_date = []
    first_source_date = first_source.split('-')
    modification_date.append(first_source_date[0])
    if len(first_source_date) > 1:
        modification_date.append(first_source_date[1])
    else:
        modification_date.append(first_source_date[0])

    return Entry(
        id=int(id_),
        name=name,
        description=description,
        esd=int(esd),
        point=Point(float(longitude), float(latitude)),
        first_source=f'{modification_date[0]}-1-1' if first_source else None,
        last_source=f'{modification_date[1]}-12-31' if first_source else None,
        established=f'{established}-1-1',
        citation=citation)


with app.test_request_context():
    app.preprocess_request()
    entries = csv_to_datamodel()
    relic = Entity.get_by_id(221174)
    replico = Entity.get_by_id(198155)
    zbiva = Entity.get_by_id(239450)
    church_type = Entity.get_by_id(285)
    ZBIVA_PROJECT = 6

    for entry in entries:
        place = insert({
            'name': entry.name,
            'description': entry.description,
            'openatlas_class_name': 'place',
            'begin_from': entry.established})
        place.link('P2', relic)
        place.link('P2', replico)
        place.link('P2', zbiva)
        place.link('P2', church_type)

        geom = {
            "type": "Feature",
            "geometry": mapping(entry.point),
            "properties": {
                "name": "",
                "description": "",
                "id": -9999999999999,
                "shapeType": "centerpoint"}}
        geom_dict = {'point': f'[{json.dumps(geom)}]', 'line': '[]',
                     'polygon': '[]'}
        place.update_gis(geom_dict)
#
        modification = insert({
            'name': f'Foundation of {entry.name}',
            'description': '',
            'openatlas_class_name': 'modification',
            'begin_from': entry.first_source,
            'begin_to': entry.last_source})
        modification.link('P31', place)

        import_data(ZBIVA_PROJECT, place.id, 23, f'{entry.id}_church')
        import_data(
            ZBIVA_PROJECT,
            modification.id,
            23,
            f'{entry.id}_modification')
