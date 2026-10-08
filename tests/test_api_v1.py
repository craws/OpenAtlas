from pathlib import Path

from flask import g, url_for
from rdflib import Dataset, RDF, URIRef

from openatlas import app
from openatlas.api.api_v1.formatters.lod import format_lod_entities
from openatlas.api.api_v1.formatters.loud import format_loud_entities
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity
from openatlas.models.settings import set_logo
from tests.base import ApiTestCase, get_hierarchy, insert


class ApiV1(ApiTestCase):

    def test_api(self) -> None:
        pass

    def test_lod(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        rv_json = rv.get_json()
        assert rv_json[
                   '@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'Physical Thing'
        assert rv_json['_label'] == 'Shire'

        rv = c.get(
            url_for('api_v1_lod.get_entity_ext', uuid=e.place.uuid, ext='ttl'))
        assert 'text/turtle' in rv.headers.get('Content-Type')

        for params in [
            {'caseStudy': e.case_study.id, 'limit': 1, 'page': 2},
            {'caseStudy': e.place.uuid, 'limit': 5, 'offset': 2},
            {'startDate': '1988-02-03', 'endDate': '1988-04-03'},
            {'startDate': '-400',
             'endDate': '2000-05',
             'caseStudy': e.case_study.uuid,
             'sortBy': 'name',
             'sort': 'desc'},
            {'startDate': '2000'},
            {'endDate': '2000'},
            {'startDate': '-500'},
            {'endDate': '-500'},
            {'startDate': '2000-02'},
            {'startDate': '-500-02'},
            {'endDate': '2000-02'},
            {'endDate': '1900-02'},
            {'endDate': '2004-02'},
            {'endDate': '2001-02', 'search': e.place.name},
            {'endDate': '2020-04'},
            {'endDate': '2020-01'},
            {'startDate': '2000-02-29'},
            {'startDate': '-400-02-28', 'typeId': e.boundary_mark.id},
            {'endDate': '2004-02-29'},
            {'endDate': '-500-03-15'},
            {'startDate': '   '}]:
            rv = c.get(url_for(
                'api_v1_lod.get_entities', entity_class='acquisition', **params))
            assert rv.status_code == 200

        for sort_field in [
                'name', 'startDate', 'endDate', 'start_date', 'end_date']:
            for sort_order in ['asc', 'desc']:
                rv = c.get(url_for(
                    'api_v1_lod.get_entities',
                    entity_class='acquisition',
                    sortBy=sort_field,
                    sort=sort_order))
                assert rv.status_code == 200

        rv = c.get(url_for(
            'api_v1_lod.get_entities',
            entity_class='acquisition',
            sortBy='invalid_field'))
        assert rv.status_code == 422

        for params in [
            {'startDate': '0'},
            {'startDate': '-0'},
            {'startDate': '0000-03-15'},
            {'endDate': '0'},
            {'endDate': '0-05'}]:
            rv = c.get(url_for(
                'api_v1_lod.get_entities', entity_class='acquisition', **params))
            assert rv.status_code == 422
            assert b'There is no year 0' in rv.data

        for params in [
            {'startDate': '2000-00'},
            {'startDate': '2000-13'},
            {'startDate': '2000-00-15'},
            {'startDate': '2000-13-15'},
            {'startDate': '2001-02-29'},
            {'startDate': '1900-02-29'},
            {'startDate': '2000-02-30'},
            {'startDate': '2020-04-31'},
            {'startDate': '2020-01-00'},
            {'startDate': '2020-01-32'},
            {'startDate': 'invalid'},
            {'startDate': '-abc'},
            {'startDate': '2020-01-01-01'},
            {'endDate': '2020-00'},
            {'endDate': '2020-13'},
            {'endDate': '2020-00-15'},
            {'endDate': '2020-13-15'},
            {'endDate': '2001-02-29'},
            {'endDate': '1900-02-29'},
            {'endDate': '2000-02-30'},
            {'endDate': '2020-04-31'},
            {'endDate': '2020-01-00'},
            {'endDate': '2020-01-32'},
            {'endDate': 'invalid'},
            {'endDate': '-abc'},
            {'endDate': '2020-01-01-01'}]:
            rv = c.get(url_for(
                'api_v1_lod.get_entities', entity_class='acquisition', **params))
            assert rv.status_code == 422
        rv = c.get(
            url_for(
                'api_v1_lod.get_entities',
                entity_class='type',
                limit=1,
                page=2))
        assert rv.status_code == 200
        assert 'hydra:previous' in rv.get_json()

        assert format_lod_entities([]) == {
            '@context': 'https://linked.art/ns/v1/linked-art.json',
            '@graph': []}

        rv = c.get(url_for(
            'api_v1_lod.get_entities', entity_class='acquisition',
            startDate='999999999'))
        assert rv.status_code == 422

        rv = c.get(
            url_for(
                'api_v1_lod.get_entity',
                uuid='7404a969-97ba-4861-a555-3a97be2be967'))
        assert rv.status_code == 404

    def test_loud(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_loud.get_entity', uuid=e.place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        rv_json = rv.get_json()
        assert rv_json[
                   '@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'HumanMadeObject'
        assert rv_json['current_location']['type'] == 'Place'
        assert rv_json['_label'] == 'Shire'

        rv = c.get(
            url_for(
                'api_v1_loud.get_entity_ext',
                uuid=e.place.uuid,
                ext='ttl'))
        assert 'text/turtle' in rv.headers.get('Content-Type')

        rv = c.get(
            url_for(
                'api_v1_loud.get_entity',
                uuid='7404a969-97ba-4861-a555-3a97be2be967'))
        assert rv.status_code == 404

        for class_ in ['place', 'person', 'artifact', 'file', 'type']:
            rv = c.get(
                url_for('api_v1_loud.get_entities', entity_class=class_))
            assert rv.status_code == 200
            rv_json = rv.get_json()
            assert rv_json['type'] == 'hydra:PartialCollectionView'
            assert rv_json['@graph']

        rv = c.get(
            url_for(
                'api_v1_loud.get_entities',
                entity_class='type',
                limit=1,
                page=2))
        assert rv.status_code == 200
        assert 'hydra:previous' in rv.get_json()

        assert format_loud_entities([]) == {
            '@context': 'https://linked.art/ns/v1/linked-art.json',
            '@graph': []}

        rv = c.get(url_for('api_v1_loud.get_entity', uuid=e.move.uuid))
        part = rv.get_json()['part'][0]
        assert part['type'] == 'Move'
        assert part['moved'][0]['id'].endswith(e.artifact.uuid)
        assert part['moved_to']['type'] == 'Place'
        assert part['moved_from']['type'] == 'Place'

        rv = c.get(url_for('api_v1_loud.get_entity', uuid=e.artifact.uuid))
        rv_json = rv.get_json()
        assert rv_json['produced_by']['type'] == 'Production'
        assert rv_json['destroyed_by']['type'] == 'Destruction'
        assert 'timespan' in rv_json['destroyed_by']

        for entity in (e.place, e.feature):
            rv = c.get(url_for('api_v1_loud.get_entity', uuid=entity.uuid))
            rv_json = rv.get_json()
            assert rv_json['type'] == 'HumanMadeObject'

    def test_system(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_root.api_v1_index'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert rv['name'] == "OpenAtlas API"
        assert 'version' in rv
        assert 'openapiSchema' in rv
        assert 'documentation' in rv
        assert 'manual' in rv

        rv = c.get(url_for('api_v1_system.get_system_info'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert 'apiVersions' in rv
        assert isinstance(rv['apiVersions'], dict)
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

        rv = c.get(
            url_for(
                'api_v1_system.get_entity_count',
                case_study_id=e.case_study.id))
        assert 'counts' in rv.get_json()

        rv = c.get(url_for('api_v1_system.get_system_classes'))
        assert rv.status_code == 200
        rv = rv.get_json()
        assert 'locale' in rv
        assert 'results' in rv
        assert isinstance(rv['results'], list)
        rv = c.get(url_for('api_v1_system.get_system_classes', locale='de'))
        assert 'de' in rv.get_json()['locale']

        rv = c.get(url_for('api_v1_system.get_entity_count'))
        assert 'counts' in rv.get_json()

        rv = c.get(url_for('api_v1_system.get_system_properties'))
        assert rv.status_code == 200
        assert 'properties' in rv.get_json()

    # todo: review
    def test_vocabulary(self) -> None:
        c = self.client
        e = self.get_api_entities()
        with app.test_request_context():
            app.preprocess_request()
            vocabulary_type = next(iter(g.types.values()))
            file = Entity.get_by_class('file')[0]
            file.link('P67', vocabulary_type)
            reference_system = next(iter(g.reference_systems.values()))
            reference_system.link(
                'P67',
                vocabulary_type,
                'vocabulary-id',
                type_id=self.precision_type.subs[0])
            reference = insert('bibliography', 'Vocabulary reference')
            reference.link('P67', vocabulary_type, '12-13')
        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_list'))
        assert rv.status_code == 200

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
                'api_v1_vocabulary.get_vocabulary_item',
                id=e.boundary_mark.id))
        assert rv.status_code == 200

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_item',
                id=e.place.id))
        assert rv.status_code == 404

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
                openatlas_class='place',
                case_study=e.case_study.id))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

    # todo: review
    def test_vocabulary_skos(self) -> None:
        skos = 'http://www.w3.org/2004/02/skos/core#'
        c = self.client
        with app.test_request_context():
            app.preprocess_request()
            root = self.precision_type
            child = g.types[root.subs[0]]
            reference_system = next(iter(g.reference_systems.values()))
            reference_system.link(
                'P67',
                child,
                'vocabulary-id',
                type_id=self.precision_type.subs[0])
            resolver = reference_system.resolver_url
            other = g.types[root.subs[-1]]
            other_uri = URIRef(url_for(
                'api.entity_uuid', uuid=other.uuid, _external=True))
            reference_system.link(
                'P67',
                other,
                'University positions',
                type_id=self.precision_type.subs[0])
            root_uri = URIRef(url_for(
                'api.entity_uuid', uuid=root.uuid, _external=True))

        format_map = {
            'ttl': ('turtle', 'text/turtle'),
            'xml': ('xml', 'application/rdf+xml'),
            'json': ('json-ld', 'application/ld+json'),
            'nt': ('nt', 'application/n-triples')}
        for ext, (rdf_format, mimetype) in format_map.items():
            rv = c.get(
                url_for(
                    'api_v1_vocabulary.get_vocabulary_skos_ext',
                    id=root.id,
                    ext=ext))
            assert rv.status_code == 200
            assert mimetype in rv.headers.get('Content-Type')
            graph = Dataset()
            graph.parse(data=rv.data, format=rdf_format)
            assert (
                       root_uri, RDF.type,
                       URIRef(f'{skos}ConceptScheme')) in graph

        rv = c.get(
            url_for('api_v1_vocabulary.get_vocabulary_skos', id=root.id))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')

        for rdf_format, mimetype in [
            ('turtle', 'text/turtle'),
            ('xml', 'application/rdf+xml'),
            ('json-ld', 'application/ld+json'),
            ('nt', 'application/n-triples')]:
            rv = c.get(
                url_for('api_v1_vocabulary.get_vocabulary_skos', id=root.id),
                headers={'Accept': mimetype})
            assert rv.status_code == 200
            assert mimetype in rv.headers.get('Content-Type')
            graph = Dataset()
            graph.parse(data=rv.data, format=rdf_format)
            assert (
                       root_uri, RDF.type,
                       URIRef(f'{skos}ConceptScheme')) in graph

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=root.id,
                ext='ttl'))
        graph = Dataset()
        graph.parse(data=rv.data, format='turtle')

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=root.id,
                ext='nt'))
        assert rv.status_code == 200
        graph = Dataset()
        graph.parse(data=rv.data, format='nt')
        match_links = list(
            graph.objects(other_uri, URIRef(f'{skos}exactMatch'))) + list(
            graph.objects(other_uri, URIRef(f'{skos}closeMatch')))
        assert all(' ' not in str(uri) for uri in match_links)
        if resolver:
            assert URIRef(f'{resolver}University%20positions') in match_links

        # Unknown id returns 404
        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos',
                id=999999))
        assert rv.status_code == 404
        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=999999,
                ext='ttl'))
        assert rv.status_code == 404

    def test_metadata(self) -> None:
        c = self.client
        e = self.get_api_entities()

        # Case studies
        rv = c.get(url_for('api_v1_metadata.get_case_studies'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

        rv = c.get(
            url_for(
                'api_v1_metadata.get_case_study_by_id',
                id=e.case_study.id))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'id' in rv_json
        assert 'name' in rv_json

        rv = c.get(url_for('api_v1_metadata.get_case_study_by_id', id=99999))
        assert rv.status_code == 404

        # Agents
        rv = c.get(url_for('api_v1_metadata.get_agents'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

        # Agent by ID
        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=999999))
        assert rv.status_code == 404
        assert rv.get_json()['details']['provided_uuid'] == '999999'

        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=1))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'name' in rv_json
        assert 'class' in rv_json

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
                    'description': 'OpenAtlas logo',
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[1]},
                follow_redirects=True)

        e = self.get_api_entities()
        lic_url = 'https://creativecommons.org/licenses/by/4.0/'
        with app.test_request_context():
            app.preprocess_request()
            lic_ext_ref = insert('external_reference', lic_url)
            lic_ext_ref.link('P67', e.open_license)
            e.file.link('P2', e.open_license)

        with c.get(
                url_for('api_v1_files.display_file', id=e.file.id)) as rv:
            assert rv.status_code in (200, 302, 404)
        with c.get(
                url_for(
                    'api_v1_files.display_file',
                    id=e.file_without_file.id)) as rv:
            assert rv.status_code in (200, 302, 404)
        with c.get(
                url_for(
                    'api_v1_files.display_file',
                    id=e.file.id,
                    download=True)) as rv:
            assert rv.status_code == 200
            assert f'filename={e.file.id}.png' in rv.headers.get(
                'Content-Disposition', '')

        with c.get(
                url_for('api_v1_files.display_thumbnail', id=e.file.id)) as rv:
            assert rv.status_code in (200, 302, 404)
        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_without_file.id)) as rv:
            assert rv.status_code in (200, 302, 404)
        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file.id,
                    download=True)) as rv:
            assert rv.status_code == 200
            assert f'filename={e.file.id}.png' in rv.headers.get(
                'Content-Disposition', '')

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_not_public.id)) as rv:
            assert rv.status_code == 403

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_without_licences.id)) as rv:
            assert rv.status_code == 403

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.place.id)) as rv:
            assert rv.status_code == 404

        rv = c.get(url_for('api_v1_files.get_public_files'))
        assert rv.status_code == 200
        assert 'data' in rv.get_json()

    def test_iiif(self) -> None:
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
                    'description': 'OpenAtlas logo',
                    'file': img,
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[1]},
                follow_redirects=True)

        e = self.get_api_entities()
        lic_url = 'https://creativecommons.org/licenses/by/4.0/'
        with app.test_request_context():
            app.preprocess_request()
            lic_ext_ref = insert('external_reference', lic_url)
            lic_ext_ref.link('P67', e.open_license)
            e.file.link('P2', e.open_license)
            e.file.link('P67', e.actor)
            e.file.link('P67', lic_ext_ref, inverse=True)
            set_logo(e.file.id)

            AnnotationImage.insert(
                image_id=e.file.id,
                coordinates='10,10,50,50',
                entity_id=e.place.id,
                text='Sample IIIF annotation')
            annotations = AnnotationImage.get_by_file_id(e.file.id)
            annotation_id = annotations[0].id

        # Manifest
        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_manifest',
                id=e.file.id,
                version='2'))
        assert rv.status_code == 200
        manifest_v2 = rv.get_json()
        assert manifest_v2['@type'] == 'sc:Manifest'
        assert manifest_v2['license'] == lic_url
        assert 'Public domain' in manifest_v2['attribution']

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_manifest',
                id=e.file.id,
                version='3'))
        assert rv.status_code == 200
        manifest_v3 = rv.get_json()
        assert manifest_v3['type'] == 'Manifest'
        assert manifest_v3['rights'] == lic_url
        statement = manifest_v3['requiredStatement']['value']['en'][0]
        assert 'Public domain' in statement

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_manifest',
                id=e.file.id,
                version='99'))
        assert rv.status_code == 422

        # Canvas
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id, version='3'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id, version='99'))
        assert rv.status_code == 422

        # Image
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id, version='3'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id, version='99'))
        assert rv.status_code == 422

        # Direct URL structure check: /api/1/iiif/<id>/image/<version>
        rv = c.get(f'/api/1/iiif/{e.file.id}/image/2')
        assert rv.status_code == 200

        # Annotation list
        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation_list',
                id=e.file.id,
                version='2'))
        assert rv.status_code == 200
        assert rv.get_json()['@type'] == 'sc:AnnotationList'

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation_list',
                id=e.file.id,
                version='3'))
        assert rv.status_code == 200
        assert rv.get_json()['type'] == 'AnnotationPage'

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation_list',
                id=e.file.id,
                version='99'))
        assert rv.status_code == 422

        # Annotation
        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation',
                id=annotation_id,
                version='2'))
        assert rv.status_code == 200
        assert rv.get_json()['@type'] == 'oa:Annotation'

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation',
                id=annotation_id,
                version='3'))
        assert rv.status_code == 200
        assert rv.get_json()['type'] == 'Annotation'

        rv = c.get(f'/api/1/iiif/{annotation_id}/annotation/2')
        assert rv.status_code == 200

        rv = c.get(f'/api/1/iiif/{e.file.id}/manifest/4')
        assert rv.status_code in (400, 422)

        rv = c.get('/api/1/iiif/999999/manifest/2')
        assert rv.status_code == 404
        assert rv.get_json()['details']['provided_uuid'] == '999999'

        for id_ in [0, 999999]:
            rv = c.get(f'/api/1/iiif/{id_}/annotation/3')
            assert rv.status_code == 404
            assert rv.get_json()['details']['provided_id'] == str(id_)

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
