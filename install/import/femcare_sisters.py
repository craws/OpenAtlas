from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd

from openatlas import app
from openatlas.models.entity import Entity

file_path = Path('files/sisters.csv')


class Entry:
    def __init__(self, attributes: dict[str, Any]) -> None:
        self.number = attributes['number']
        self.name = attributes['name']
        self.birthday = self.convert_str_to_date(attributes['birthday'])
        self.death_date = self.convert_str_to_date(attributes['deathday'])
        self.profess = self.convert_str_to_date(attributes['profess'])
        self.rank = attributes['rank']
        self.bio = attributes['bio']
        self.duties = attributes['duties']
        self.sister = Sister(self)
        self.function = Function(self)

    @staticmethod
    def convert_str_to_date(date_: str) -> date | None:
        if not isinstance(date_, str):
            return None
        if date_.isdigit():
            date_ = f'1.1.{date_}'
        try:
            converted_date = datetime.strptime(date_, '%d.%m.%Y').date()
        except ValueError:
            converted_date = None
        return converted_date


class Sister:
    def __init__(self, entry_: Entry) -> None:
        self.name = entry_.name
        self.birthday = entry_.birthday
        self.death_date = entry_.death_date
        self.description = f'{entry_.duties}\n\n{entry_.bio}'
        self.number = entry_.number

    def insert_sister(self) -> Entity:
        sister_ = Entity.insert('person', self.name, self.description)
        sister_.update({'attributes': {
            'begin_from': self.birthday,
            'end_from': self.death_date}})
        sister_.link('P2', case_study)
        return sister_


class Function:
    def __init__(self, entry_: Entry) -> None:
        self.profess = entry_.profess
        self.rank = entry_.rank


def parse_csv() -> list[Entry]:
    data = pd.read_csv(file_path, delimiter='\t', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return [Entry({
        'number': row['Nummer'] if pd.notna(row['Stand']) else '',
        'name': row['Name'],
        'birthday': row['Geburtsdatum'],
        'profess': row['Professdatum'],
        'deathday': row['Sterbedatum'],
        'rank': row['Stand'] if pd.notna(row['Stand']) else 'N/A',
        'bio': row['Biographische Details'] if pd.notna(
            row['Biographische Details']) else '',
        'duties': row['Ämterlisten'] if pd.notna(row['Ämterlisten']) else ''})
        for _, row in data.iterrows()]


def insert_rank_types(entries_: list[Entry]) -> dict[str, Any]:
    stand_type = Entity.insert('type', 'Stand')
    stand_type.link('P127', actor_function_hierarchy)
    ranks_: dict[str, Entity] = {}
    for entry_ in entries_:
        if entry_.rank in ranks_ or not isinstance(entry_.rank, str):
            continue
        type_ = Entity.insert('type', entry_.rank)
        type_.link('P127', stand_type)
        ranks_[entry_.rank] = type_
    return ranks_


with app.test_request_context():
    app.preprocess_request()
    entries = parse_csv()
    case_study = Entity.get_by_id(358)
    actor_function_hierarchy = Entity.get_by_id(14)
    elisabethinen_vienna = Entity.get_by_id(362)
    rank_types = insert_rank_types(entries)
    for entry in entries:
        sister = entry.sister.insert_sister()

        if not isinstance(entry.rank, str):
            continue
        function_link = sister.link(
            'P107',
            elisabethinen_vienna,
            inverse=True,
            type_id=rank_types[entry.rank].id)
        #sister.update({
        #   'attributes': {
        #       'begin_from': entry.function.profess,
        #       'begin_to': '',
        #       'begin_comment': '',
        #       'end_from': entry.sister.death_date,
        #       'end_to': '',
        #       'end_comment': ''},
        #   'links': {
        #       'insert': [{
        #           'property': 'P107',
        #           'range': elisabethinen_vienna,
        #           'description': '',
        #           'inverse': True,
        #           'type_id': rank_types[entry.rank].id,
        #           'return_link_id': False}],
        #       'delete': set(),
        #       'delete_inverse': set()},
        #   'attributes_link': {
        #       'begin_from': entry.function.profess,
        #       'begin_to': '',
        #       'begin_comment': '',
        #       'end_from': entry.sister.death_date,
        #       'end_to': '',
        #       'end_comment': ''},
        #})
