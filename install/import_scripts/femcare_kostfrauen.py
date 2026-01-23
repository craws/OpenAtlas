import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

from openatlas import app
from openatlas.models.entity import Entity, insert

# todo:
#   * handle death
#   * Should we make events instead of membership to a group to handle death

FILE_PATH: Final = Path("install/import_scripts/Kostfrauen.csv")


@dataclass
class Entry:
    name: str
    entry_date: str
    death: bool
    leave_date: str
    description: str


def import_csv_data(file_path: Path) -> list[Entry]:
    entries_csv: list[Entry] = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            entries_csv.append(process_row(row))
    return entries_csv


def process_row(row: dict[str, str]) -> Entry:
    name: str = row.get("Name", "").strip()
    entry_date: str = row.get("Eintrittsdatum", "").strip()
    death_: str = row.get("Verstorben", "").strip()
    leave_date: str = row.get("Austrittsdatum", "").strip()
    description: str = row.get("Informationen", "").strip()

    fmt = "%d.%m.%Y"
    out_fmt = "%Y-%m-%d"

    e_date = datetime.strptime(entry_date, fmt).strftime(out_fmt)
    l_date = datetime.strptime(leave_date, fmt).strftime(out_fmt) \
        if leave_date else None

    return Entry(
        name=name,
        entry_date=e_date,
        death=death_ != "nein",
        leave_date=l_date,
        description=description)


with app.test_request_context():
    app.preprocess_request()
    entries = import_csv_data(FILE_PATH)
    case_study = Entity.get_by_id(19073)
    death = Entity.get_by_id(361)
    kostfrauen_group = Entity.get_by_id(19074)

    print('Remove former data')
    for item in case_study.get_linked_entities('P2', inverse=True):
        item.delete()
    print('\nFormer data removed')

    for entry in entries:
        entity = insert({
            'name': entry.name,
            'description': entry.description,
            'openatlas_class_name': 'person'})
        entity.link('P2', case_study)

        kostfrauen_group.link(
            'P107',
            entity,
            dates={
                'begin_from': entry.entry_date,
                'begin_to': None,
                'begin_comment': None,
                'end_from': entry.leave_date,
                'end_to': None,
                'end_comment': None})
