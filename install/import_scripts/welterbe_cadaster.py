import csv
from collections import defaultdict
from pathlib import Path

from openatlas import app
from openatlas.api.import_scripts.util import get_reference_system_by_name
from openatlas.models.entity import Entity, insert

# Download data from (Tab 'Distributionen/Distributions')
# https://www.data.gv.at/datasets/5a56bef7-7b60-4822-9da7-1d118f312a4d
# and store the needed CSV files in install/import_scripts/cadaster_data/

# Change the ID for the correct cadaster hierarchy
CADASTER_HIERARCHY_ID = 221484


def import_csv_data() -> dict[str, set[str]]:
    entries_csv = defaultdict(set)
    data_dir = Path('install/import_scripts/cadaster_data')
    for path in data_dir.iterdir():
        if path.is_file() and path.name != '.gitignore':
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    entries_csv[row["KG-NR"]].add(row["GST-NR"])
    return entries_csv


with app.test_request_context():
    app.preprocess_request()

    cadaster_hierarchy = Entity.get_by_id(CADASTER_HIERARCHY_ID)
    cadaster_reference_system = get_reference_system_by_name('Cadaster')
    entries = import_csv_data()
    cadaster_hierarchy_subs = {
        e.name: e for e in Entity.get_by_ids(cadaster_hierarchy.subs)}

    for kg_name, gst_list in entries.items():
        if kg_entity := cadaster_hierarchy_subs.get(kg_name):
            kg_subs = {e.name for e in Entity.get_by_ids(kg_entity.subs)}
            gst_list.difference_update(kg_subs)
        else:
            kg_entity = insert({
                'name': kg_name,
                'openatlas_class_name': 'administrative_unit'})
            kg_entity.link('P89', cadaster_hierarchy)
            kg_entity.link(
                'P67',
                cadaster_reference_system,
                kg_name,
                inverse=True)

        for gst_name in gst_list:
            gst_entity = insert({
                'name': gst_name,
                'openatlas_class_name': 'administrative_unit'})
            gst_entity.link('P89', kg_entity)
            gst_entity.link(
                'P67',
                cadaster_reference_system,
                f'{kg_name}/{gst_name}',
                inverse=True)
