from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import pandas as pd
import pdfplumber

from openatlas import app
from openatlas.api.import_scripts.util import get_exact_match
from openatlas.models.entity import Entity

FILE_PATH = Path('files/femcare')
SKELETON_PATH = FILE_PATH / 'skeletons'

# pylint: skip-file

DEBUG_MSG = defaultdict(list)


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
                DEBUG_MSG['multiple_SE_in_finds'].append(row[0])
            elif '?' in row[1]:
                DEBUG_MSG['undecided_SE_in_finds'].append(row[0])
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


# def get_individuals() -> list[Individual]:
#     output = []
#     for docx_file in SKELETON_PATH.glob('*.docx'):
#         doc = docx.Document(docx_file)
#
#         se_id = probe_type = find_type = None
#         position = orientation = preservation = dislocation = None
#         age = extraction = None
#         description = []
#
#         if not doc.tables:
#             continue
#
#         for table_num, table in enumerate(doc.tables):
#             match table_num:
#                 case 1:
#                     for row_num, row in enumerate(table.rows):
#                         cells = row.cells
#
#                         if row_num == 0:
#                             se_id = cells[4].text.replace('SE:', '').strip()
#                         elif row_num == 2 and 'uf078' in repr(cells[1].text):
#                             probe_type = \
#                                 cells[2].text.replace('Art:', '').strip()
#                         elif row_num == 3 and 'uf078' in repr(cells[1].text):
#                             find_type = cells[2].text.strip()
#
#                 case 3:
#                     for row_num, row in enumerate(table.rows):
#                         cells = row.cells
#
#                         if row_num == 0:
#                             position = cells[0].text.replace(
#                                 'Lage:','').strip()
#                             orientation = \
#                                 (cells[1].text.replace('Orientierung:', '')
#                                  .strip())
#
#                         elif row_num == 1:
#                             preservation = \
#                                 (cells[0].text.
#                                  replace('Erhaltungszustand:', '').strip())
#                             dislocation = \
#                                 (cells[1].text.replace('Dislozierung:', '')
#                                  .strip())
#
#                         elif row_num == 2:
#                             age = cells[0].text.replace('Alter:', '').strip()
#                             extraction = \
#                                 cells[1].text.replace('Bergung:', '').strip()
#
#                         elif row_num in range(3, 8):
#                             text = cells[0].text
#                             parts = text.split(':', 1)
#                             if len(parts) == 2 and \
#                                     parts[1].strip() not in ['-', '']:
#                                 description.append(text)
#
#         output.append(Individual(
#             se_id=int(se_id),
#             description=description,
#             probe_type=probe_type,
#             find_type=find_type,
#             position=position,
#             orientation=orientation,
#             preservation=preservation,
#             dislocation=dislocation,
#             age=age,
#             extraction=extraction))
#     return output

