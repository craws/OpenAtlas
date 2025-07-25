from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import docx
import pandas as pd

from openatlas import app
from openatlas.api.import_scripts.util import get_exact_match
from openatlas.models.entity import Entity

FILE_PATH = Path('files/femcare')
SKELETON_PATH = FILE_PATH / 'skeletons'

# pylint: skip-file

DEBUG_MSG = defaultdict(list)


# Todo:
#   * I did install new package for reading docx: python3-docx


@dataclass
class Individual:
    se_id: int
    description: list
    probe_type: str
    find_type: str
    position: str
    orientation: str
    preservation: str
    dislocation: str
    age: str
    extraction: str


@dataclass
class ParsedStratigraphicUnit:
    id_: str
    se_id: int
    type: str
    name: str
    layer: str
    feature: str
    individual_id: Optional[int] = None


@dataclass
class Feature:
    id_: str
    obj_id: int
    name: str
    type: str
    se: list[str]
    description: str
    cut: str


@dataclass
class Find:
    id_: str
    f_id: int
    name: str
    material: str
    designation: str
    description: str
    dating: str
    stratigraphic_unit: str
    feature_id: str
    openatlas_class: str


@dataclass
class StratigraphicUnit:
    id_: str
    se_id: int
    name: str
    layer: str
    feature: str
    type: str
    description: Optional[list[str]] = None
    individual_id: Optional[int] = None
    probe_type: Optional[str] = None
    find_type: Optional[str] = None
    position: Optional[str] = None
    orientation: Optional[str] = None
    preservation: Optional[str] = None
    dislocation: Optional[str] = None
    age: Optional[str] = None
    extraction: Optional[str] = None


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
            name=f'Objekt {str(int(row[0])).strip()}',
            type=row[1].strip(),
            se=se_list,
            description=row[3] if pd.notna(row[3]) else None,
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
            name=f'SE {str(int(row[0])).strip()}',
            # convert to int cause of the leading zeros
            type=row[1],
            layer=row[2].strip(),
            individual_id=int(row[3]) if pd.notna(row[3]) else None,
            feature=f"feature_{int(row[4])}".strip()
            if pd.notna(row[4]) else '')
        se.append(entry_obj)
    return se


def parse_finds() -> list[Find]:
    df = pd.read_csv(FILE_PATH / 'finds.csv', delimiter=',')
    finds_ = []
    for index, row in df.iterrows():

        stratigraphic_unit = ''
        if pd.notna(row[1]):
            if row[1] == '-':
                stratigraphic_unit = ''
            elif '/' in row[1]:
                DEBUG_MSG['multiple_SE_in_finds'].append(row[1])
            elif '?' in row[1]:
                DEBUG_MSG['undecided_SE_in_finds'].append(row[1])
            else:
                stratigraphic_unit = f"stratigraphic_{int(row[1])}".strip()
        feature_ = ''
        if pd.notna(row[4]):
            if row[4] == '-':
                feature_ = ''
            else:
                feature_ = f"feature_{int(row[4])}".strip()

        entry_obj = Find(
            id_=f"find_{int(row[0])}".strip(),
            f_id=int(row[0]),
            stratigraphic_unit=stratigraphic_unit,
            feature_id=feature_,
            name=f"FNR {int(row[0])}",
            material=row[6] if pd.notna(row[6]) else '',
            designation=row[7] if pd.notna(row[7]) else '',
            description=row[8] if pd.notna(row[8]) else '',
            dating=row[9] if pd.notna(row[9]) else '',
            openatlas_class='human_remains'
            if row[6] == 'menschl. Kn.' else 'artifact')
        finds_.append(entry_obj)
    return finds_


