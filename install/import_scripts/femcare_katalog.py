import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from docx import Document

FILE_PATH = Path('files/femcare')
FUNDFOTOS_KATALOG = FILE_PATH / 'Katalog_fundfotos.docx'
FUNDFOTOS_MEDAILLIEN = FILE_PATH / 'Fundfotos_Medaillien'

# pylint: skip-file


@dataclass
class FundEntity:
    id: str
    type: str = ''
    date: str = ''
    location: str = ''
    description: str = ''
    dimensions: str = ''
    identifications: str = ''

    _current_index: int = field(default=0, init=False, repr=False)

    def add_entry(self, text: str) -> None:
        field_names = [
            'type',
            'date',
            'location',
            'description',
            'dimensions',
            'identifications']
        if self._current_index < len(field_names):
            target_field = field_names[self._current_index]
            setattr(self, target_field, text)
            self._current_index += 1


def parse_katalog(file_path: Path) -> dict[str, FundEntity]:
    doc = Document(str(file_path))
    entities: dict[str, FundEntity] = {}
    current: Optional[FundEntity] = None

    for table in doc.tables:
        for row in table.rows:
            if not row.cells:
                continue
            first_text = row.cells[0].text.strip()
            row_id = None
            if (first_text
                    and first_text[0].isdigit() and first_text.endswith('.')):
                row_id = first_text.rstrip('.')
            is_new_entity = False
            if row_id:
                if current is None or current.id != row_id:
                    is_new_entity = True
            else:
                continue
            if is_new_entity:
                current = FundEntity(id=row_id)
                entities[row_id] = current
            if not current:
                continue
            row_seen_tc: set[int] = set()
            for cell in row.cells:
                tc_id = id(cell._tc)
                if tc_id in row_seen_tc:
                    continue
                row_seen_tc.add(tc_id)
                text = cell.text.strip()
                if text == f'{current.id}.':
                    continue
                current.add_entry(text)
    return entities


@dataclass
class KatalogEntity:
    id: str
    type: str = 'Medaille'
    start_date: str = ''
    end_date: str = ''
    location: str = ''
    description: str = ''
    weight: str = ''
    diameter: str = ''
    coin: str = ''
    length: str = ''
    height: str = ''
    identifications: str = ''
    fndnr: str = ''
    se: str = ''
    image_id: str = ''


def parse_find_entry(entry: str) -> dict[str, str]:
    fndnr_match = re.search(r'Fund-Nr\.\s*([\d/]+)', entry)
    se_match = re.search(r'SE\s*(\d+)', entry)
    id_match = re.search(r'ID\s*(\d+)', entry)

    return {
        'fndnr': fndnr_match.group(1) if fndnr_match else '',
        'se': se_match.group(1) if se_match else '',
        'id': id_match.group(1) if id_match else ''}


def get_fundkatalog_entries(
        fund_entities: dict[str, FundEntity]) -> list[KatalogEntity]:
    result_ = []
    for entry in fund_entities.values():
        start_date = ''
        end_date = ''
        weight = ''
        length = ''
        height = ''
        diameter = ''
        coin_ = ''
        description_ = ''
        if entry.date:
            date = entry.date.split('\u2013')  # en dash, not hyphen!
            start_date = date[0]
            if len(date) > 1:
                end_date = date[1]
        if entry.dimensions:
            dim_tmp = entry.dimensions.split('mm')
            weight_dimensions = dim_tmp[0].split('g,')
            weight = weight_dimensions[0].strip()
            if len(weight_dimensions) == 2:
                tmp = weight_dimensions[1]
                coin_dimensions = tmp.split('h,')
                if len(coin_dimensions) == 2:
                    coin_ = coin_dimensions[0].strip()
                    tmp = coin_dimensions[1].strip()
                dimensions = tmp.split('x')
                if len(dimensions) == 2:
                    length = dimensions[0].strip()
                    height = dimensions[1].strip()
                else:
                    diameter = dimensions[0].strip()
            if len(dim_tmp) == 2:
                description_ = f'{dim_tmp[1].strip()}\n'

        # todo: check out fundnummer with subcategories e.g. 1489/4. Add
        #  for each a new artifact?

        idendification = parse_find_entry(entry.identifications)
        result_.append(KatalogEntity(
            id=entry.id,
            type=entry.type or 'Medaille',
            start_date=start_date,
            end_date=end_date,
            location=entry.location,
            description=f'{description_}{entry.description}',
            weight=weight,
            coin=coin_,
            length=length,
            height=height,
            diameter=diameter,
            fndnr=idendification['fndnr'],
            se=idendification['se'],
            image_id=idendification['id']))
    return result_


if __name__ == '__main__':
    if FUNDFOTOS_KATALOG.exists():
        result: dict[str, FundEntity] = parse_katalog(FUNDFOTOS_KATALOG)
        fundkatalog_entries = get_fundkatalog_entries(result)
        for e in fundkatalog_entries:
            # print(e)
            pass
        # todo: next steps: move to main function, add to finds, update finds
        #   with data and images
        fundfotos_medaillien = {}
        for file_ in FUNDFOTOS_MEDAILLIEN.iterdir():
            fundfotos_medaillien[file_.stem] = file_
    else:
        print(f'Datei nicht gefunden: {FUNDFOTOS_KATALOG}')
