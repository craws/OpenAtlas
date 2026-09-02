from pathlib import Path

from flask import g, url_for

from openatlas import app
from openatlas.api.api_v04.resources.api_entity import ApiEntity
from tests.base import ApiTestCase, get_hierarchy

from openatlas.api.api_v1.util.date_util import pad_historical_date

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
        assert rv_json['@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'Site'
        assert rv_json['_label'] == 'Shire'

        # Test extensions
        rv = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='ttl'))
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='xml'))
        assert rv.status_code == 200
        assert 'application/rdf+xml' in rv.headers.get('Content-Type')

        rv = c.get(url_for('api_v1.entity_ext', id=place.uuid, ext='nt'))
        assert rv.status_code == 200
        assert 'application/n-triples' in rv.headers.get('Content-Type')

        # Test multiple entities collection (Hydra pagination & @graph)
        rv = c.get(url_for('api_v1.entities', entity_class='place'))
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
        rv = c.get(url_for('api_v1.entities', entity_class='place', limit=1, page=1, sort='asc'))
        assert rv.status_code == 200
        p1_json = rv.get_json()
        assert len(p1_json['@graph']) == 1
        assert p1_json['hydra:totalItems'] >= 2
        assert 'hydra:previous' not in p1_json
        assert 'hydra:next' in p1_json
        assert 'page=2' in p1_json['hydra:next']
        assert 'sort=asc' in p1_json['hydra:next']
        first_asc_label = p1_json['@graph'][0]['_label']

        rv = c.get(url_for('api_v1.entities', entity_class='place', limit=1, page=2, sort='asc'))
        assert rv.status_code == 200
        p2_json = rv.get_json()
        assert len(p2_json['@graph']) == 1
        assert 'hydra:previous' in p2_json
        assert 'page=1' in p2_json['hydra:previous']
        second_asc_label = p2_json['@graph'][0]['_label']
        assert first_asc_label <= second_asc_label

        rv = c.get(url_for('api_v1.entities', entity_class='place', limit=1, page=1, sort='desc'))
        assert rv.status_code == 200
        desc_json = rv.get_json()
        assert len(desc_json['@graph']) == 1
        first_desc_label = desc_json['@graph'][0]['_label']
        assert first_desc_label >= first_asc_label

        # Test sorting by startDate and endDate
        rv = c.get(url_for('api_v1.entities', entity_class='place', sortBy='startDate', sort='asc'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='place', sortBy='endDate', sort='desc'))
        assert rv.status_code == 200

        # Test search filter
        rv = c.get(url_for('api_v1.entities', entity_class='place', search='Shire'))
        assert rv.status_code == 200
        search_json = rv.get_json()
        assert len(search_json['@graph']) >= 1
        assert any('Shire' in item['_label'] for item in search_json['@graph'])

        # Test date filters (startDate, endDate with historical and incomplete formats)
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='0100-01-01', endDate='2000-01-01'))
        assert rv.status_code == 200

        # Test historical dates (year-only, year-month, negative BCE years)
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='400', endDate='400'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='400-05', endDate='400-05'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='400-02', endDate='400-02'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='-400', endDate='-400'))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='-400-05', endDate='-400-05'))
        assert rv.status_code == 200

        # Test invalid date formats return 422
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='invalid'))
        assert rv.status_code == 422
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='400-13'))
        assert rv.status_code == 422
        rv = c.get(url_for('api_v1.entities', entity_class='place', startDate='400-02-31'))
        assert rv.status_code == 422

        # Direct unit tests for pad_historical_date
        assert pad_historical_date(None) is None
        assert pad_historical_date('') is None
        assert pad_historical_date('400', is_end_date=False) == '0400-01-01'
        assert pad_historical_date('400', is_end_date=True) == '0400-12-31'
        assert pad_historical_date('400-05', is_end_date=False) == '0400-05-01'
        assert pad_historical_date('400-05', is_end_date=True) == '0400-05-31'
        assert pad_historical_date('400-02', is_end_date=True) == '0400-02-29'
        assert pad_historical_date('500-02', is_end_date=True) == '0500-02-28'
        assert pad_historical_date('-400', is_end_date=False) == '-0400-01-01'
        assert pad_historical_date('-400', is_end_date=True) == '-0400-12-31'
        assert pad_historical_date('-400-05', is_end_date=False) == '-0400-05-01'
        assert pad_historical_date('-400-05', is_end_date=True) == '-0400-05-31'
        assert pad_historical_date('1900-01-01', is_end_date=False) == '1900-01-01'
        assert pad_historical_date('1900-01-01', is_end_date=True) == '1900-01-01'

        # Test type filter with ID and UUID
        rv = c.get(url_for('api_v1.entities', entity_class='file', typeId=open_license.id))
        assert rv.status_code == 200
        total_items_id = rv.get_json()['hydra:totalItems']
        rv = c.get(url_for('api_v1.entities', entity_class='file', typeId=open_license.uuid))
        assert rv.status_code == 200
        assert total_items_id == rv.get_json()['hydra:totalItems']

        # Test case study filter with ID and UUID
        rv = c.get(url_for('api_v1.entities', entity_class='file', caseStudy=open_license.id))
        assert rv.status_code == 200
        rv = c.get(url_for('api_v1.entities', entity_class='file', caseStudy=open_license.uuid))
        assert rv.status_code == 200

        # Test nonexistent type or UUID returns empty graph
        rv = c.get(url_for('api_v1.entities', entity_class='place', typeId='99999999-9999-9999-9999-999999999999'))
        assert rv.status_code == 200
        assert rv.get_json()['hydra:totalItems'] == 0

        # Test invalid entity class returns 422 or 404
        rv = c.get(url_for('api_v1.entities', entity_class='nonexistent_class'))
        assert rv.status_code in (404, 422)

        # Test multiple entities with Accept header content negotiation
        rv = c.get(
            url_for('api_v1.entities', entity_class='place'),
            headers={'Accept': 'text/turtle'})
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for('api_v1.entities', entity_class='place'),
            headers={'Accept': 'application/rdf+xml'})
        assert rv.status_code == 200
        assert 'application/rdf+xml' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for('api_v1.entities', entity_class='place'),
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
        rv = c.get(url_for('api_v1_loud.loud_entity', id=place.uuid))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        loud_json = rv.get_json()
        assert loud_json['type'] == 'Site'
        assert loud_json['_label'] == 'Shire'

        rv = c.get(url_for('api_v1_loud.loud_entity_ext', id=place.uuid, ext='ttl'))
        assert rv.status_code == 200
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(url_for('api_v1_loud.loud_entities', entity_class='place'))
        assert rv.status_code == 200
        loud_entities_json = rv.get_json()
        assert isinstance(loud_entities_json['@graph'], list)

        # Test 404
        import uuid
        rv = c.get(url_for('api_v1.entity', id=uuid.uuid4()))
        assert rv.status_code == 404
        rv = c.get(url_for('api_v1_loud.loud_entity', id=uuid.uuid4()))
        assert rv.status_code == 404

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
