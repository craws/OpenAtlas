# Used to join data from OpenAtlas projects to the demo version

from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from flask import g

from openatlas import app, before_request
from openatlas.api.import_scripts.util import get_exact_match
from openatlas.models.entity import Entity
from openatlas.models.type import Type

file_path = Path('files/sisters.csv')


with app.test_request_context():
    app.preprocess_request()
    case_study = Entity.get_by_id(358)

    # Remove former data
    for item in case_study.get_linked_entities('P2', True):
        item.delete()
