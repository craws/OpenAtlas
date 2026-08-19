import json
from pathlib import Path
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.api.api_v04.resources.api_entity import ApiEntity
from tests.base import ApiTestCase, get_hierarchy


class ApiV1(ApiTestCase):

    def test_api(self) -> None:
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            rights_holder_ids = [rh.id for rh in g.rights_holder]

        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'
        public_type = get_hierarchy('Public sharing allowed')
        with open(logo_path / 'logo.png', 'rb') as img:
            c.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo',
                    'file': img,
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[1]},
                follow_redirects=True)

        c.get(url_for('logout'))
        with app.test_request_context():
            app.preprocess_request()

            for entity in ApiEntity.get_by_cidoc_classes(['all']):
                match entity.name:
                    case 'Location of Shire':
                        location = entity
                    case 'Shire':
                        place = entity
                    case 'Boundary Mark':
                        boundary_mark = entity
                    case 'Travel to Mordor':
                        event = entity
                    case 'Exchange of the one ring':
                        event2 = entity
                    case 'Economical':
                        relation_sub = entity
                    case 'Austria':
                        unit_node = entity
                    case 'Frodo':
                        actor = entity
                    case 'Sam':
                        actor2 = entity
                    case 'Home of Baggins':
                        feature = entity
                    case 'The One Ring':
                        artifact = entity
                    case 'Sûza':
                        alias = entity
                    case 'Height':
                        height = entity
                    case 'Weight':
                        weight_ = entity
                    case 'Change of Property':
                        change_of_property = entity
                    case 'File not public':
                        file_not_public = entity
                    case 'File without license':
                        file_without_licences = entity
                    case 'File without file':
                        file_without_file = entity
                    case 'OpenAtlas logo':
                        file = entity
                    case 'Public domain':
                        open_license = entity

            file.link('P2', open_license)


        rv = c.get(url_for('api_v1.entity', id=place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        rv_json = rv.get_json()
        assert rv_json['type'] == 'Site'
        assert rv_json['_label'] == 'Shire'

        # Test extensions
        rv_ttl = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='ttl'))
        assert rv_ttl.status_code == 200
        assert 'text/turtle' in rv_ttl.headers.get('Content-Type')

        rv_xml = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='xml'))
        assert rv_xml.status_code == 200
        assert 'application/rdf+xml' in rv_xml.headers.get('Content-Type')

        rv_nt = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='nt'))
        assert rv_nt.status_code == 200
        assert 'application/n-triples' in rv_nt.headers.get('Content-Type')

        # Test 404
        import uuid
        rv_404 = c.get(url_for('api_v1.entity', id=uuid.uuid4()))
        assert rv_404.status_code == 404

    def test_docs(self) -> None:
        c = self.client
        for url in [
            '/api/1/docs/swagger',
            '/api/1/docs/redoc',
            '/api/1/docs/scalar',
            '/api/1/docs/openapi.json',
            '/api/1/docs/',
        ]:
            rv = c.get(url)
            assert rv.status_code == 200
