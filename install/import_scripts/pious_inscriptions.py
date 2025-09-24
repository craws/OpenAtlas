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


def get_admin_units():
    admin_units_: dict[str, Entity] = {}
    province_control: dict[str, Entity] = {}
    for entry in data:
        if entry['site'] in admin_units_:
            continue

        site_name = entry['site']
        province_name = None
        if ", Province of" in entry['site']:
            split_site = entry['site'].split(',')
            site_name = split_site[0]
            province_name = split_site[1].strip()
            if province_name in province_control:
                continue
            province = Entity.insert('administrative_unit', province_name)
            province.link('P89', admin_hierarchy)
            province_control[province_name] = province

        unit = Entity.insert('administrative_unit', site_name)
        unit.link('P89', province_control.get(province_name) or admin_hierarchy)
        admin_units_[entry['site']] = unit
    return admin_units_


def get_places():
    places_: dict[str, Entity] = {}
    for entry in data:
        if entry['placement'] in places_:
            continue
        place = Entity.insert('place', entry['placement'])
        place.link('P2', case_study)
        location = Entity.insert(
            'object_location',
            f"Location of {entry['placement']}")
        place.link('P53', location)
        location.link('P89', admin_units[entry['site']])
        places_[entry['placement']] = place
    return places_


data = get_pious_data_from_db()
clean_data()

# Just for debugging reasons
df = pd.DataFrame(data)
df.to_csv("inscriptions.csv", index=False, encoding="utf-8")

with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(784)
    admin_hierarchy = Entity.get_by_id(81)
    admin_units = get_admin_units()
    places = get_places()
