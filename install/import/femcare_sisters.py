from pathlib import Path

import pandas as pd

from openatlas.models.entity import Entity

file_path = Path('files/sisters.csv')

from openatlas import app


def parse_csv():
    df = pd.read_csv(file_path, delimiter='\t', encoding='utf-8', dtype=str)
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    for _, row in df.iterrows():
        Entity.insert('person', row['Name'])
        break


with app.test_request_context():
    app.preprocess_request()
    parse_csv()

    # df['Beginn'] = pd.to_datetime(
    #     df['Beginn'],
    #     format='%d.%m.%Y',
    #     errors='coerce')
