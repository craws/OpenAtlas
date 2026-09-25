from pathlib import Path

from flask import g, url_for

from openatlas import app
from openatlas.models.annotation import AnnotationImage
from openatlas.models.entity import Entity
from tests.base import ApiTestCase, get_hierarchy, insert

from rdflib import Dataset, RDF, URIRef


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

        rv = c.get(url_for(
            'api_v1_lod.entities', entity_class='acquisition',
            startDate='-400', endDate='2000-05'))
        assert rv.status_code == 200

        for params in [
                {'startDate': '0'},
                {'startDate': '-0'},
                {'startDate': '0000-03-15'},
                {'endDate': '0'},
                {'endDate': '0-05'}]:
            rv = c.get(url_for(
                'api_v1_lod.entities', entity_class='acquisition', **params))
            assert rv.status_code == 422
            assert b'There is no year 0' in rv.data

        rv = c.get(url_for(
            'api_v1_lod.entities', entity_class='acquisition',
            startDate='999999999'))
        assert rv.status_code == 400
        rv_json = rv.get_json()
        assert rv_json['status'] == 400
        assert {'title', 'message', 'details', 'url', 'timestamp'} \
            <= rv_json.keys()

        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=999999))
        assert rv.status_code == 404
        rv_json = rv.get_json()
        assert rv_json['status'] == 404
        assert {'title', 'message', 'details', 'url', 'timestamp'} \
            <= rv_json.keys()


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
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

    def test_vocabulary_skos(self) -> None:
        skos = 'http://www.w3.org/2004/02/skos/core#'
        dcterms = 'http://purl.org/dc/terms/'
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
            child_uri = URIRef(url_for(
                'api.entity_uuid', uuid=child.uuid, _external=True))
            grandchild = g.types[child.subs[0]] if child.subs else None
            grandchild_uri = URIRef(url_for(
                'api.entity_uuid',
                uuid=grandchild.uuid,
                _external=True)) if grandchild else None

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
                root_uri, RDF.type, URIRef(f'{skos}ConceptScheme')) in graph

        # Content negotiation tests
        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_skos', id=root.id))
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
                root_uri, RDF.type, URIRef(f'{skos}ConceptScheme')) in graph

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=root.id,
                ext='ttl'))
        graph = Dataset()
        graph.parse(data=rv.data, format='turtle')

        # ConceptScheme with placeholder dcterms metadata
        assert (root_uri, RDF.type, URIRef(f'{skos}ConceptScheme')) in graph

        # Immediate child is a top concept linked via hasTopConcept /
        # topConceptOf (never inScheme / broader / narrower to the scheme)
        assert (child_uri, RDF.type, URIRef(f'{skos}Concept')) in graph
        assert (root_uri, URIRef(f'{skos}hasTopConcept'), child_uri) in graph
        assert (child_uri, URIRef(f'{skos}topConceptOf'), root_uri) in graph
        assert (child_uri, URIRef(f'{skos}inScheme'), root_uri) not in graph
        assert (child_uri, URIRef(f'{skos}broader'), root_uri) not in graph
        assert (root_uri, URIRef(f'{skos}narrower'), child_uri) not in graph

        # Deeper descendants use inScheme and reciprocal broader / narrower
        # to their parent concept (not to the scheme)
        if grandchild_uri is not None:
            assert (
                grandchild_uri, RDF.type, URIRef(f'{skos}Concept')) in graph
            assert (
                grandchild_uri,
                URIRef(f'{skos}inScheme'),
                root_uri) in graph
            assert (
                grandchild_uri,
                URIRef(f'{skos}broader'),
                child_uri) in graph
            assert (
                child_uri,
                URIRef(f'{skos}narrower'),
                grandchild_uri) in graph
            assert (
                grandchild_uri,
                URIRef(f'{skos}topConceptOf'),
                root_uri) not in graph

        # External reference produces a match link
        match_links = list(
            graph.objects(child_uri, URIRef(f'{skos}exactMatch'))) + list(
            graph.objects(child_uri, URIRef(f'{skos}closeMatch')))
        assert match_links

        # Identifiers with spaces are URL-encoded, values without a
        # resolvable URI are skipped instead of crashing the serializer
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

        from openatlas.api.api_v1.formatters.skos import _get_match_uri
        from openatlas.api.api_v1.models.util import \
            ExternalReferenceSystemModel
        assert _get_match_uri(ExternalReferenceSystemModel(
            id=1, name='Local', identifier='University positions')) is None
        assert _get_match_uri(ExternalReferenceSystemModel(
            id=1,
            name='Wikidata',
            url='https://www.wikidata.org/wiki/',
            identifier='https://www.wikidata.org/wiki/Q 1')) == URIRef(
            'https://www.wikidata.org/wiki/Q%201')

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

        # Agents
        rv = c.get(url_for('api_v1_metadata.get_agents'))
        assert rv.status_code == 200
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

        # Agent by ID (dummy 1 for now)
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
                    id=e.file.id,
                    download=True)) as rv:
            assert rv.status_code == 200
            assert f'filename={e.file.id}.png' in rv.headers.get(
                'Content-Disposition', '')

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

            AnnotationImage.insert(
                image_id=e.file.id,
                coordinates='10,10,50,50',
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

        # Direct URL structure check: /api/1/iiif/<id>/manifest/<version>
        rv = c.get(f'/api/1/iiif/{e.file.id}/manifest/2')
        assert rv.status_code == 200
        rv = c.get(f'/api/1/iiif/{e.file.id}/manifest/3')
        assert rv.status_code == 200

        # Canvas
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id, version='3'))
        assert rv.status_code == 200

        # Direct URL structure check: /api/1/iiif/<id>/canvas/<version>
        rv = c.get(f'/api/1/iiif/{e.file.id}/canvas/2')
        assert rv.status_code == 200

        # Image
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id, version='2'))
        assert rv.status_code == 200

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id, version='3'))
        assert rv.status_code == 200

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

        # Direct URL structure check: /api/1/iiif/<id>/annotation-list/<version>
        rv = c.get(f'/api/1/iiif/{e.file.id}/annotation-list/2')
        assert rv.status_code == 200

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

        # Direct URL structure check: /api/1/iiif/<id>/annotation/<version>
        rv = c.get(f'/api/1/iiif/{annotation_id}/annotation/2')
        assert rv.status_code == 200

        # Error cases: unsupported version
        rv = c.get(f'/api/1/iiif/{e.file.id}/manifest/4')
        assert rv.status_code in (400, 422)

        # Error cases: id does not exist
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
