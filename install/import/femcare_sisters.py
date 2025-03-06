from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from flask import g

from openatlas import app, before_request
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
    def convert_str_to_date(date_: str) -> list[date | str]:
        if not isinstance(date_, str):
            return ['', '']
        timespan = []
        if "????" in date_:
            date_ = date_.replace('????', '')
            timespan.append(f'1.1.{date_}')
            timespan.append(f'31.12.{date_}')
        if "??" in date_:
            date_ = date_.replace('??', '')
            timespan.append(f'1.{date_}')
            timespan.append(f'31.{date_}')
        try:
            if timespan:
                converted_dates = [datetime.strptime(d, '%d.%m.%Y').date()for d in timespan]
            else:
                converted_dates= [datetime.strptime(date_, '%d.%m.%Y').date(), '']
        except ValueError:
            converted_dates = ['', '']
        return converted_dates


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
            'begin_from': self.birthday[0],
            'begin_to': self.birthday[1],
            'end_from': self.death_date[0],
            'end_to': self.death_date[1]}})
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
    case_study = Entity.get_by_id(358)
    actor_function_hierarchy = Entity.get_by_id(14)
    elisabethinen_vienna = Entity.get_by_id(362)

    entries = parse_csv()
    rank_types = insert_rank_types(entries)
    before_request()  # needed to refresh g.types for update_links
    for entry in entries:
        sister = entry.sister.insert_sister()
        sister.update_links({
           'attributes': {
               'begin_from': entry.function.profess[0],
               'begin_to': entry.function.profess[1],
               'begin_comment': '',
               'end_from': entry.sister.death_date[0],
               'end_to': entry.sister.death_date[1],
               'end_comment': ''},
           'links': {
               'insert': [{
                   'property': 'P107',
                   'range': elisabethinen_vienna,
                   'description': '',
                   'inverse': True,
                   'type_id': rank_types[entry.rank].id,
                   'return_link_id': False}],
               'delete': set(),
               'delete_inverse': set()},
           'attributes_link': {
               'begin_from': entry.function.profess[0],
               'begin_to': entry.function.profess[1],
               'begin_comment': '',
               'end_from': entry.sister.death_date[0],
               'end_to': entry.sister.death_date[1],
               'end_comment': ''}
        }, new=True)