# import re
# from pdfminer.high_level import extract_text
#
# # --- helpers for PDF parsing ---
#
# LABEL_PATTERN = re.compile(r"^\s*([\wÄÖÜäöüß()/+\- ]+)\s*:\s*(.*)$")
#
#
# def _norm(s: str | None) -> str | None:
#     if not s:
#         return None
#     s = " ".join(s.split())
#     return s if s not in ("", "-") else None
#
# def _is_label_line(line: str) -> bool:
#     return bool(LABEL_PATTERN.match(line))
#
# def _collect_until_next_label(start_idx: int, lines: list[str],
# break_tokens=("SE:",)) -> str:
#     """Collect text for a field until the next label or header-like line."""
#     m = LABEL_PATTERN.match(lines[start_idx])
#     if not m:
#         return ""
#     acc = [m.group(2).strip()]
#     i = start_idx + 1
#     while i < len(lines):
#         line = lines[i].strip()
#         if not line:
#             i += 1
#             continue
#
#         # Stop if the line looks like a new label or header
#         if any(line.startswith(tok) for tok in break_tokens):
#             break
#         if LABEL_PATTERN.match(line):
#             break
#         if re.match(r"^[A-ZÄÖÜ][A-Za-zÄÖÜäöüß\s\-]{2,}:", line):
#             break
#         if any(header in line for header in [
#             "Erhaltene", "Position", "Beschreibung", "Skizze",
#             "Dokumentation"
#         ]):
#             break
#
#         acc.append(line)
#         i += 1
#
#     text = " ".join(acc).strip()
#     # Shorten if field is supposed to be a short code like "Bergung" or
#     "Alter"
#     if m.group(1).strip().lower() in ("bergung", "alter") and len(
#     text.split()) > 6:
#         text = " ".join(text.split()[:5])
#     return text
#
#
#
# def parse_section(section_text: str) -> Individual | None:
#     lines = [l.rstrip() for l in section_text.splitlines()]
#     print(lines)
#     se_id = None
#     for line in lines:
#         m = re.search(r"\bSE\s*:\s*(\d+)\b", line)
#         if m:
#             se_id = int(m.group(1))
#             break
#     if se_id is None:
#         return None
#
#     def fetch(label: str) -> str | None:
#         for idx, line in enumerate(lines):
#             if re.match(rf"^\s*{re.escape(label)}\s*:", line):
#                 #return _norm(_collect_until_next_label(idx,
#                 lines)).replace('ObjGr.(Nr):', '')
#                 return _norm(_collect_until_next_label(idx, lines))
#
#         return None
#
#     position     = fetch("Lage")
#     orientation  = fetch("Orientierung")
#     preservation = fetch("Erhaltungszustand")
#     dislocation  = fetch("Dislozierung")
#     age          = fetch("Alter")
#     extraction   = fetch("Bergung")
#     probe_type   = fetch("Art")
#
#     # handle find_type with flexible labels
#     find_type = None
#     for candidate in ("Fundart", "Fund", "Befund", "Bestattungsart"):
#         find_type = fetch(candidate)
#         if find_type:
#             break
#
#     # --- description: only keep specific meaningful fields ---
#     wanted_labels = [
#         "Position(Objekt)+Beschreibung",
#         "Grabkonstruktion",
#         "Fundmaterial",
#         "Grabmarkierung/ -überbau und -form",
#         "Anmerkungen/ Skizze"]
#
#     description = []
#     for idx, line in enumerate(lines):
#         m = LABEL_PATTERN.match(line)
#         if not m:
#             continue
#
#         label = m.group(1)
#         if label not in wanted_labels:
#             continue
#         value = m.group(2)
#
#         # --- Handle cases where value is below the label (next 1–2 lines)
#         ---
#         if value in ("", "-"):
#             for offset in (1, 2):
#                 if idx + offset < len(lines):
#                     nxt = lines[idx + offset].strip()
#                     # skip empty or label-like lines
#                     if nxt and not LABEL_PATTERN.match(nxt):
#                         value = nxt
#                         break
#
#         # --- Skip if still empty or only '-' ---
#         if not value or value == "-":
#             continue
#
#         # --- Collect continuation lines, but stop early at known headers ---
#         cont = []
#         for j in range(idx + 1, len(lines)):
#             nxt = lines[j].strip()
#             if not nxt:
#                 continue
#             if LABEL_PATTERN.match(nxt):
#                 break
#             if re.match(r"^(Darstellung|Anmerkungen|Datum|BearbeiterIn|MNr
#             |KG|MBez)\b", nxt):
#                 break
#             if any(h in nxt for h in [
#                 "Darstellung der stratigraphischen Verhältnisse",
#                 "Anmerkungen", "Datum", "BearbeiterIn", "MNr"
#             ]):
#                 break
#             cont.append(nxt)
#
#         # Prefer continuation text if found, otherwise current value
#         text_value = " ".join(cont).strip() if cont else value
#         text_value = _norm(text_value)
#         if not text_value or text_value == "-":
#             continue
#
#         # Keep the label in output
#         description.append(f"{label}: {text_value}")
#
#     return Individual(
#         se_id=se_id,
#         description=description,
#         probe_type=probe_type,
#         find_type=find_type,
#         position=position,
#         orientation=orientation,
#         preservation=preservation,
#         dislocation=dislocation,
#         age=age,
#         extraction=extraction)
#
# def split_sections_by_se(full_text: str) -> list[str]:
#     anchors = list(re.finditer(r"\bSE\s*:\s*\d+\b", full_text))
#     if not anchors:
#         return [full_text]
#     sections = []
#     for idx, m in enumerate(anchors):
#         start = m.start()
#         end = anchors[idx+1].start() if idx+1 < len(anchors) else len(
#         full_text)
#         sections.append(full_text[start:end])
#     return sections



