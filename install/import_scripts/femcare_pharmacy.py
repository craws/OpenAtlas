from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from openatlas import app
from openatlas.models.entity import Entity

FILE_PATH = Path('files/pharmacy.csv')


# pylint: skip-file

@dataclass
class Entry:
    acronym: str
    name: str
    translation: str


def parse_csv():
    df = pd.read_csv(FILE_PATH, delimiter=';', header=None)
    entries = []
    for index, row in df.iloc[1:].iterrows():
        acronym = row[0].strip() if pd.notna(row[0]) and str(
            row[0]).strip() not in ('?', '') else None
        name = row[1].strip() if pd.notna(row[1]) and str(
            row[1]).strip() not in ('?', '') else None
        translation = row[2].strip() if pd.notna(row[2]) and str(
            row[2]).strip() not in ('?', '') else None

        entry_obj = Entry(acronym=acronym, name=name, translation=translation)
        entries.append(entry_obj)
    return entries


with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(708)
    inventory_hierarchy = Entity.get_by_id(746)

    entries = parse_csv()
    acetum = Entity.insert('type', 'Acetum')
    acetum.link('P127', inventory_hierarchy)
    aqua = Entity.insert('type', 'Aqua')
    aqua.link('P127', inventory_hierarchy)
    baccae = Entity.insert('type', 'Baccae')
    baccae.link('P127', inventory_hierarchy)
    cortex = Entity.insert('type', 'Cortex')
    cortex.link('P127', inventory_hierarchy)
    cummi = Entity.insert('type', 'Cummi')
    cummi.link('P127', inventory_hierarchy)
    electuarium = Entity.insert('type', 'Electuarium')
    electuarium.link('P127', inventory_hierarchy)
    emplastrum = Entity.insert('type', 'Emplastrum')
    emplastrum.link('P127', inventory_hierarchy)
    flores = Entity.insert('type', 'Flores')
    flores.link('P127', inventory_hierarchy)
    folia = Entity.insert('type', 'Folia')
    folia.link('P127', inventory_hierarchy)
    gummi = Entity.insert('type', 'Gummi')
    gummi.link('P127', inventory_hierarchy)
    herba = Entity.insert('type', 'Herba')
    herba.link('P127', inventory_hierarchy)
    lapis = Entity.insert('type', 'Lapis')
    lapis.link('P127', inventory_hierarchy)
    lignum = Entity.insert('type', 'Lignum')
    lignum.link('P127', inventory_hierarchy)
    mercurius = Entity.insert('type', 'Mercurius')
    mercurius.link('P127', inventory_hierarchy)
    oleum = Entity.insert('type', 'Oleum')
    oleum.link('P127', inventory_hierarchy)
    pulvis = Entity.insert('type', 'Pulvis')
    pulvis.link('P127', inventory_hierarchy)
    radix = Entity.insert('type', 'Radix')
    radix.link('P127', inventory_hierarchy)
    saccharum = Entity.insert('type', 'Saccharum')
    saccharum.link('P127', inventory_hierarchy)
    sal = Entity.insert('type', 'Sal')
    sal.link('P127', inventory_hierarchy)
    semen = Entity.insert('type', 'Semen')
    semen.link('P127', inventory_hierarchy)
    species = Entity.insert('type', 'Species')
    species.link('P127', inventory_hierarchy)
    spiritus = Entity.insert('type', 'Spiritus')
    spiritus.link('P127', inventory_hierarchy)
    syrupus = Entity.insert('type', 'Syrupus')
    syrupus.link('P127', inventory_hierarchy)
    tinctura = Entity.insert('type', 'Tinctura')
    tinctura.link('P127', inventory_hierarchy)
    unguentum = Entity.insert('type', 'Unguentum')
    unguentum.link('P127', inventory_hierarchy)

    category_map = {
        'ACET.': acetum,
        'AQ.': aqua,
        'AQUA': aqua,
        'BACC.': baccae,
        'CORT': cortex,
        'CUM.': cummi,
        'CUMI': cummi,
        'EL.': electuarium,
        'ELECT.': electuarium,
        'ELELOS.': electuarium,
        'EMPL.': emplastrum,
        'FL': flores,
        'FLOR': flores,
        'FOL.': folia,
        'FOLIA': folia,
        'GUM': gummi,
        'HERB': herba,
        'LAP': lapis,
        'LIG.': lignum,
        'LIGN': lignum,
        'MERCUR': mercurius,
        'OL.': oleum,
        'PUL': pulvis,
        'PULV': pulvis,
        'RAD': radix,
        'SACH.': saccharum,
        'SACCHARIN.': saccharum,
        'SAL': sal,
        'SEM.': semen,
        'SP.': species,
        'SPEC.': species,
        'SPIR.': spiritus,
        'SYR.': syrupus,
        'TINCT.': tinctura,
        'TR.': tinctura,
        'UNG': unguentum}

    for entry in entries:

        name = entry.name
        if not name:
            name = entry.acronym

        description_ = entry.translation
        if not description_:
            description_ = None

        type_ = Entity.insert('type', name, description_)
        linked_to_specific_category = False
        if entry.acronym:
            for prefix, category_entity in category_map.items():
                if entry.acronym.startswith(prefix):
                    type_.link('P127', category_entity)
                    linked_to_specific_category = True

        if not linked_to_specific_category:
            type_.link('P127', inventory_hierarchy)

        artifact = Entity.insert('artifact', entry.acronym)
        artifact.link('P2', type_)
        artifact.link('P2', case_study)
        location = Entity.insert(
            'object_location',
            f"Location of {entry.acronym}")
        artifact.link('P53', location)
