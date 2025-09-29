import re
from typing import Any

import pandas as pd
from psycopg2 import connect, extras

from openatlas import app
from openatlas.models.entity import Entity


# CATEGORIES = ["Source", "Image", "Further Reading", "Further
# Bibliography", "Image Source"]


def get_pious_data_from_db() -> list[dict[str, Any]]:
    db = connect(
        database='pious',
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
        port=app.config['DATABASE_PORT'],
        host=app.config['DATABASE_HOST'])
    cursor = db.cursor(cursor_factory=extras.DictCursor)
    cursor.execute("SELECT * FROM public.inscriptions")
    return [dict(row) for row in cursor.fetchall()]


def clean_data() -> None:
    for row in data:
        row["site"] = row["site"].rstrip(".")  # remove trailing .
        row["site"] = row["site"].replace(
            'province', 'Province')  # corrected spelling
        row["site"] = re.sub(
            r"\s+", " ", row["site"]).strip()  # collapse spaces

        row['placement'] = row["placement"].rstrip(".")  # remove trailing .


def get_admin_units() -> dict[str, Entity]:
    admin_units_: dict[str, Entity] = {}
    for entry in data:
        if entry['site'] in admin_units_:
            continue

        site_name = entry['site']
        province_name = None
        if ", Province of" in entry['site']:
            split_site = entry['site'].split(',')
            site_name = split_site[0]
            province_name = split_site[1].strip()

        unit = Entity.insert('administrative_unit', site_name)
        unit.link('P89', provinces.get(province_name) or admin_hierarchy)
        admin_units_[entry['site']] = unit
    return admin_units_


def get_provinces() -> dict[str, Entity]:
    provinces_: dict[str, Entity] = {}
    for entry in data:
        if ", Province of" in entry['site']:
            split_site = entry['site'].split(',')
            province_name = split_site[1].strip()
            if province_name in provinces_:
                continue
            province = Entity.insert('administrative_unit', province_name)
            province.link('P89', admin_hierarchy)
            provinces_[province_name] = province
    return provinces_


def get_places() -> dict[str, Entity]:
    places_control_group: dict[str, Entity] = {}
    places_: dict[str, Entity] = {}
    for entry in data:
        if entry['placement'] in places_control_group:
            places_[entry['id_string']] = places_control_group[entry['placement']]
            continue
        place = Entity.insert('place', entry['placement'])
        place.link('P2', case_study)
        location = Entity.insert(
            'object_location',
            f"Location of {entry['placement']}")
        place.link('P53', location)
        location.link('P89', admin_units[entry['site']])
        places_control_group[entry['placement']] = place
        places_[entry['id_string']] = place
    return places_

def get_current_location_types()-> dict[str, Entity]:
    current_locations_: dict[str, Entity] = {}
    for entry in data:
        if not entry['current_location'] :
            continue
        if entry['current_location'] in current_locations_:
            continue
        current_location = Entity.insert('type', entry['current_location'])
        current_location.link('P127', current_location_hierarchy)
        current_locations_[entry['current_location']] = current_location
    return current_locations_

def get_artifacts() -> dict[str, Entity]:
    artifacts_: dict[str, Entity] = {}
    for entry in data:
        # todo: Maybe move commentary to source itself as new text with
        #   type "commentary"
        description = f"""
        {entry['site2']}\n{entry['description']}\n{entry['commentary']}"""
        artifact = Entity.insert('artifact', entry['id_string'], description)
        location = Entity.insert(
            'object_location',
            f"Location of {entry['id_string']}")
        artifact.link('P53', location)
        artifact.link('P46', places[entry['id_string']], inverse=True)
        if entry.get('current_location'):
            artifact.link('P2', current_locations[entry['current_location']])

    return artifacts_


data = get_pious_data_from_db()
clean_data()

# Just for debugging reasons
df = pd.DataFrame(data)
df.to_csv("files/inscriptions.csv", index=False, encoding="utf-8")

with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(784)
    admin_hierarchy = Entity.get_by_id(81)
    current_location_hierarchy = Entity.get_by_id(786)
    provinces = get_provinces()
    admin_units = get_admin_units()
    places = get_places()
    current_locations = get_current_location_types()
    artifacts = get_artifacts()
