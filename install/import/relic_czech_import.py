import itertools
import time
from pathlib import Path
from typing import Any

import pandas as pd
from flask import g
from flask_login import login_user

from openatlas import app, before_request
from openatlas.display.util2 import datetime64_to_timestamp
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.imports import Project, import_data_
from openatlas.models.user import User

ADMIN_PATH = Path('files/relic_admin.csv')
GRAVE_PATH = Path('files/grave_fields.csv')
FORTRESSES_PATH = Path('files/fortresses.csv')
BIBLIOGRAPHY_PATH = Path('files/bibliography.csv')
SPINNER = itertools.cycle(["|", "/", "-", "\\"])
COUNT = 0


# pylint: skip-file


class AdministrativeUnit:
    def __init__(self, attributes_: dict[str, Any]) -> None:
        self.region = attributes_['region']
        self.district = attributes_['district']
        self.cadastre = attributes_['cadastre']


def parse_admin_units() -> list[AdministrativeUnit]:
    data = pd.read_csv(ADMIN_PATH, delimiter='\t', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    result = []
    for _, row in data.iterrows():
        result.append(AdministrativeUnit({
            'region': row['region'],
            'district': row['district'],
            'cadastre': row['cadastre']}))
    return result


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
    # print(f'{len(not_imported)} entries couldn\'t be imported.')
    print(f"Execution time: {time.time() - start_time:.6f} seconds")
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
#    #print(f'{len(not_imported)} entries couldn\'t be imported.')
#    print(f"Execution time: {time.time() - start_time:.6f} seconds")
#    return {'cadastres': cadastres}

def import_cemeteries() -> None:
    data = pd.read_csv(GRAVE_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        result.append(row.to_dict())
    for row in result:
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
    import_data_(project, 'place', result)


def import_fortresses() -> None:
    data = pd.read_csv(
        FORTRESSES_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        result.append(row.to_dict())
    ref_key = 'reference_system_Archaeological_Map_of_the_Czech_Republic'
    for row in result:
        for key, value in row.items():
            if key == 'District':
                row['administrative_unit_id'] = (
                    str(admin_units['districts'][value.lower()]))
            if key == 'id':
                row['id'] = f'fortress_{value}'
            if key == ref_key and value:
                row[ref_key] = f'{value};exact_match'
    import_data_(project, 'place', result)


def import_bibliography() -> None:
    data = pd.read_csv(
        BIBLIOGRAPHY_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        result.append(row.to_dict())
    import_data_(project, 'bibliography', result)


if __name__ == "__main__":
    with app.test_request_context():
        app.preprocess_request()
        user = User.get_by_id(23)
        login_user(user)
        project = Project.get_by_id(5)
        start_time = time.time()
        print('Importing administrative units \n')
        admin_units = import_and_get_administrative_units()
        before_request()
        print('Importing cemeteries \n')
        # import_cemeteries()
        print('Importing bibliography \n')
        import_bibliography()
        print('Importing fortresses \n')
        import_fortresses()