def get_individuals() -> list[Individual]:
    output = []
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
                            probe_type = \
                                cells[2].text.replace('Art:', '').strip()
                        elif row_num == 3 and 'uf078' in repr(cells[1].text):
                            find_type = cells[2].text.strip()

                case 3:
                    for row_num, row in enumerate(table.rows):
                        cells = row.cells

                        if row_num == 0:
                            position = cells[0].text.replace('Lage:',
                                                             '').strip()
                            orientation = \
                                (cells[1].text.replace('Orientierung:', '')
                                 .strip())

                        elif row_num == 1:
                            preservation = \
                                (cells[0].text.
                                 replace('Erhaltungszustand:', '').strip())
                            dislocation = \
                                (cells[1].text.replace('Dislozierung:', '')
                                 .strip())

                        elif row_num == 2:
                            age = cells[0].text.replace('Alter:', '').strip()
                            extraction = \
                                cells[1].text.replace('Bergung:', '').strip()

                        elif row_num in range(3, 8):
                            text = cells[0].text
                            parts = text.split(':', 1)
                            if len(parts) == 2 and \
                                    parts[1].strip() not in ['-', '']:
                                description.append(text)

        output.append(Individual(
            se_id=int(se_id),
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
    for strat_unit in strat_units:
        ind = individual_lookup.get(int(strat_unit.se_id))
        merged.append(StratigraphicUnit(
            id_=strat_unit.id_,
            se_id=strat_unit.se_id,
            name=strat_unit.name,
            layer=strat_unit.layer,
            feature=strat_unit.feature,
            type=strat_unit.type,
            individual_id=strat_unit.individual_id,
            description=ind.description if ind else [],
            probe_type=ind.probe_type if ind else None,
            find_type=ind.find_type if ind else None,
            position=ind.position if ind else None,
            orientation=ind.orientation if ind else None,
            preservation=ind.preservation if ind else None,
            dislocation=ind.dislocation if ind else None,
            age=ind.age if ind else None,
            extraction=ind.extraction if ind else None))
    return merged


def build_types(
        entities: list,
        hierarchy: Entity,
        attribute: str) -> dict[str, Entity]:
    types: dict[str, Entity] = {}
    for entry in entities:
        key = getattr(entry, attribute, None)
        if not key or key in types:
            continue
        type_ = Entity.insert('type', key)
        type_.link('P127', hierarchy)
        types[key] = type_
    return types


def build_find_types(
        entities: list,
        attribute: str) -> dict[str, Entity]:
    types: dict[str, Entity] = {}
    for entry in entities:
        hierarchy = import_artifact_type
        if entry.material == 'menschl. Kn.':
            hierarchy = import_hr_type
        key = getattr(entry, attribute, None)
        if not key or key in types:
            continue
        type_ = Entity.insert('type', key)
        type_.link('P127', hierarchy)
        types[key] = type_
    return types


with app.test_request_context():
    app.preprocess_request()
    exact_match = get_exact_match()
    case_study = Entity.get_by_id(16305)
    place = Entity.get_by_id(145)
    feature_main_type = Entity.get_by_id(72)
    import_feature_type = Entity.insert('type', 'imported')
    import_feature_type.link('P127', feature_main_type)
    artifact_main_type = Entity.get_by_id(21)
    import_artifact_type = Entity.insert('type', 'imported')
    import_artifact_type.link('P127', artifact_main_type)
    hr_main_type = Entity.get_by_id(78)
    import_hr_type = Entity.insert('type', 'imported')
    import_hr_type.link('P127', hr_main_type)
    su_main_type = Entity.get_by_id(75)
    import_su_type = Entity.insert('type', 'imported')
    import_su_type.link('P127', su_main_type)

    # Get OpenAtlas reference systems
    ref_sys_finds = Entity.get_by_id(16307)
    ref_sys_indi = Entity.get_by_id(321)
    ref_sys_feat = Entity.get_by_id(16306)
    ref_sys_su = Entity.get_by_id(16308)

    # Get OpenAtlas hierarchies
    probe_hierarchy = Entity.get_by_id(16309)
    find_hierarchy = Entity.get_by_id(16310)
    position_hierarchy = Entity.get_by_id(16311)
    orientation_hierarchy = Entity.get_by_id(16312)
    preservation_hierarchy = Entity.get_by_id(16313)
    dislocation_hierarchy = Entity.get_by_id(16314)
    age_hierarchy = Entity.get_by_id(16315)
    extraction_hierarchy = Entity.get_by_id(16316)
    layer_hierarchy = Entity.get_by_id(16317)
    material_hierarchy = Entity.get_by_id(16318)
    designation_hierarchy = Entity.get_by_id(16319)
    dating_hierarchy = Entity.get_by_id(16320)
    cut_hierarchy = Entity.get_by_id(16323)

    # Get data out of documents
    features = parse_features()
    merged_units = merge_units(
        parse_stratigraphic_units(),
        get_individuals())
    finds = parse_finds()

    # Build type dictionaries from Feature
    feature_types = build_types(features, import_feature_type, 'type')
    cut_types = build_types(features, cut_hierarchy, 'cut')

    # Build type dictionaries from StratigraphicUnit
    su_types = build_types(merged_units, import_su_type, 'type')
    probe_types = build_types(merged_units, probe_hierarchy, 'probe_type')
    find_types = build_types(merged_units, find_hierarchy, 'find_type')
    position_types = build_types(merged_units, position_hierarchy, 'position')
    age_types = build_types(merged_units, age_hierarchy, 'age')
    layer_types = build_types(merged_units, layer_hierarchy, 'layer')
    orientation_types = build_types(
        merged_units, orientation_hierarchy, 'orientation')
    preservation_types = build_types(
        merged_units, preservation_hierarchy, 'preservation')
    dislocation_types = build_types(
        merged_units, dislocation_hierarchy, 'dislocation')
    extraction_types = build_types(
        merged_units, extraction_hierarchy, 'extraction')

    # Build type dictionaries from Find
    material_types = build_types(finds, material_hierarchy, 'material')
    dating_types = build_types(finds, dating_hierarchy, 'dating')

    designation_types = build_find_types(finds, 'designation')

    added_features: dict[str, Entity] = {}
    for entry in features:
        feature = Entity.insert('feature', entry.name, entry.description)
        feature.link('P2', case_study)
        feature.link('P2', feature_types[entry.type])
        if entry.cut:
            feature.link('P2', cut_types[entry.cut])
        feature.link('P46', place, inverse=True)
        ref_sys_feat.link(
            'P67',
            feature,
            str(entry.obj_id),
            type_id=exact_match.id)
        location = Entity.insert(
            'object_location',
            f"Location of {entry.name}")
        feature.link('P53', location)
        added_features[entry.id_] = feature

    added_stratigraphic: dict[str, Entity] = {}
    for entry in merged_units:
        su = Entity.insert(
            'stratigraphic_unit',
            entry.name,
            '\n'.join(entry.description))
        su.link('P2', case_study)
        su.link('P46', added_features[entry.feature], inverse=True)
        ref_sys_su.link(
            'P67',
            su,
            str(entry.se_id),
            type_id=exact_match.id)
        if entry.individual_id:
            ref_sys_indi.link(
                'P67',
                su,
                str(entry.individual_id),
                type_id=exact_match.id)
        location = Entity.insert(
            'object_location',
            f"Location of {entry.name}")
        su.link('P53', location)

        if entry.type:
            su.link('P2', su_types[entry.type])
        if entry.probe_type:
            su.link('P2', probe_types[entry.probe_type])
        if entry.find_type:
            su.link('P2', find_types[entry.find_type])
        if entry.position:
            su.link('P2', position_types[entry.position])
        if entry.orientation:
            su.link('P2', orientation_types[entry.orientation])
        if entry.preservation:
            su.link('P2', preservation_types[entry.preservation])
        if entry.dislocation:
            su.link('P2', dislocation_types[entry.dislocation])
        if entry.age:
            su.link('P2', age_types[entry.age])
        if entry.extraction:
            su.link('P2', extraction_types[entry.extraction])
        if entry.layer:
            su.link('P2', layer_types[entry.layer])

        added_stratigraphic[entry.id_] = su

    added_finds: dict[str, Entity] = {}
    for entry in finds:
        if entry.stratigraphic_unit:
            link_to_entity = added_stratigraphic.get(entry.stratigraphic_unit)
        elif entry.feature_id:
            link_to_entity = added_features.get(entry.feature_id)
        else:
            link_to_entity = place
        if not link_to_entity:
            DEBUG_MSG['no_super_for_finds'].append(entry.f_id)
            continue

        system_class = 'artifact'
        if entry.material == 'menschl. Kn.':
            system_class = 'human_remains'
        find = Entity.insert(system_class, entry.name, entry.description)
        find.link('P2', case_study)
        find.link('P46', link_to_entity, inverse=True)

        ref_sys_finds.link(
            'P67',
            find,
            str(entry.f_id),
            type_id=exact_match.id)
        location = Entity.insert(
            'object_location',
            f"Location of {entry.name}")
        find.link('P53', location)

        if entry.material:
            find.link('P2', material_types[entry.material])
        if entry.designation:
            find.link('P2', designation_types[entry.designation])
        if entry.dating:
            find.link('P2', dating_types[entry.dating])

    print(DEBUG_MSG)
