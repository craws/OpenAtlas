import itertools
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
from flask import g
from pandas import isnull

from openatlas import app
from openatlas.models.entity import Entity

FILE_PATH = Path('files/patientinnenbuch.csv')
SPINNER = itertools.cycle(["|", "/", "-", "\\"])
COUNT = 0
# pylint: skip-file


class Entry:
    def __init__(self, attributes_: dict[str, Any]) -> None:
        self.text = attributes_['text']
        self.number = attributes_['number']
        self.begin = self.convert_str_to_date(attributes_['begin'])
        self.end = self.convert_str_to_date(attributes_['end'])
        self.persons_name = attributes_['persons_name']
        self.origin = attributes_['origin']
        self.diagnose = attributes_['diagnose']
        self.age = attributes_['age']
        self.died = attributes_['died']
        #self.source = Source(self)
        self.person = Person(self)
        self.activity = Activity(self)

    @staticmethod
    def convert_str_to_date(date_: str) -> date | None:
        if not isinstance(date_, str):
            return None
        return datetime.strptime(date_, '%d.%m.%Y').date()


# class Source:
#
#     def __init__(self, entry_: Entry):
#         self.name = f'Patient record {entry_.number}'
#         self.text = entry_.text
#
#     def insert_source(self) -> Entity:
#         source_ = Entity.insert('source', self.name, self.text)
#         source_.link('P2', case_study)
#         return source_


class Person:

    def __init__(self, entry_: Entry) -> None:
        self.name = entry_.persons_name
        self.begin = entry_.begin
        self.end = entry_.end
        self.age = int(entry_.age) if entry_.age else None
        self.died = entry_.died
        self.birth_year = self.get_year_of_birth()
        self.death_date = entry_.end if self.died else None

    def get_year_of_birth(self) -> Optional[int]:
        birth_year = None
        if self.age and self.end:
            birth_year = int(self.end.year - self.age)
        elif self.age and self.begin:
            birth_year = int(self.begin.year - self.age)
        return birth_year

    def insert_person(self) -> Entity:
        person_ = Entity.insert('person', self.name)
        dates = {
            'begin_from': None,
            'begin_to': None,
            'end_from': self.death_date}
        if self.birth_year:
            birth_begin = str(self.birth_year - 1)
            birth_end = str(self.birth_year + 1)
            dates['begin_from'] = (
                np.datetime64(birth_begin, 'D'))  # type: ignore
            dates['begin_to'] = np.datetime64(
                f'{birth_end}-12-31')  # type: ignore
        person_.update({'attributes': dates})
        person_.link('P2', case_study)
        return person_


class Activity:

    def __init__(self, entry_: Entry):
        self.number = entry_.number
        self.name = f'Patient visit {self.number} of {entry_.persons_name}'
        self.begin = entry_.begin
        self.end = entry_.end
        self.diagnose = entry_.diagnose
        self.text = entry_.text
        self.died = entry_.died

    def insert_activity(self) -> Entity:
        activity_ = Entity.insert('activity', self.name, self.text)
        activity_.update({
            'attributes': {
                'begin_from': self.begin,
                'end_from': self.end}})
        activity_.link('P2', case_study)
        if self.died:
            activity_.link('P2', death_type)
        return activity_


def parse_csv() -> list[Entry]:
    data = pd.read_csv(FILE_PATH, delimiter=';', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    result = []
    for _, row in data.iterrows():
        result.append(Entry({
            'text': row['Originaltext'],
            'number': row['Nr.'],
            'begin': row['Beginn'],
            'end': row['Ende'],
            'persons_name': row['Name'] if pd.notna(
                row['Name']) else 'Unbekannt',
            'origin': row['Herkunft'] if pd.notna(row['Herkunft']) else '',
            'diagnose': row['Diagnose'] if pd.notna(
                row['Diagnose']) else 'N/A',
            'age': row['Alter'] if pd.notna(row['Alter']) else None,
            'died': bool(pd.notna(row['Verst.']))}))
    return result


def get_diagnose_types(entries_: list[Entry]) -> dict[str, Entity]:
    diagnose_types_: dict[str, Entity] = {}
    for entry_ in entries_:
        if entry_.diagnose in diagnose_types_:
            continue
        type_ = Entity.insert('type', entry_.diagnose)
        type_.link('P127', diagnose_hierarchy)
        diagnose_types_[entry_.diagnose] = type_
    return diagnose_types_


def get_origin_places(entries_: list[Entry]) -> dict[str, Entity]:
    origin_places_: dict[str, Entity] = {}
    for entry_ in entries_:
        if not entry_.origin or entry_.origin in origin_places_:
            continue
        place = Entity.insert('place', entry_.origin)
        place.link('P2', case_study)
        location = Entity.insert(
            'object_location',
            f"Location of {entry_.origin}")
        place.link('P53', location)
        origin_places_[entry_.origin] = location
    return origin_places_


with app.test_request_context():
    app.preprocess_request()
    start_time = time.time()
    case_study = Entity.get_by_id(357)
    diagnose_hierarchy = Entity.get_by_id(359)
    death_type = Entity.get_by_id(361)
    source = Entity.get_by_id(143)

    # Remove former data
    print('Remove former data\n')
    for item in case_study.get_linked_entities('P2', True):
        item.delete()
        COUNT += 1
        if COUNT % 15 == 0:
            sys.stdout.write(f"\rDeleting {next(SPINNER)}")
            sys.stdout.flush()
    print('Former data removed\n')

    for type_id in diagnose_hierarchy.subs:  # type: ignore
        g.types[type_id].delete()

    # Insert import
    entries = parse_csv()
    print('Parsed CSV')
    diagnose_types = get_diagnose_types(entries)
    print('Added diagnose types CSV')
    origin_places = get_origin_places(entries)
    print('Added places')

    not_imported = []
    for entry in entries:
        if isnull(entry.number):
            not_imported.append(entry)
            continue
        #source = entry.source.insert_source()
        person = entry.person.insert_person()
        activity = entry.activity.insert_activity()
        activity.link('P2', diagnose_types[entry.diagnose])
        source.link('P67', person)
        source.link('P67', activity)
        activity.link('P11', person)
        if entry.origin:
            person.link('OA8', origin_places[entry.origin])
        COUNT += 1
        if COUNT % 15 == 0:
            sys.stdout.write(f"\rProcessing {next(SPINNER)}")
            sys.stdout.flush()

    print(f'\n{COUNT} rows where imported.')
    print(f'{len(not_imported)} entries couldn\'t be imported.')
    print(f"Execution time: {time.time() - start_time:.6f} seconds")
