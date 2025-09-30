import re
from typing import Any

import pandas as pd
from psycopg2 import connect, extras

from openatlas import app
from openatlas.models.entity import Entity


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


def get_pious_data_from_csv() -> list[dict[str, Any]]:
    df_ = pd.read_csv("files/inscriptions.csv", dtype=str)
    df_ = df_.where(pd.notnull(df_), None)
    return df_.to_dict(orient="records")


def clean_data() -> None:
    for row in data:
        row["site"] = row["site"].rstrip(".")  # remove trailing .
        row["site"] = row["site"].replace(
            'province',
            'Province')  # corrected spelling
        row["site"] = re.sub(
            r"\s+", " ",
            row["site"]).strip()  # collapse spaces
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
            places_[entry['id_string']] = places_control_group[
                entry['placement']]
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


def get_current_location_types() -> dict[str, Entity]:
    current_locations_: dict[str, Entity] = {}
    for entry in data:
        if not entry.get('current_location'):
            continue
        if entry['current_location'] in current_locations_:
            continue
        print(entry.get('current_location'))
        current_location = Entity.insert('type', entry['current_location'])
        current_location.link('P127', current_location_hierarchy)
        current_locations_[entry['current_location']] = current_location
    return current_locations_


def insert_artifacts_and_sources() -> None:
    for entry in data:
        # Artifact
        artifact_desc = f"""
        {entry['date']}\n{entry['site2']}\n{entry['description']}"""
        artifact = Entity.insert('artifact', entry['id_string'], artifact_desc)
        location = Entity.insert(
            'object_location',
            f"Location of {entry['id_string']}")
        artifact.link('P53', location)
        artifact.link('P46', places[entry['id_string']], inverse=True)
        print(entry.get('current_location'))
        if entry.get('current_location'):
            artifact.link('P2', current_locations[entry['current_location']])
        # Todo: add images

        # Source
        source_desc = f"{entry['commentary']}\n{entry['source']}"
        source = Entity.insert('source', entry['id_string'], source_desc)
        source.link('P2', inscription_type)
        source.link('P2', language_types[entry.get('language') or 'Greek'])
        source.link('P128', artifact, inverse=True)
        transcription = Entity.insert(
            'source_translation',
            f'Transcription of {entry["id_string"]}',
            entry['transcription'])
        transcription.link('P2', original_text_type)
        transcription.link('P73', source, inverse=True)
        transcription_corrected = Entity.insert(
            'source_translation',
            f'Corrected transcription of {entry["id_string"]}',
            entry['transcription_corrected'])
        transcription_corrected.link('P2', original_text_corrected_type)
        transcription_corrected.link('P73', source, inverse=True)
        transcription_simplified = Entity.insert(
            'source_translation',
            f'Simplified transcription of {entry["id_string"]}',
            entry['transcription_simplified'])
        transcription_simplified.link('P2', original_text_normalized_type)
        transcription_simplified.link('P73', source, inverse=True)
        translation = Entity.insert(
            'source_translation',
            f'Translation of {entry["id_string"]}',
            entry['translation'])
        translation.link('P2', translation_type)
        translation.link('P73', source, inverse=True)

# If no database is available, comment the next 3 lines
data = get_pious_data_from_db()
df = pd.DataFrame(data)
df.to_csv("files/inscriptions.csv", index=False, encoding="utf-8")
data = get_pious_data_from_csv()
clean_data()

with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(784)
    admin_hierarchy = Entity.get_by_id(81)
    current_location_hierarchy = Entity.get_by_id(786)
    inscription_type = Entity.get_by_id(787)
    original_text_type = Entity.get_by_id(96)
    original_text_corrected_type = Entity.get_by_id(788)
    original_text_normalized_type = Entity.get_by_id(789)
    translation_type = Entity.get_by_id(97)
    language_types = {
        'Greek': Entity.get_by_id(792),
        'Russian': Entity.get_by_id(791)}
    provinces = get_provinces()
    admin_units = get_admin_units()
    places = get_places()
    current_locations = get_current_location_types()
    insert_artifacts_and_sources()
