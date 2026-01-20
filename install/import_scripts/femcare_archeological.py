from __future__ import annotations

import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd
from docx import Document

from openatlas import app
from openatlas.api.import_scripts.util import get_exact_match
from openatlas.models.entity import Entity, insert

FILE_PATH = Path('files/femcare')
SKELETON_PATH = FILE_PATH / '06_SE Protokollblätter' / ('Elisabethinen_SE '
                                                        'Protokolle')
SKELETON_IMAGE_PATH = FILE_PATH / 'skelett_mannchen'
UPLOAD = FILE_PATH / 'uploads'

SCHNITTE_PATH = FILE_PATH / "17_Fotodokumentation" / "Schnitte"

# pylint: skip-file

DEBUG_MSG = defaultdict(list)

FILE_INFO = {
    'creator': 'LH Novetus',
    'license_holder': 'LH Novetus',
    'public': True}


@dataclass
class Individual:
    se_id: int
    description: list
    probe_type: str
    # find_type: str
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


def build_se_ind_map(root: Path) -> dict[str, Path]:
    """
    Scan 'Schnitte' recursively and return mapping
    { 'SE_x_Ind_y': folder_path }.
    """
    out: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        name = path.name
        if name.startswith("SE_") and "_Ind_" in name:
            out[name] = path
    return out


def parse_features() -> list[Feature]:
    df = pd.read_csv(FILE_PATH / 'features.csv', delimiter=',')
    features_ = []
    current_cut = ''
    for index, row in df.iterrows():
        if "Schnitt" in row.iloc[0]:
            current_cut = row.iloc[0]
            continue
        se_raw = row.iloc[2]
        se_list = se_raw.split(", ") if pd.notna(se_raw) else []
        entry_obj = Feature(
            id_=f"feature_{int(row.iloc[0])}".strip(),
            obj_id=int(row.iloc[0]),
            name=f'Objekt {str(int(row.iloc[0])).strip()}',
            type=row.iloc[1].strip(),
            se=se_list,
            description=row.iloc[3] if pd.notna(row.iloc[3]) else None,
            cut=current_cut.strip())
        features_.append(entry_obj)
    return features_


def parse_stratigraphic_units() -> list[ParsedStratigraphicUnit]:
    df = pd.read_csv(FILE_PATH / 'se.csv', delimiter=',')
    se = []
    for index, row in df.iterrows():
        if pd.isna(row.iloc[2]) or row.iloc[2] == '':
            continue
        if pd.isna(row.iloc[4]) or row.iloc[4] == 0:
            DEBUG_MSG['no_feature_available'].append(int(row.iloc[0]))
            continue
        entry_obj = ParsedStratigraphicUnit(
            id_=f"stratigraphic_{int(row.iloc[0])}".strip(),
            se_id=int(row.iloc[0]),
            name=f'SE {str(int(row.iloc[0])).strip()}',
            # convert to int cause of the leading zeros
            type=row.iloc[1],
            layer=row.iloc[2].strip(),
            individual_id=int(row.iloc[3]) if pd.notna(row.iloc[3]) else None,
            feature=f"feature_{int(row.iloc[4])}".strip()
            if pd.notna(row.iloc[4]) else '')
        se.append(entry_obj)
    return se


def parse_finds() -> list[Find]:
    df = pd.read_csv(FILE_PATH / 'finds.csv', delimiter=',')
    finds_ = []
    for index, row in df.iterrows():

        stratigraphic_unit = ''
        if pd.notna(row.iloc[1]):
            if row.iloc[1] == '-':
                stratigraphic_unit = ''
            elif '/' in row.iloc[1]:
                DEBUG_MSG['multiple_SE_in_finds'].append(row.iloc[0])
            elif '?' in row.iloc[1]:
                DEBUG_MSG['undecided_SE_in_finds'].append(row.iloc[0])
            else:
                stratigraphic_unit = (f"stratigraphic_"
                                      f"{int(row.iloc[1])}").strip()
        feature_ = ''
        if pd.notna(row.iloc[4]):
            if row.iloc[4] == '-':
                feature_ = ''
            else:
                feature_ = f"feature_{int(row.iloc[4])}".strip()

        entry_obj = Find(
            id_=f"find_{int(row.iloc[0])}".strip(),
            f_id=int(row.iloc[0]),
            stratigraphic_unit=stratigraphic_unit,
            feature_id=feature_,
            name=f"FNR {int(row.iloc[0])}",
            material=row.iloc[6] if pd.notna(row.iloc[6]) else '',
            designation=row.iloc[7] if pd.notna(row.iloc[7]) else '',
            description=row.iloc[8] if pd.notna(row.iloc[8]) else '',
            dating=row.iloc[9] if pd.notna(row.iloc[9]) else '',
            openatlas_class='human_remains'
            if row.iloc[6] == 'menschl. Kn.' else 'artifact')
        finds_.append(entry_obj)
    return finds_


