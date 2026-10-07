import json
from openatlas import app
from tests.base import TestBaseCase


class OpenAPI(TestBaseCase):
    def test_openapi_file_generation(self):
        c = self.client
        instance_file = app.config['OPENAPI_INSTANCE_FILE']

        if instance_file.exists():
            instance_file.unlink()
        rv = c.get('/openapi.json')
        assert rv.status_code == 200

        with instance_file.open(mode='r+') as f:
            data = json.load(f)
            data['servers'][0]['description'] = 'Wrong description'
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        rv = c.get('/openapi.json')
        assert rv.status_code == 200
        with instance_file.open(mode='r') as f:
            data = json.load(f)
            assert data['servers'][0]['description'] != 'Wrong description'

        with instance_file.open(mode='r+') as f:
            data = json.load(f)
            data['info']['version'] = '9.9.9'
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        rv = c.get('/openapi.json')
        assert rv.status_code == 200
        with instance_file.open(mode='r') as f:
            data = json.load(f)
            assert data['info']['version'] != '9.9.9'

        rv = c.get('/swagger')
        assert rv.status_code == 200
