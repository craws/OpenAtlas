import itertools
import time
from pathlib import Path
from typing import Any

import pandas as pd
from flask import g

from openatlas import app
from openatlas.models.entity import Entity

FILE_PATH = Path('files/relic_admin.csv')
SPINNER = itertools.cycle(["|", "/", "-", "\\"])
COUNT = 0
# pylint: skip-file


class Entry:
    def __init__(self, attributes_: dict[str, Any]) -> None:
        self.region = attributes_['region']
        self.district = attributes_['district']
        self.cadastre = attributes_['cadastre']

def parse_csv() -> list[Entry]:
    data = pd.read_csv(FILE_PATH, delimiter='\t', encoding='utf-8', dtype=str)
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    result = []
    for _, row in data.iterrows():
        result.append(Entry({
            'region': row['region'],
            'district': row['district'],
            'cadastre': row['cadastre']}))
    return result

#################################
# Code for Administrative units #
#################################

with app.test_request_context():
    app.preprocess_request()
    start_time = time.time()
    admin_cz_type = Entity.get_by_id(117158)
    entries = parse_csv()

    regions = {}
    districts = {}
    cadastres = {}

    for region_id in g.types[117158].subs:
        region = Entity.get_by_id(region_id)
        regions[region.name.lower()] = region.id
        for district_id in g.types[region.id].subs:
            district = Entity.get_by_id(district_id)
            districts[district.name.lower()] = district.id
            for cadastre_id in g.types[district.id].subs:
                cadastre = Entity.get_by_id(cadastre_id)
                cadastres[cadastre.name.lower()] = cadastre.id

    for entry in entries:
        if entry.region.lower() not in regions:
            region = Entity.insert('administrative_unit', entry.region)
            region.link('P89', admin_cz_type)
            regions[region.name.lower()] = region.id
        if entry.district.lower() not in districts:
            district = Entity.insert('administrative_unit', entry.district)
            district.link('P89', Entity.get_by_id(regions[entry.region.lower()]))
            districts[district.name.lower()] = district.id
        if entry.cadastre.lower() not in cadastres:
            cadastre = Entity.insert('administrative_unit', entry.cadastre)
            cadastre.link('P89', Entity.get_by_id(districts[entry.district.lower()]))
            cadastres[cadastre.name.lower()] = cadastre.id

    print(f'\n{len(regions)} regions where imported.')
    print(f'\n{len(districts)} districts where imported.')
    print(f'\n{len(cadastres)} cadastres where imported.')
    #print(f'{len(not_imported)} entries couldn\'t be imported.')
    print(f"Execution time: {time.time() - start_time:.6f} seconds")


#######################
# Code for RELIC Type #
#######################

#with app.test_request_context():
#    app.preprocess_request()
#    start_time = time.time()
#    relic_type = Entity.get_by_id(255820)
#    relic_admin_type = Entity.insert('type', 'Administrative units')
#    relic_admin_type.link('P127', relic_type)
#    entries = parse_csv()
#    regions = {}
#    districts = {}
#    cadastres = {}
#    for entry in entries:
#        if entry.region.lower() not in regions:
#            region = Entity.insert('type', entry.region)
#            region.link('P127', relic_admin_type)
#            regions[region.name.lower()] = region.id
#    for entry in entries:
#        if entry.district.lower() not in districts:
#            district = Entity.insert('type', entry.district)
#            district.link('P127', Entity.get_by_id(regions[entry.region.lower()]))
#            districts[district.name.lower()] = district.id
#    for entry in entries:
#        if entry.cadastre.lower() not in cadastres:
#            cadastre = Entity.insert('type', entry.cadastre)
#            cadastre.link('P127', Entity.get_by_id(districts[entry.district.lower()]))
#            cadastres[cadastre.name.lower()] = cadastre.id
#    print(f'\n{len(regions)} regions where imported.')
#    print(f'\n{len(districts)} districts where imported.')
#    print(f'\n{len(cadastres)} cadastres where imported.')
#    #print(f'{len(not_imported)} entries couldn\'t be imported.')
#    print(f"Execution time: {time.time() - start_time:.6f} seconds")