SE_PATTERN = re.compile(r"\bSE\s*:\s*(\d+)\b")

# basic Label: Value pattern
LABEL_PATTERN = re.compile(r"^\s*([\wÄÖÜäöüß()/+\- ]+)\s*:\s*(.*)$")

# mapping for simple one-liners
SHORT_FIELDS = {
    "Lage": "position",
    "Orientierung": "orientation",
    "Erhaltungszustand": "preservation",
    "Dislozierung": "dislocation",
    "Alter": "age",
    "Bergung": "extraction",
    "Art": "probe_type",
}

# descriptive labels to merge into one text block
DESCRIPTION_FIELDS = {
    "Position(Objekt)+Beschreibung",
    "Grabkonstruktion",
    "Fundmaterial",
    "Grabmarkierung/ -überbau und -form",
    "Anmerkungen/ Skizze",
}


def extract_se_records(pdf_path: str | Path) -> Iterator[dict[str, str]]:
    """Yield parsed SE entries from SE-Protokolle PDF."""
    pdf_file = Path(pdf_path)
    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            matches = list(SE_PATTERN.finditer(text))
            if not matches:
                continue

            record: dict[str, str] = {"page": str(page_num)}

            # use last SE found on the page
            record["se_number"] = matches[-1].group(1)

            last_label: str | None = None
            description_parts: list[str] = []

            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue

                m = LABEL_PATTERN.match(line)
                if m:
                    label = m.group(1).strip()
                    value = m.group(2).strip()

                    # short fields
                    if label in SHORT_FIELDS:
                        record[SHORT_FIELDS[label]] = value
                        last_label = label

                    # description fields → accumulate multiline block
                    elif label in DESCRIPTION_FIELDS:
                        block = f"{label}: {value}".strip()
                        description_parts.append(block)
                        last_label = "description"

                    else:
                        last_label = None

                elif last_label == "description":
                    description_parts.append(line)

                elif last_label in SHORT_FIELDS and line:
                    # line continuation for short field
                    record[SHORT_FIELDS[last_label]] += " " + line

            # join all description fields with newlines
            if description_parts:
                record["description"] = "\n".join(description_parts)

            yield record


def extract_all_se_records(pdf_path: str | Path) -> list[dict[str, str]]:
    """Return all SE records from given PDF."""
    return list(extract_se_records(pdf_path))



# todo: start here for SE
def get_individuals() -> list[Individual]:
    """Parse all SE-Protokolle PDFs and return Individuals."""
    pdf_dir = FILE_PATH / "06_SE Protokollblätter"
    output: list[Individual] = []

    for pdf_file in sorted(pdf_dir.glob("Schnitt *_SE-Protokolle.pdf")):
        tables = extract_all_se_records(pdf_file)
        print(f"Extracted {len(tables)} SE entries.")
        for rec in tables[:3]:
            print(f"\nSE {rec['se_number']}:")
            for k, v in rec.items():
                if k not in {"page", "se_number"}:
                    print(f"  {k}: {v[:120]}")
        # text = extract_text(str(pdf_file))
        # sections = split_sections_by_se(text)
        # for sec in sections:
        #     ind = parse_section(sec)
        #     if ind:
        #         output.append(ind)

    return output