def parse_individual_docx(file_path: Path) -> Optional[Individual]:
    """Parse one DOCX file by reading table 2 and 4 directly."""
    doc = Document(str(file_path))
    tables = doc.tables
    if len(tables) < 4:
        return None

    # --- Table 2: contains SE id and general attributes ---
    t2 = tables[1]
    se_id = None
    for token in t2._cells:
        if token.text.startswith("SE"):
            try:
                se_id = int(
                    token.text.replace("SE", "").replace(":", "").strip())
                break
            except ValueError:
                continue
    if se_id is None:
        return None

    # --- Table 4: contains main archaeological info ---
    t4 = tables[3]
    fields = {
        "Lage": "",
        "Orientierung": "",
        "Erhaltungszustand": "",
        "Dislozierung": "",
        "Alter": "",
        "Bergung": "",
        "Art": ""}

    for row in t4.rows:
        cells = row.cells
        if len(cells) < 1:
            continue
        for cell in cells:
            text = cell.text.strip()
            splited_text = text.split(':')
            label = splited_text[0].strip()
            value = splited_text[1].strip() if len(splited_text) > 1 else ""
            if label in fields:
                fields[label] = value

    description_parts: list[str] = []
    desc_labels = {
        "Position(Objekt)+Beschreibung",
        "Grabkonstruktion",
        "Fundmaterial",
        "Grabmarkierung/ -überbau und -form",
        "Anmerkungen/ Skizze"}

    for row in t4.rows:
        cells = row.cells
        if len(cells) < 1:
            continue
        splited_text = cells[0].text.split(':')
        label = splited_text[0].strip()
        value = splited_text[1].strip() if len(splited_text) > 1 else ""
        if label in desc_labels and value and value != '-':
            description_parts.append(f"{label}: {value}")

    ind = Individual(
        se_id=se_id,
        description=description_parts,
        probe_type=fields["Art"],
        position=fields["Lage"],
        orientation=fields["Orientierung"],
        preservation=fields["Erhaltungszustand"],
        dislocation=fields["Dislozierung"],
        age=fields["Alter"],
        extraction=fields["Bergung"])
    return ind


def get_individuals() -> list[Individual]:
    output: list[Individual] = []
    for file1 in sorted(SKELETON_PATH.glob("Ind_*_SE_*.docx")):
        ind = parse_individual_docx(file1)
        if ind:
            output.append(ind)
    for file2 in sorted(SKELETON_PATH.glob("SE_*_Ind_*.docx")):
        ind = parse_individual_docx(file2)
        if ind:
            output.append(ind)
    return output


def merge_units(
        strat_units: list[ParsedStratigraphicUnit],
        individuals: list[Individual]) -> list[StratigraphicUnit]:
    individual_lookup = {ind.se_id: ind for ind in individuals}
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
            # find_type=ind.find_type if ind else None,
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
    for entry_ in entities:
        key_ = getattr(entry_, attribute, None)
        if not key_ or key_ in types:
            continue
        # type_ = Entity.insert('type', key_)
        type_ = insert({'name': key_, 'openatlas_class_name': 'type'})
        type_.link('P127', hierarchy)
        types[key_] = type_
    return types


def build_find_types(
        entities: list,
        attribute: str) -> dict[str, Entity]:
    types: dict[str, Entity] = {}
    for entry_ in entities:
        hierarchy = import_artifact_type
        if entry_.material == 'menschl. Kn.':
            hierarchy = import_hr_type
        key_ = getattr(entry_, attribute, None)
        if not key_ or key_ in types:
            continue
        # type_ = Entity.insert('type', key_)
        type_ = insert({'name': key_, 'openatlas_class_name': 'type'})
        type_.link('P127', hierarchy)
        types[key_] = type_
    return types


