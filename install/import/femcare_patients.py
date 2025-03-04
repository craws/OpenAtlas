from pathlib import Path
from typing import Optional

import pandas as pd


from openatlas import app
from openatlas.models.entity import Entity

file_path = Path('files/patientinnenbuch.csv')
date_format = "%d.%m.%Y"


def parse_csv():
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', dtype=str)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    df['Beginn'] = pd.to_datetime(
        df['Beginn'],
        format='%d.%m.%Y',
        errors='coerce')
    df['Ende'] = pd.to_datetime(
        df['Ende'],
        format='%d.%m.%Y',
        errors='coerce')

    return [
        Entry(
            text=row['Originaltext'],
            nr=row['Nr.'],
            begin=row['Beginn'],
            end=row['Ende'],
            name=row['Name'] if pd.notna(row['Name']) else 'Unbekannt',
            origin=row['Herkunft'] if pd.notna(row['Herkunft']) else '',
            diagnose=row['Diagnose'] if pd.notna(row['Diagnose']) else 'N/A',
            age=row['Alter'] if pd.notna(row['Alter']) else None,
            died=bool(pd.notna(row['Verst.']))
        ) for _, row in df.iterrows()]


class Entry:
    def __init__(self, text, nr, begin, end, name, origin, diagnose, age,
                 died):
        self.text = text
        self.nr = nr
        self.begin = begin
        self.end = end
        self.persons_name = name
        self.origin = origin
        self.diagnose = diagnose
        self.age = age
        self.died = died
        self.source = Source(self)
        self.person = Person(self)
        self.activity = Activity(self)


class Source:

    def __init__(self, entry: Entry):
        self.name = f'Patient record {entry.nr}'
        self.text = entry.text

    def insert_source(self) -> Entity:
        source_ = Entity.insert('source', self.name, self.text)
        source_.link('P2', case_study)
        return source_


class Person:

    def __init__(self, entry: Entry):
        self.name = entry.persons_name
        self.begin = entry.begin
        self.end = entry.end
        self.age = int(entry.age) if entry.age else None
        self.died = entry.died
        self.birth_date = self.get_day_of_birth()
        self.death_date = entry.end if self.died else None

    def get_day_of_birth(self) -> Optional[int]:
        if not self.age or (self.begin or self.end):
            return None
        if self.begin:
            return self.begin.year - self.age
        return self.end.year - self.age

    def insert_person(self) -> Entity:
        person_ = Entity.insert('person', self.name)
        person_.update({
            'attributes': {
                'end_from': self.death_date,
                'begin_from': self.birth_date}})
        person_.link('P2', case_study)
        return person_


class Activity:

    def __init__(self, entry: Entry):
        self.nr = entry.nr
        self.name = f'Patient visit {self.nr} of {entry.persons_name}'
        self.begin = entry.begin
        self.end = entry.end
        self.diagnose = entry.diagnose
        self.text = entry.text

    def insert_activity(self) -> Entity:
        activity_ = Entity.insert('activity', self.name, self.text)
        activity_.update({
            'attributes': {
                'end_from': self.begin,
                'begin_from': self.end}})
        activity_.link('P2', case_study)
        return activity_


def get_diagnose_types(entries_: list[Entry]) -> dict[str, Entity]:
    diagnose_types_ = {}
    for e_ in entries_:
        if e_.diagnose in diagnose_types_.keys():
            continue
        type_ = Entity.insert('type', e_.diagnose)
        type_.link('P127', diagnose_hierarchy)
        diagnose_types_[e_.diagnose] = type_
    return diagnose_types_


with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(357)
    diagnose_hierarchy = Entity.get_by_id(359)
    entries = parse_csv()
    diagnose_types = get_diagnose_types(entries)
    for e in entries:
        source = e.source.insert_source()
        person = e.person.insert_person()
        activity = e.activity.insert_activity()
        activity.link('P2', diagnose_types[e.diagnose])
        source.link('P67', person)
        source.link('P67', activity)
        activity.link('P11', person)