# Todo: start here for images
# def extract_images_from_pdfs() -> None:
#    """Extract images from SE PDFs and remove duplicate (e.g. logo) images."""
#    out_dir = FILE_PATH / "skelett_mannchen"
#    out_dir.mkdir(parents=True, exist_ok=True)
#
#    pdf_dir = FILE_PATH / "06_SE Protokollblätter"
#
#    for pdf_file in sorted(pdf_dir.glob("Schnitt *_SE-Protokolle.pdf")):
#        doc = fitz.open(pdf_file)
#        for page_index, page in enumerate(doc):
#            text = page.get_text()
#            # detect SE number
#            m = re.search(r"\bSE\s*:\s*(\d+)\b", text)
#            se_number = m.group(1) if m else f"{pdf_file.stem}_p{
#            page_index+1}"
#            # detect Ind number
#            i = re.search(r"\bIndividuum\s*:\s*(\d+)\b", text)
#            ind_number = i.group(1) if i else f"{pdf_file.stem}_p{
#            page_index+1}"
#
#            for img_index, img in enumerate(page.get_images(full=True)):
#                xref = img[0]
#                pix = fitz.Pixmap(doc, xref)
#                if pix.n > 3:  # convert RGBA → RGB
#                    pix = fitz.Pixmap(fitz.csRGB, pix)
#                img_path = out_dir / f"SE {se_number}_{ind_number}_{
#                img_index+1}.jpg"
#                pix.save(img_path)
#                pix = None
#        doc.close()
#
#    # --- remove duplicates ---
#    seen = {}
#    for img_file in sorted(out_dir.glob("*.jpg")):
#        size = os.path.getsize(img_file)
#        if size not in seen:
#            seen[size] = [img_file]
#            continue
#        if size > 150_000:
#            continue
#        # potential duplicates → hash check
#        current_hash = hashlib.sha256(img_file.read_bytes()).hexdigest()
#        is_duplicate = False
#        for existing in seen[size]:
#            existing_hash = hashlib.sha256(existing.read_bytes()).hexdigest()
#            if current_hash == existing_hash:
#                img_file.unlink(missing_ok=True)  # remove duplicate
#                is_duplicate = True
#                break
#        if not is_duplicate:
#            seen[size].append(img_file)
#

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
    for entry_ in entities:
        key = getattr(entry_, attribute, None)
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
    for entry_ in entities:
        hierarchy = import_artifact_type
        if entry_.material == 'menschl. Kn.':
            hierarchy = import_hr_type
        key = getattr(entry_, attribute, None)
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
    get_individuals()
    # Remove former data
    # print('Remove former data')
    # for item in case_study.get_linked_entities('P2', True):
    #     item.delete()
    # print('\nFormer data removed')
