import itertools
import time
from pathlib import Path
from typing import Any, Optional

import pandas as pd
from flask import g
from flask_login import login_user

from openatlas import app, before_request
from openatlas.display.util2 import datetime64_to_timestamp
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.imports import Project, get_id_from_origin_id, \
    import_data_
from openatlas.models.user import User

ADMIN_PATH = Path('files/relic_admin.csv')
GRAVE_PATH = Path('files/grave_fields.csv')
FORTRESSES_PATH = Path('files/fortresses.csv')
CHURCHES_PATH = Path('files/churches.csv')
MONASTERIES_PATH = Path('files/monasteries.csv')
BIBLIOGRAPHY_PATH = Path('files/bibliography.csv')


# pylint: skip-file
class AdministrativeUnit:
    def __init__(self, attributes_: dict[str, Any]) -> None:
        self.region = attributes_['region']
        self.district = attributes_['district']
        self.cadastre = attributes_['cadastre']


def parse_admin_units() -> list[AdministrativeUnit]:
    data = pd.read_csv(ADMIN_PATH, delimiter='\t', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    admin_result = []
    for _, row in data.iterrows():
        admin_result.append(AdministrativeUnit({
            'region': row['region'],
            'district': row['district'],
            'cadastre': row['cadastre']}))
    return admin_result


#################################
# Code for Administrative units #
#################################

def import_and_get_administrative_units() -> dict[str, dict[str, Any]]:
    admin_cz_type = Entity.get_by_id(117158)
    entries = parse_admin_units()

    regions_ = {}
    districts_ = {}
    cadastres_ = {}

    for region_id in g.types[117158].subs:
        region = Entity.get_by_id(region_id)
        regions_[region.name.lower()] = region.id
        for district_id in g.types[region.id].subs:
            district = Entity.get_by_id(district_id)
            districts_[district.name.lower()] = district.id
            for cadastre_id in g.types[district.id].subs:
                cadastre = Entity.get_by_id(cadastre_id)
                cadastres_[cadastre.name.lower()] = cadastre.id

    for entry in entries:
        if entry.region.lower() not in regions_:
            region = Entity.insert('administrative_unit', entry.region)
            region.link('P89', admin_cz_type)
            regions_[region.name.lower()] = region.id
        if entry.district.lower() not in districts_:
            district = Entity.insert('administrative_unit', entry.district)
            district.link(
                'P89', Entity.get_by_id(regions_[entry.region.lower()]))
            districts_[district.name.lower()] = district.id
        if entry.cadastre.lower() not in cadastres_:
            cadastre = Entity.insert('administrative_unit', entry.cadastre)
            cadastre.link(
                'P89', Entity.get_by_id(districts_[entry.district.lower()]))
            cadastres_[cadastre.name.lower()] = cadastre.id

    print(f'\n{len(regions_)} regions where imported.')
    print(f'\n{len(districts_)} districts where imported.')
    print(f'\n{len(cadastres_)} cadastres where imported.')
    return {
        'regions': regions_,
        'districts': districts_,
        'cadastres': cadastres_}


#######################
# Code for RELIC Type #
#######################

# def import_and_get_administrative_units() -> dict[str, dict[str, Any]]:
#    relic_type = Entity.get_by_id(255820)
#    relic_admin_type = Entity.insert('type', 'Administrative units')
#    relic_admin_type.link('P127', relic_type)
#    entries = parse_csv()
#    regions = {}
#    districts = {}
#    cadastres = {}
#    for entry in entries:
#        if entry.region.lower() not in regions:
#            region = Entity.insert('type', entry.region)
#            region.link('P127', relic_admin_type)
#            regions[region.name.lower()] = region.id
#        if entry.district.lower() not in districts:
#            district = Entity.insert('type', entry.district)
#            district.link('P127', Entity.get_by_id(regions[
#            entry.region.lower()]))
#            districts[district.name.lower()] = district.id
#        if entry.cadastre.lower() not in cadastres:
#            cadastre = Entity.insert('type', entry.cadastre)
#            cadastre.link('P127', Entity.get_by_id(districts[
#            entry.district.lower()]))
#            cadastres[cadastre.name.lower()] = cadastre.id
#    print(f'\n{len(regions)} regions where imported.')
#    print(f'\n{len(districts)} districts where imported.')
#    print(f'\n{len(cadastres)} cadastres where imported.')
#    return {'cadastres': cadastres}

def import_cemeteries() -> None:
    data = pd.read_csv(GRAVE_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    cementary_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        cementary_result.append(row.to_dict())
    for row in cementary_result:
        for key, value in row.items():
            if key in ['begin_from', 'begin_to', 'end_from', 'end_to']:
                value = value.split('-')
                value = [int(item) for item in value]
                value = value + [None] * (3 - len(value))
                value = datetime64_to_timestamp(form_to_datetime64(
                    value[0],
                    value[1],
                    value[2],
                    to_date=key in ['begin_to', 'end_to']))
                row[key] = value if all(value) else ''
            if key == 'cadastre':
                row['administrative_unit_id'] = str(
                    admin_units['cadastres'][value.lower()])
            if key == 'id':
                row['id'] = f'cemetery_{value}'
    import_data_(project, 'place', cementary_result)


def import_fortresses() -> None:
    data = pd.read_csv(
        FORTRESSES_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    fortress_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        fortress_result.append(row.to_dict())
    ref_key = 'reference_system_Archaeological_Map_of_the_Czech_Republic'
    for row in fortress_result:
        for key, value in row.items():
            if key == 'District':
                row['administrative_unit_id'] = (
                    str(admin_units['districts'][value.lower()]))
            if key == 'id':
                row['id'] = f'fortress_{value}'
            if key == ref_key and value:
                row[ref_key] = f'{value};exact_match'
    import_data_(project, 'place', fortress_result)


def import_churches() -> None:
    data = pd.read_csv(
        CHURCHES_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    church_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        church_result.append(row.to_dict())
    founders = {}
    for row in church_result:
        for key, value in row.items():
            if key in [
                'begin_from', 'begin_to', 'end_from', 'end_to'] and value:
                value = value.split('-')
                value = [int(item) for item in value]
                value = value + [None] * (3 - len(value))
                value = datetime64_to_timestamp(form_to_datetime64(
                    value[0],
                    value[1],
                    value[2],
                    to_date=key in ['begin_to', 'end_to']))
                row[key] = value if all(value) else ''
            if key == 'cadastre':
                row['administrative_unit_id'] = (
                    str(admin_units['cadastres'][value.lower()]))
            if key == 'founder' and value:
                founders[row['id']] = Entity.get_by_id(value)
    import_data_(project, 'place', church_result)
    for id_, founder in founders.items():
        church = Entity.get_by_id(int(get_id_from_origin_id(project, id_)))
        founding_event = Entity.insert(
            'modification',
            f'Foundation of {church.name}')
        founding_event.update({
            'attributes': {
                'begin_from': form_to_datetime64(
                    church.begin_from.astype(object).year, 0, 0),
                'begin_to': form_to_datetime64(
                    church.begin_to.astype(object).year, 0, 0, to_date=True),
                'end_from': form_to_datetime64(
                    church.begin_from.astype(object).year, 0, 0),
                'end_to': form_to_datetime64(
                    church.begin_to.astype(object).year, 0, 0, to_date=True)}})
        founding_event.link('P2', founding_event_type)
        founding_event.link('P2', relic_type)
        founding_event.link('P2', replico_type)
        founding_event.link('P31', church)
        founding_event.update_links(
            get_update_links_dict('P14', founder, creator_type.id),
            new=True)


def get_update_links_dict(
        property_: str,
        range_: Entity,
        type_id: Optional[int] = '',
        inverse: Optional[bool] = False) -> dict[str, Any]:
    return {
        'attributes': {
            'begin_from': '',
            'begin_to': '',
            'begin_comment': '',
            'end_from': '',
            'end_to': '',
            'end_comment': ''},
        'links': {
            'insert': [{
                'property': property_,
                'range': range_,
                'description': '',
                'inverse': inverse,
                'type_id': type_id,
                'return_link_id': False}],
            'delete': set(),
            'delete_inverse': set()},
        'attributes_link': {
            'begin_from': '',
            'begin_to': '',
            'begin_comment': '',
            'end_from': '',
            'end_to': '',
            'end_comment': ''}}


def import_monasteries() -> None:
    data = pd.read_csv(
        MONASTERIES_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    monasteries_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        monasteries_result.append(row.to_dict())
    founders = {}
    possessor_1 = {}
    possessor_2 = {}
    for row in monasteries_result:
        for key, value in row.items():
            if key in ['end_from']:
                value = row['end_to']
            if key in ['begin_to'] and not value:
                value = row['begin_from'].split('-')[0]
            if (key in [
                'begin_from', 'begin_to', 'end_from', 'end_to',
                'p1_dating_from_earliest', 'p1_dating_from_latest',
                'p1_dating_to_earliest', 'p1_dating_to_latest',
                'p2_dating_from_earliest', 'p2_dating_from_latest',
                'p2_dating_to_earliest', 'p2_dating_to_latest']
                    and value):
                value = value.split('-')
                value = [int(item) for item in value]
                value = value + [None] * (3 - len(value))
                value = datetime64_to_timestamp(form_to_datetime64(
                    value[0],
                    value[1],
                    value[2],
                    to_date=key in ['begin_to', 'end_to'] or 'latest' in key))
                row[key] = value if all(value) else ''
            if key == 'cadastre':
                row['administrative_unit_id'] = (
                    str(admin_units['cadastres'][value.lower()]))
    for row in monasteries_result:
        for key, value in row.items():
            if key == 'founder' and value:
                founders[row['id']] = Entity.get_by_id(value)
            if key == 'possessor1_id' and value:
                possessor_1[row['id']] = {
                    'possessor': Entity.get_by_id(value),
                    'founder': Entity.get_by_id(row.get('founder')) if row.get(
                        'founder') else None,
                    'begin_from': row.get('p1_dating_from_earliest'),
                    'begin_to': row.get('p1_dating_from_latest'),
                    'end_from': row.get('p1_dating_to_earliest'),
                    'end_to': row.get('p1_dating_to_latest')}
            if key == 'possessor2_id' and value:
                possessor_2[row['id']] = {
                    'possessor': Entity.get_by_id(value),
                    'founder': Entity.get_by_id(row.get('founder')) if row.get(
                        'founder') else None,
                    'begin_from': row.get('p2_dating_from_earliest'),
                    'begin_to': row.get('p2_dating_from_latest'),
                    'end_from': row.get('p2_dating_to_earliest'),
                    'end_to': row.get('p2_dating_to_latest')}

    import_data_(project, 'place', monasteries_result)

    for id_, founder in founders.items():
        monastery = Entity.get_by_id(int(get_id_from_origin_id(project, id_)))
        founding_event = Entity.insert(
            'modification',
            f'Foundation of {monastery.name}')
        founding_event.update({
            'attributes': {
                'begin_from': form_to_datetime64(
                    monastery.begin_from.astype(object).year, 0, 0),
                'begin_to': form_to_datetime64(
                    monastery.begin_from.astype(object).year, 0, 0, to_date=True),
                'end_from': form_to_datetime64(
                    monastery.begin_to.astype(object).year, 0, 0),
                'end_to': form_to_datetime64(
                    monastery.begin_to.astype(object).year, 0, 0, to_date=True)}})
        founding_event.link('P2', founding_event_type)
        founding_event.link('P2', relic_type)
        founding_event.link('P2', replico_type)
        founding_event.link('P31', monastery)
        founding_event.update_links(
            get_update_links_dict('P14', founder, creator_type.id),
            new=True)

    for id_, possessor1 in possessor_1.items():
        monastery = Entity.get_by_id(int(get_id_from_origin_id(project, id_)))
        ownership1_event = Entity.insert(
            'modification',
            f'Ownership of {monastery.name}')
        ownership1_event.update({
            'attributes': {
                'begin_from': possessor1['begin_from'],
                'begin_to': possessor1['begin_to'],
                'end_from': possessor1['end_from'],
                'end_to': possessor1['end_to']}})
        ownership1_event.link('P2', ownership_event_type)
        ownership1_event.link('P2', relic_type)
        ownership1_event.link('P2', replico_type)
        ownership1_event.link('P31', monastery)
        ownership1_event.update_links(
            get_update_links_dict(
                'P14', possessor1['possessor'], owner_type.id),
            new=True)


    for id_, possessor2 in possessor_2.items():
        monastery = Entity.get_by_id(int(get_id_from_origin_id(project, id_)))
        ownership2_event = Entity.insert(
            'modification',
            f'Ownership of {monastery.name}')
        ownership2_event.update({
            'attributes': {
                'begin_from': possessor2['begin_from'],
                'begin_to': possessor2['begin_to'],
                'end_from': possessor2['end_from'],
                'end_to': possessor2['end_to']}})
        ownership2_event.link('P2', ownership_event_type)
        ownership2_event.link('P2', relic_type)
        ownership2_event.link('P2', replico_type)
        ownership2_event.link('P31', monastery)
        ownership2_event.update_links(
            get_update_links_dict(
                'P14', possessor2['possessor'], owner_type.id),
            new=True)


def import_bibliography() -> None:
    data = pd.read_csv(
        BIBLIOGRAPHY_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    bib_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        bib_result.append(row.to_dict())
    import_data_(project, 'bibliography', bib_result)


if __name__ == "__main__":
    with app.test_request_context():
        start_time = time.time()
        app.preprocess_request()
        user = User.get_by_id(23)
        login_user(user)
        project = Project.get_by_id(5)
        founding_event_type = Entity.get_by_id(208862)
        ownership_event_type = Entity.get_by_id(208839)
        creator_type = Entity.get_by_id(19)
        owner_type= Entity.get_by_id(208851)
        # possessor_type = Entity.get_by_id(208860)
        # proprietor_type = Entity.get_by_id(208859)
        relic_type = Entity.get_by_id(221174)
        replico_type = Entity.get_by_id(198155)

        print('Importing administrative units \n')
        start_time_ = time.time()
        admin_units = import_and_get_administrative_units()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        before_request()

        print('Importing cemeteries \n')

        start_time_ = time.time()
        import_cemeteries()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print('Importing bibliography \n')

        start_time_ = time.time()
        import_bibliography()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print('Importing fortresses \n')

        start_time_ = time.time()
        import_fortresses()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print('Importing churches \n')

        start_time_ = time.time()
        import_churches()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print('Importing monasteries \n')

        start_time_ = time.time()
        import_monasteries()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")
        print(f"Total execution time: {time.time() - start_time:.6f} seconds")
