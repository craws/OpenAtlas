import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from typing import Any
from unidecode import unidecode
import pandas as pd
from flask import g
from flask_login import login_user

from openatlas import app, before_request
from openatlas.display.util2 import datetime64_to_timestamp
from openatlas.forms.util import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.imports import (
    Project, get_id_from_origin_id, import_data_)
from openatlas.models.user import User

ADMIN_PATH = Path('files/zbiva_admin.csv')
PLACE_PATH = Path('files/zbiva_places.csv')
BIBLIOGRAPHY_PATH = Path('files/zbiva_literature.csv')


# pylint: skip-file
@dataclass
class AdministrativeUnit:
    region: str
    district: str
    cadastre: str

def parse_admin_units() -> list[AdministrativeUnit]:
    df = pd.read_csv(ADMIN_PATH, delimiter=',', encoding='utf-8', dtype=str)
    df = df.rename(columns=lambda x: x.strip().lower())
    return [AdministrativeUnit(**row) for row in
            df[['region', 'district', 'cadastre']].to_dict(orient='records')]

#################################
# Code for Administrative units #
#################################

def normalize_name(name: str) -> str:
    """
    Normalize name for internal comparison only (case + accent insensitive).
    """
    return unidecode(name.strip().lower())

def import_and_get_administrative_units() -> dict[str, dict[str, Any]]:
    admin_cz_type = Entity.get_by_id(139570)
    entries = parse_admin_units()

    regions_ = {}
    districts_ = {}
    cadastres_ = {}

    for entry in entries:
        region_norm = normalize_name(entry.region)
        district_norm = normalize_name(entry.district)
        cadastre_norm = normalize_name(entry.cadastre)

        region_key = region_norm
        district_key = f"{region_norm}>{district_norm}"
        cadastre_key = f"{district_key}>{cadastre_norm}"

        if region_key not in regions_:
            region = Entity.insert('administrative_unit', entry.region)  # original name
            region.link('P89', admin_cz_type)
            regions_[region_key] = region.id

        if district_key not in districts_:
            district = Entity.insert('administrative_unit', entry.district)  # original name
            district.link('P89', Entity.get_by_id(regions_[region_key]))
            districts_[district_key] = district.id

        if cadastre_key not in cadastres_:
            cadastre = Entity.insert('administrative_unit', entry.cadastre)  # original name
            cadastre.link('P89', Entity.get_by_id(districts_[district_key]))
            cadastres_[cadastre_key] = cadastre.id

    print(f'\n{len(regions_)} regions were imported.')
    print(f'\n{len(districts_)} districts were imported.')
    print(f'\n{len(cadastres_)} cadastres were imported.')
    return {
        'regions': regions_,
        'districts': districts_,
        'cadastres': cadastres_}



def import_places() -> None:
    data = pd.read_csv(PLACE_PATH, delimiter=',', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data = data.fillna('')
    places_result: list[dict[str, Any]] = []
    for _, row in data.iterrows():
        places_result.append(row.to_dict())
    cadastres_ = admin_units['cadastres']
    for row in places_result:
        region_norm = normalize_name(row.get('region', ''))
        district_norm = normalize_name(row.get('district', ''))
        cadastre_norm = normalize_name(row.get('cadastre', ''))
        cadastre_key = f"{region_norm}>{district_norm}>{cadastre_norm}"

        if region_norm and district_norm and cadastre_norm:
            cadastre_id = cadastres_.get(cadastre_key, 0)
            row['administrative_unit_id'] = cadastre_id
    import_data_(project, 'place', places_result)






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
        project = Project.get_by_id(6)

        print('Importing administrative units \n')
        start_time_ = time.time()
        admin_units = import_and_get_administrative_units()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        before_request()

        print('Importing bibliography \n')
        start_time_ = time.time()
        import_bibliography()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print('Importing places \n')
        start_time_ = time.time()
        import_places()
        print(f"Execution time: {time.time() - start_time_:.6f} seconds \n")

        print(f"Total execution time: {time.time() - start_time:.6f} seconds")