with app.test_request_context():
    app.preprocess_request()
    exact_match = get_exact_match()
    case_study = Entity.get_by_id(16305)
    folder_map = build_se_ind_map(SCHNITTE_PATH)
    cc_by_sa_type = Entity.get_by_id(50)

    print('Remove former data')
    for item in case_study.get_linked_entities('P2', inverse=True):
        item.delete()
    print('\nFormer data removed')

    skelett_maenchens = {}
    for file_ in SKELETON_IMAGE_PATH.iterdir():
        skelett_maenchens[file_.stem] = file_

    skelett_maenchens_files = {}
    for k, v in skelett_maenchens.items():
        key = f"SE_{k.split()[1].split('_')[0]}"
        if key not in skelett_maenchens_files:
            skelett_maenchens_files[key] = v

    place = Entity.get_by_id(145)
    feature_main_type = Entity.get_by_id(72)
    # import_feature_type = Entity.insert('type', 'imported')
    import_feature_type = insert(
        {'name': 'imported', 'openatlas_class_name': 'type'})
    import_feature_type.link('P127', feature_main_type)
    artifact_main_type = Entity.get_by_id(21)
    # import_artifact_type = Entity.insert('type', 'imported')
    import_artifact_type = insert(
        {'name': 'imported', 'openatlas_class_name': 'type'})
    import_artifact_type.link('P127', artifact_main_type)
    hr_main_type = Entity.get_by_id(78)
    # import_hr_type = Entity.insert('type', 'imported')
    import_hr_type = insert(
        {'name': 'imported', 'openatlas_class_name': 'type'})
    import_hr_type.link('P127', hr_main_type)
    su_main_type = Entity.get_by_id(75)
    # import_su_type = Entity.insert('type', 'imported')
    import_su_type = insert(
        {'name': 'imported', 'openatlas_class_name': 'type'})
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
        # feature = Entity.insert('feature', entry.name, entry.description)
        feature = insert({
            'name': entry.name,
            'description': entry.description,
            'openatlas_class_name': 'feature'})
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
        # location = Entity.insert(
        #     'object_location',
        #     f"Location of {entry.name}")
        location = insert({
            'name': f'Location of {entry.name}',
            'openatlas_class_name': 'object_location'})
        feature.link('P53', location)
        added_features[entry.id_] = feature

    added_stratigraphic: dict[str, Entity] = {}
    for entry in merged_units:
        # su = Entity.insert(
        #     'stratigraphic_unit',
        #     entry.name,
        #     '\n'.join(entry.description))
        su = insert({
            'name': entry.name,
            'description': '\n'.join(entry.description),
            'openatlas_class_name': 'stratigraphic_unit'})
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
        # location = Entity.insert(
        #     'object_location',
        #     f"Location of {entry.name}")
        location = insert({
            'name': f'Location of {entry.name}',
            'openatlas_class_name': 'object_location'})
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

        skelett_file = skelett_maenchens_files.get(f'SE_{entry.se_id}')
        if skelett_file:
            # file = Entity.insert(
            #     'file',
            #     f'SE {entry.se_id} Ind '
            #     f'{entry.individual_id} Skelettmännchen')
            file = insert({
                'name': f'SE {entry.se_id} Ind '
                        f'{entry.individual_id} Skelettmännchen',
                'openatlas_class_name': 'file'})
            file.save_file_info(FILE_INFO)
            file.link('P2', cc_by_sa_type)
            su.link('P67', file, inverse=True)

            ext = skelett_file.suffix
            dest = UPLOAD / f"{file.id}{ext}"
            UPLOAD.mkdir(parents=True, exist_ok=True)
            shutil.copy(skelett_file, dest)

        key = f"SE_{entry.se_id}_Ind_{entry.individual_id}"

        if folder := folder_map.get(key):
            images = [
                p for p in folder.iterdir()
                if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}]
            for idx, image in enumerate(images):
                # file = Entity.insert(
                #       'file',
                #       f'SE {entry.se_id} Ind '
                #       f'{entry.individual_id} {idx}')
                file = insert({
                    'name': f'SE {entry.se_id} Ind '
                            f'{entry.individual_id} {idx}',
                    'openatlas_class_name': 'file'})
                file.save_file_info(FILE_INFO)
                file.link('P2', cc_by_sa_type)
                su.link('P67', file, inverse=True)
                ext = image.suffix
                dest = UPLOAD / f"{file.id}{ext.lower()}"
                UPLOAD.mkdir(parents=True, exist_ok=True)
                shutil.copy(image, dest)

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
        # find = Entity.insert(system_class, entry.name, entry.description)
        find = insert({
            'name': entry.name,
            'description': entry.description,
            'openatlas_class_name': system_class})
        find.link('P2', case_study)
        find.link('P46', link_to_entity, inverse=True)

        ref_sys_finds.link(
            'P67',
            find,
            str(entry.f_id),
            type_id=exact_match.id)
        # location = Entity.insert(
        #     'object_location',
        #     f"Location of {entry.name}")
        location = insert({
            'name': f'Location of {entry.name}',
            'openatlas_class_name': 'object_location'})
        find.link('P53', location)

        if entry.material:
            find.link('P2', material_types[entry.material])
        if entry.designation:
            find.link('P2', designation_types[entry.designation])
        if entry.dating:
            find.link('P2', dating_types[entry.dating])

    print(DEBUG_MSG)
