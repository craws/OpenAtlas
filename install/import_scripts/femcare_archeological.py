from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import docx
import pandas as pd

from openatlas import app
from openatlas.models.entity import Entity

FILE_PATH = Path('files/femcare')
SKELETON_PATH = FILE_PATH / 'skeletons'

# pylint: skip-file

DEBUG_MSG = defaultdict(list)

# Todo:
#   * External Reference System for objnr, senr and fnr
#   * I did install new package for reading docx: python3-docx


@dataclass
class Individual:
    se_id: int
    description: list
    probe_type: str   # -> Type
    find_type: str  # -> Type
    position: str  # -> Type
    orientation: str  # -> Type
    preservation: str  # -> Type
    dislocation:str  # -> Type
    age:str  # -> Type
    extraction:str  # -> Type

@dataclass
class Feature:
    id_: str
    obj_id: int
    name: str
    se: list[str]
    description: str
    cut: str


@dataclass
class ParsedStratigraphicUnit:
    id_: str
    se_id: int
    name: str
    layer: str  # SE/IF -> Type
    skeleton: Optional[int]
    feature: str


@dataclass
class Find:
    id_: str
    f_id: int
    name: str
    material: str  # -> Type
    designation: str  # -> Type
    description: str
    dating: str  # -> Type
    stratigraphic_unit: str
    feature: str
    openatlas_class: str


@dataclass
class StratigraphicUnit:
    id_: str
    se_id: int
    name: str
    layer: str
    skeleton: Optional[int]
    feature: str
    description: Optional[list[str]] = None
    probe_type: Optional[str] = None
    find_type: Optional[str] = None
    position: Optional[str] = None
    orientation: Optional[str] = None
    preservation: Optional[str] = None
    dislocation: Optional[str] = None
    age: Optional[str] = None
    extraction: Optional[str] = None

# Todo: Do not forget, to handle situation, if no stratigraphic is available,
#   then go for feature, if no feature is available then go for place
# Todo: split  "menschl. Kn." to human remains
def parse_features() -> list[Feature]:
    df = pd.read_csv(FILE_PATH / 'features.csv', delimiter=',')
    features_ = []
    current_cut = ''
    for index, row in df.iterrows():
        if "Schnitt" in row[0]:
            current_cut = row[0]
            continue
        se_raw = row[2]
        se_list = se_raw.split(", ") if pd.notna(se_raw) else []
        entry_obj = Feature(
            id_=f"feature_{int(row[0])}".strip(),
            obj_id=int(row[0]),
            name=row[1].strip(),
            se=se_list,
            description=row[3],
            cut=current_cut.strip())
        features_.append(entry_obj)
    return features_


def parse_stratigraphic_units() -> list[ParsedStratigraphicUnit]:
    df = pd.read_csv(FILE_PATH / 'se.csv', delimiter=',')
    se = []
    for index, row in df.iterrows():
        if pd.isna(row[2]) or row[2] == '':
            continue
        if pd.isna(row[4]) or row[4] == 0:
            DEBUG_MSG['no_feature_available'].append(int(row[0]))
            continue
        entry_obj = ParsedStratigraphicUnit(
            id_=f"stratigraphic_{int(row[0])}".strip(),
            se_id=int(row[0]),
            name=row[1].strip(),
            layer=row[2].strip(),
            skeleton=int(row[3]) if pd.notna(row[3]) else None,
            feature=f"feature_{int(row[0])}".strip() if pd.notna(row[4]) else '')
        se.append(entry_obj)
    return se


def parse_finds() -> list[ParsedStratigraphicUnit]:
    df = pd.read_csv(FILE_PATH / 'finds.csv', delimiter=',')
    finds_ = []
    for index, row in df.iterrows():
        stratigraphic_unit=f"stratigraphic_{int(row[0])}".strip()
        if row[1] == '-':
            stratigraphic_unit = ''
        feature=f"feature_{int(row[0])}".strip()
        if row[4] == '-':
            feature=''

        entry_obj = Find(
            id_=f"find_{int(row[0])}".strip(),
            f_id=int(row[0]),
            stratigraphic_unit=stratigraphic_unit,
            feature=feature,
            name=f"Fund {int(row[0])}",
            material=row[6],
            designation=row[7],
            description=row[8],
            dating=row[9],
            openatlas_class='human_remains'
            if row[6] == 'menschl. Kn.' else 'artifact' )
        finds_.append(entry_obj)
    return finds_


def get_individuals() -> list[Individual]:
    output=[]
    for docx_file in SKELETON_PATH.glob('*.docx'):
        doc = docx.Document(docx_file)

        se_id = probe_type = find_type = None
        position = orientation = preservation = dislocation = None
        age = extraction = None
        description = []

        if not doc.tables:
            continue

        for table_num, table in enumerate(doc.tables):
            match table_num:
                case 1:
                    for row_num, row in enumerate(table.rows):
                        cells = row.cells

                        if row_num == 0:
                            se_id = cells[4].text.replace('SE:', '').strip()

                        elif row_num == 2 and 'uf078' in repr(cells[1].text):
                            probe_type = cells[2].text.replace('Art:', '').strip()

                        elif row_num == 3 and 'uf078' in repr(cells[1].text):
                            find_type = cells[2].text

                case 3:
                    for row_num, row in enumerate(table.rows):
                        cells = row.cells

                        if row_num == 0:
                            position = cells[0].text.replace('Lage:', '').strip()
                            orientation = cells[1].text.replace('Orientierung:', '').strip()

                        elif row_num == 1:
                            preservation = cells[0].text.replace('Erhaltungszustand:', '').strip()
                            dislocation = cells[1].text.replace('Dislozierung:', '').strip()

                        elif row_num == 2:
                            age = cells[0].text.replace('Alter:', '').strip()
                            extraction = cells[1].text.replace('Bergung:', '').strip()

                        elif row_num in range(3, 8):
                            text = cells[0].text
                            parts = text.split(':', 1)
                            if len(parts) == 2 and parts[1].strip() not in ['-', '']:
                                description.append(text)

        output.append(Individual(
            se_id=se_id,
            description=description,
            probe_type=probe_type,
            find_type=find_type,
            position=position,
            orientation=orientation,
            preservation=preservation,
            dislocation=dislocation,
            age=age,
            extraction=extraction))
    return output

def merge_units(
    strat_units: list[ParsedStratigraphicUnit],
    individuals: list[Individual]) -> list[StratigraphicUnit]:
    individual_lookup = {int(ind.se_id): ind for ind in individuals}
    merged = []
    for su in strat_units:
        ind = individual_lookup.get(int(su.se_id))
        merged.append(StratigraphicUnit(
            id_=su.id_,
            se_id=su.se_id,
            name=su.name,
            layer=su.layer,
            skeleton=su.skeleton,
            feature=su.feature,
            description=ind.description if ind else None,
            probe_type=ind.probe_type if ind else None,
            find_type=ind.find_type if ind else None,
            position=ind.position if ind else None,
            orientation=ind.orientation if ind else None,
            preservation=ind.preservation if ind else None,
            dislocation=ind.dislocation if ind else None,
            age=ind.age if ind else None,
            extraction=ind.extraction if ind else None))
    return merged



with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(16305)
    place = Entity.get_by_id(145)

    features = parse_features()
    strati_units = merge_units(parse_stratigraphic_units(), get_individuals())
    finds = parse_finds()

    print(DEBUG_MSG)

