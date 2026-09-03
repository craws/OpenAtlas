from pathlib import Path

from flask import g, url_for

from openatlas import app
from tests.base import ApiTestCase, get_hierarchy

from openatlas.api.api_v1.util.date_util import handle_date


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

        e = self.get_api_entities()

        with app.test_request_context():
            app.preprocess_request()
            e.file.link('P2', e.open_license)

        rv = c.get(url_for('api_v1_lod.entity', id=e.place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        rv_json = rv.get_json()
        assert rv_json[
                   '@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'Site'
        assert rv_json['_label'] == 'Shire'

        # Test extensions
        rv = c.get(
            url_for('api_v1_lod.entity_ext', id=e.place.uuid, ext='ttl'))
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for('api_v1_lod.entity_ext', id=e.place.uuid, ext='xml'))
        assert rv.status_code == 200
        assert 'application/rdf+xml' in rv.headers.get('Content-Type')

        rv = c.get(url_for('api_v1_lod.entity_ext', id=e.place.uuid, ext='nt'))
        assert rv.status_code == 200
        assert 'application/n-triples' in rv.headers.get('Content-Type')

        # Test multiple entities collection (Hydra pagination & @graph)
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place'))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        entities_json = rv.get_json()
        assert entities_json['@context'] == [
            'https://linked.art/ns/v1/linked-art.json',
            {'hydra': 'http://www.w3.org/ns/hydra/core#'}]
        assert entities_json['type'] == 'hydra:PartialCollectionView'
        assert isinstance(entities_json['hydra:totalItems'], int)
        assert 'hydra:first' in entities_json
        assert 'hydra:last' in entities_json
        assert isinstance(entities_json['@graph'], list)
        assert len(entities_json['@graph']) > 0
        for item in entities_json['@graph']:
            assert '@context' not in item
            assert 'id' in item
            assert 'type' in item
            assert '_label' in item

        # Test pagination with limit and sorting (asc & desc by name)
        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place', limit=1,
                    page=1, sort='asc'))
        assert rv.status_code == 200
        p1_json = rv.get_json()
        assert len(p1_json['@graph']) == 1
        assert p1_json['hydra:totalItems'] >= 2
        assert 'hydra:previous' not in p1_json
        assert 'hydra:next' in p1_json
        assert 'page=2' in p1_json['hydra:next']
        assert 'sort=asc' in p1_json['hydra:next']
        first_asc_label = p1_json['@graph'][0]['_label']

        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place', limit=1,
                    page=2, sort='asc'))
        assert rv.status_code == 200
        p2_json = rv.get_json()
        assert len(p2_json['@graph']) == 1
        assert 'hydra:previous' in p2_json
        assert 'page=1' in p2_json['hydra:previous']
        second_asc_label = p2_json['@graph'][0]['_label']
        assert first_asc_label <= second_asc_label

        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place', limit=1,
                    page=1, sort='desc'))
        assert rv.status_code == 200
        desc_json = rv.get_json()
        assert len(desc_json['@graph']) == 1
        first_desc_label = desc_json['@graph'][0]['_label']
        assert first_desc_label >= first_asc_label

        # Test sorting by startDate and endDate
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           sortBy='startDate', sort='asc'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           sortBy='endDate', sort='desc'))
        assert rv.status_code == 200

        # Test search filter
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           search='Shire'))
        assert rv.status_code == 200
        search_json = rv.get_json()
        assert len(search_json['@graph']) >= 1
        assert any('Shire' in item['_label'] for item in search_json['@graph'])

        # Test date filters (startDate, endDate with historical and
        # incomplete formats)
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='0100-01-01', endDate='2000-01-01'))
        assert rv.status_code == 200

        # Test historical dates (year-only, year-month, negative BCE years)
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='400', endDate='400'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='400-05', endDate='400-05'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='400-02', endDate='400-02'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='-400', endDate='-400'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='-400-05', endDate='-400-05'))
        assert rv.status_code == 200

        # Test invalid date formats return 422
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='invalid'))
        assert rv.status_code == 422
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='400-13'))
        assert rv.status_code == 422
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           startDate='400-02-31'))
        assert rv.status_code == 422

        # Direct unit tests for pad_historical_date
        assert handle_date(None) is None
        assert handle_date('') is None
        assert handle_date('400', is_end_date=False) == '0400-01-01'
        assert handle_date('400', is_end_date=True) == '0400-12-31'
        assert handle_date('400-05', is_end_date=False) == '0400-05-01'
        assert handle_date('400-05', is_end_date=True) == '0400-05-31'
        assert handle_date('400-02', is_end_date=True) == '0400-02-29'
        assert handle_date('500-02', is_end_date=True) == '0500-02-28'
        assert handle_date('-400', is_end_date=False) == '-0400-01-01'
        assert handle_date('-400', is_end_date=True) == '-0400-12-31'
        assert handle_date('-400-05', is_end_date=False) == '-0400-05-01'
        assert handle_date('-400-05', is_end_date=True) == '-0400-05-31'
        assert handle_date('1900-01-01', is_end_date=False) == '1900-01-01'
        assert handle_date('1900-01-01', is_end_date=True) == '1900-01-01'

        # Test type filter with ID and UUID
        rv = c.get(url_for('api_v1_lod.entities', entity_class='file',
                           typeId=e.open_license.id))
        assert rv.status_code == 200
        total_items_id = rv.get_json()['hydra:totalItems']
        rv = c.get(url_for('api_v1_lod.entities', entity_class='file',
                           typeId=e.open_license.uuid))
        assert rv.status_code == 200
        assert total_items_id == rv.get_json()['hydra:totalItems']

        # Test case study filter with ID and UUID
        rv = c.get(url_for('api_v1_lod.entities', entity_class='file',
                           caseStudy=e.open_license.id))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1_lod.entities', entity_class='file',
                           caseStudy=e.open_license.uuid))
        assert rv.status_code == 200

        # Test nonexistent type or UUID returns empty graph
        rv = c.get(url_for('api_v1_lod.entities', entity_class='place',
                           typeId='99999999-9999-9999-9999-999999999999'))
        assert rv.status_code == 200
        assert rv.get_json()['hydra:totalItems'] == 0

        # Test invalid entity class returns 422 or 404
        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='nonexistent_class'))
        assert rv.status_code in (404, 422)

        # Test multiple entities with Accept header content negotiation
        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place'),
            headers={'Accept': 'text/turtle'})
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place'),
            headers={'Accept': 'application/rdf+xml'})
        assert rv.status_code == 200
        assert 'application/rdf+xml' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for('api_v1_lod.entities', entity_class='place'),
            headers={'Accept': 'application/n-triples'})
        assert rv.status_code == 200
        assert 'application/n-triples' in rv.headers.get('Content-Type')

        # Test empty format_lod_entities
        from openatlas.api.api_v1.formatters.lod import format_lod_entities
        from openatlas.api.api_v1.formatters.loud import format_loud_entities
        empty_res = format_lod_entities([])
        assert empty_res == {
            '@context': 'https://linked.art/ns/v1/linked-art.json',
            '@graph': []}
        empty_loud_res = format_loud_entities([])
        assert empty_loud_res == {
            '@context': 'https://linked.art/ns/v1/linked-art.json',
            '@graph': []}

        # Test LOUD routes
        rv = c.get(url_for('api_v1_loud.loud_entity', id=e.place.uuid))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        loud_json = rv.get_json()
        assert loud_json['type'] == 'Site'
        assert loud_json['_label'] == 'Shire'

        rv = c.get(
            url_for('api_v1_loud.loud_entity_ext', id=e.place.uuid, ext='ttl'))
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(url_for('api_v1_loud.loud_entities', entity_class='place'))
        assert rv.status_code == 200
        loud_entities_json = rv.get_json()
        assert isinstance(loud_entities_json['@graph'], list)

        # Test 404
        import uuid
        rv = c.get(url_for('api_v1_lod.entity', id=uuid.uuid4()))
        assert rv.status_code == 404
        rv = c.get(url_for('api_v1_loud.loud_entity', id=uuid.uuid4()))
        assert rv.status_code == 404

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