#
#
# place = Entity.get_by_id(145)
# feature_main_type = Entity.get_by_id(72)
# import_feature_type = Entity.insert('type', 'imported')
# import_feature_type.link('P127', feature_main_type)
# artifact_main_type = Entity.get_by_id(21)
# import_artifact_type = Entity.insert('type', 'imported')
# import_artifact_type.link('P127', artifact_main_type)
# hr_main_type = Entity.get_by_id(78)
# import_hr_type = Entity.insert('type', 'imported')
# import_hr_type.link('P127', hr_main_type)
# su_main_type = Entity.get_by_id(75)
# import_su_type = Entity.insert('type', 'imported')
# import_su_type.link('P127', su_main_type)
#
# # Get OpenAtlas reference systems
# ref_sys_finds = Entity.get_by_id(16307)
# ref_sys_indi = Entity.get_by_id(321)
# ref_sys_feat = Entity.get_by_id(16306)
# ref_sys_su = Entity.get_by_id(16308)
#
# # Get OpenAtlas hierarchies
# probe_hierarchy = Entity.get_by_id(16309)
# find_hierarchy = Entity.get_by_id(16310)
# position_hierarchy = Entity.get_by_id(16311)
# orientation_hierarchy = Entity.get_by_id(16312)
# preservation_hierarchy = Entity.get_by_id(16313)
# dislocation_hierarchy = Entity.get_by_id(16314)
# age_hierarchy = Entity.get_by_id(16315)
# extraction_hierarchy = Entity.get_by_id(16316)
# layer_hierarchy = Entity.get_by_id(16317)
# material_hierarchy = Entity.get_by_id(16318)
# designation_hierarchy = Entity.get_by_id(16319)
# dating_hierarchy = Entity.get_by_id(16320)
# cut_hierarchy = Entity.get_by_id(16323)
#
# # Get data out of documents
# features = parse_features()
# merged_units = merge_units(
#     parse_stratigraphic_units(),
#     get_individuals())
# finds = parse_finds()
# # Todo commented  just for performance,
# # extract_images_from_pdfs()
#
# # Build type dictionaries from Feature
# feature_types = build_types(features, import_feature_type, 'type')
# cut_types = build_types(features, cut_hierarchy, 'cut')
#
# # Build type dictionaries from StratigraphicUnit
# su_types = build_types(merged_units, import_su_type, 'type')
# probe_types = build_types(merged_units, probe_hierarchy, 'probe_type')
# find_types = build_types(merged_units, find_hierarchy, 'find_type')
# position_types = build_types(merged_units, position_hierarchy, 'position')
# age_types = build_types(merged_units, age_hierarchy, 'age')
# layer_types = build_types(merged_units, layer_hierarchy, 'layer')
# orientation_types = build_types(
#     merged_units, orientation_hierarchy, 'orientation')
# preservation_types = build_types(
#     merged_units, preservation_hierarchy, 'preservation')
# dislocation_types = build_types(
#     merged_units, dislocation_hierarchy, 'dislocation')
# extraction_types = build_types(
#     merged_units, extraction_hierarchy, 'extraction')
#
# # Build type dictionaries from Find
# material_types = build_types(finds, material_hierarchy, 'material')
# dating_types = build_types(finds, dating_hierarchy, 'dating')
#
# designation_types = build_find_types(finds, 'designation')
#
# added_features: dict[str, Entity] = {}
# for entry in features:
#     feature = Entity.insert('feature', entry.name, entry.description)
#     feature.link('P2', case_study)
#     feature.link('P2', feature_types[entry.type])
#     if entry.cut:
#         feature.link('P2', cut_types[entry.cut])
#     feature.link('P46', place, inverse=True)
#     ref_sys_feat.link(
#         'P67',
#         feature,
#         str(entry.obj_id),
#         type_id=exact_match.id)
#     location = Entity.insert(
#         'object_location',
#         f"Location of {entry.name}")
#     feature.link('P53', location)
#     added_features[entry.id_] = feature
#
# added_stratigraphic: dict[str, Entity] = {}
# for entry in merged_units:
#     su = Entity.insert(
#         'stratigraphic_unit',
#         entry.name,
#         '\n'.join(entry.description))
#     su.link('P2', case_study)
#     su.link('P46', added_features[entry.feature], inverse=True)
#     ref_sys_su.link(
#         'P67',
#         su,
#         str(entry.se_id),
#         type_id=exact_match.id)
#     if entry.individual_id:
#         ref_sys_indi.link(
#             'P67',
#             su,
#             str(entry.individual_id),
#             type_id=exact_match.id)
#     location = Entity.insert(
#         'object_location',
#         f"Location of {entry.name}")
#     su.link('P53', location)
#
#     if entry.type:
#         su.link('P2', su_types[entry.type])
#     if entry.probe_type:
#         su.link('P2', probe_types[entry.probe_type])
#     if entry.find_type:
#         su.link('P2', find_types[entry.find_type])
#     if entry.position:
#         su.link('P2', position_types[entry.position])
#     if entry.orientation:
#         su.link('P2', orientation_types[entry.orientation])
#     if entry.preservation:
#         su.link('P2', preservation_types[entry.preservation])
#     if entry.dislocation:
#         su.link('P2', dislocation_types[entry.dislocation])
#     if entry.age:
#         su.link('P2', age_types[entry.age])
#     if entry.extraction:
#         su.link('P2', extraction_types[entry.extraction])
#     if entry.layer:
#         su.link('P2', layer_types[entry.layer])
#
#     added_stratigraphic[entry.id_] = su
#
# added_finds: dict[str, Entity] = {}
# for entry in finds:
#     if entry.stratigraphic_unit:
#         link_to_entity = added_stratigraphic.get(entry.stratigraphic_unit)
#     elif entry.feature_id:
#         link_to_entity = added_features.get(entry.feature_id)
#     else:
#         link_to_entity = place
#     if not link_to_entity:
#         DEBUG_MSG['no_super_for_finds'].append(entry.f_id)
#         continue
#
#     system_class = 'artifact'
#     if entry.material == 'menschl. Kn.':
#         system_class = 'human_remains'
#     find = Entity.insert(system_class, entry.name, entry.description)
#     find.link('P2', case_study)
#     find.link('P46', link_to_entity, inverse=True)
#
#     ref_sys_finds.link(
#         'P67',
#         find,
#         str(entry.f_id),
#         type_id=exact_match.id)
#     location = Entity.insert(
#         'object_location',
#         f"Location of {entry.name}")
#     find.link('P53', location)
#
#     if entry.material:
#         find.link('P2', material_types[entry.material])
#     if entry.designation:
#         find.link('P2', designation_types[entry.designation])
#     if entry.dating:
#         find.link('P2', dating_types[entry.dating])
#
# print(DEBUG_MSG)
