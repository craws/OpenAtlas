from pathlib import Path

from flask import g, url_for

from openatlas import app
from tests.base import ApiTestCase, get_hierarchy



class ApiV1(ApiTestCase):

    def test_api(self) -> None:
        pass

    def test_lod(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_lod.entity', uuid=e.place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        rv_json = rv.get_json()
        assert rv_json[
                   '@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'Site'
        assert rv_json['_label'] == 'Shire'


    def test_system(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_root.index'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert rv['name'] == "OpenAtlas API V1"
        assert 'version' in rv
        assert 'openapiSchema' in rv
        assert 'documentation' in rv
        assert 'manual' in rv

        rv = c.get(url_for('api_v1_system.system_info'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert 'apiVersions' in rv
        assert isinstance(rv['apiVersions'], list)
        assert 'defaultLanguage' in rv
        assert 'iiif' in rv
        assert isinstance(rv['iiif'], dict)
        assert 'imageProcessing' in rv
        assert isinstance(rv['imageProcessing'], dict)
        assert 'logoFileId' in rv
        assert 'mapConfig' in rv
        assert isinstance(rv['mapConfig'], dict)
        assert 'siteName' in rv
        assert 'version' in rv

        rv = c.get(url_for('api_v1_system.entity_count'))
        assert rv.status_code == 200
        assert 'counts' in rv.get_json()
        rv = c.get(
            url_for(
                'api_v1_system.entity_count',
                case_study_id=e.case_study.id))
        assert 'counts' in rv.get_json()

        rv = c.get(url_for('api_v1_system.system_classes'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert 'locale' in rv
        assert 'results' in rv
        assert isinstance(rv['results'], list)
        rv = c.get(url_for('api_v1_system.system_classes', locale='de'))
        assert 'de' in rv.get_json()['locale']

        rv = c.get(url_for('api_v1_system.system_crm_properties'))
        assert rv.status_code == 200
        assert 'properties' in rv.get_json()

    def test_vocabulary(self) -> None:
        c = self.client
        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_list'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'types' in rv_json
        assert isinstance(rv_json['types'], dict)

        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_tree'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'standard' in rv_json
        assert 'custom' in rv_json
        assert 'place' in rv_json
        assert 'value' in rv_json
        assert 'system' in rv_json
        assert 'tools' in rv_json

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_tree_by_class',
                openatlas_class='place'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'place' in rv_json

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_standard_by_class',
                openatlas_class='place'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'results' in rv_json
        assert isinstance(rv_json['results'], list)

    def test_metadata(self) -> None:
        c = self.client
        e = self.get_api_entities()

        # Case studies
        rv = c.get(url_for('api_v1_metadata.get_case_studies'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'caseStudies' in rv_json
        assert isinstance(rv_json['caseStudies'], list)

        rv = c.get(
            url_for(
                'api_v1_metadata.get_case_study_by_id',
                id=e.case_study.id))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'id' in rv_json
        assert 'name' in rv_json

        # Agents
        rv = c.get(url_for('api_v1_metadata.get_agents'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'agents' in rv_json
        assert isinstance(rv_json['agents'], list)

        # Agent by ID (dummy 1 for now)
        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=1))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'name' in rv_json
        assert 'type' in rv_json


    def test_files(self) -> None:
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

        e = self.get_api_entities()
        with app.test_request_context():
            app.preprocess_request()
            e.file.link('P2', e.open_license)

        rv = c.get(url_for('api_v1_files.display_file', id=e.file.id))
        assert rv.status_code in (200, 404)

        rv = c.get(
            url_for(
                'api_v1_files.get_iiif_manifest',
                id=e.file.id,
                version='2'))
        assert rv.status_code == 200
        assert rv.get_json()['@type'] == 'sc:Manifest'

        rv = c.get(
            url_for(
                'api_v1_files.get_iiif_manifest',
                id=e.file.id,
                version='3'))
        assert rv.status_code == 200
        assert rv.get_json()['type'] == 'Manifest'

        rv = c.get(
            url_for('api_v1_files.get_iiif_canvas', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_files.get_iiif_image', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for(
                'api_v1_files.get_iiif_annotation_list',
                id=e.file.id,
                version='2'))
        assert rv.status_code == 200

        rv = c.get(url_for('api_v1_files.get_licensed_files'))
        assert rv.status_code == 200
        assert 'files' in rv.get_json()



    def test_docs(self) -> None:
        c = self.client
        for url in [
                '/api/1/docs/swagger',
                '/api/1/docs/redoc',
                '/api/1/docs/scalar',
                '/api/1/docs/openapi.json',
                '/api/1/docs/']:
            rv = c.get(url)
            assert rv.status_code == 200
