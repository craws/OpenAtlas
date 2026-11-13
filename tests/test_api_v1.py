from http import HTTPStatus
from pathlib import Path

from flask import g, url_for
from rdflib import RDF, Dataset, URIRef

from openatlas import app
from openatlas.api.api_v1.formatters.la_formatter import format_la_entities
from openatlas.api.api_v1.formatters.lod import format_lod_entities
from openatlas.database import overlay as db_overlay
from openatlas.models.annotation import AnnotationImage, AnnotationText
from openatlas.models.settings import set_logo
from tests.base import ApiTestCase, get_hierarchy, insert


class ApiV1(ApiTestCase):

    def upload_logo(self) -> None:
        with app.test_request_context():
            app.preprocess_request()
            rights_holder_ids = [rh.id for rh in g.rights_holder]

        logo_path = Path(app.root_path) / 'static' / 'images' / 'layout'
        public_type = get_hierarchy('Public sharing allowed')
        with open(logo_path / 'logo.png', 'rb') as img:
            self.client.post(
                url_for('insert', class_='file'),
                data={
                    'name': 'OpenAtlas logo',
                    'file': img,
                    'description': 'OpenAtlas logo',
                    'creator': f'{rights_holder_ids}',
                    'license_holder': f'{rights_holder_ids}',
                    str(public_type.id): public_type.subs[1]},
                follow_redirects=True)

    def test_lod(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.place.uuid))
        assert 'application/ld+json' in rv.headers.get('Content-Type', '')
        rv_json = rv.get_json()
        assert rv_json['@context'] == url_for(
            'api_v1_lod.get_context', _external=True)
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'Place'
        assert rv_json['label'] == 'Shire'

        with app.test_request_context():
            app.preprocess_request()
            AnnotationText.delete_annotations_text(e.source.id)
            AnnotationText.delete_annotations_text(e.translation.id)
            AnnotationText.insert({
                'source_id': e.source.id,
                'entity_id': e.actor.id,
                'link_start': 4,
                'link_end': 16,
                'text': 'Tales of the First Age'})
            AnnotationText.insert({
                'source_id': e.source.id,
                'entity_id': None,
                'link_start': 17,
                'link_end': 20,
                'text': 'Comment only'})
            AnnotationText.insert({
                'source_id': e.translation.id,
                'entity_id': e.actor.id,
                'link_start': 0,
                'link_end': 12,
                'text': None})

        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.source.uuid))
        source_data = rv.get_json()
        annotation = source_data['annotations'][0]
        assert annotation['type'] == 'Annotation'
        assert annotation['body_comment'] == 'Tales of the First Age'
        assert annotation['target'] == {
            'source': source_data['id'],
            'selector': {
                'type': 'TextPositionSelector',
                'start': 4,
                'end': 16}}
        assert annotation['body_entity'].endswith(
            str(e.actor.uuid))
        assert source_data['annotations'][1] == {
            'type': 'Annotation',
            'body_comment': 'Comment only',
            'target': {
                'source': source_data['id'],
                'selector': {
                    'type': 'TextPositionSelector',
                    'start': 17,
                    'end': 20}}}

        rv = c.get(
            url_for('api_v1_lod.get_entity', uuid=e.translation.uuid))
        translation_annotation = rv.get_json()['annotations'][0]
        assert 'body_comment' not in translation_annotation
        assert translation_annotation['body_entity'].endswith(
            str(e.actor.uuid))
        rv = c.get(url_for(
            'api_v1_lod.get_entity_ext', uuid=e.source.uuid, ext='ttl'))
        assert rv.status_code == HTTPStatus.OK
        assert 'text/turtle' in rv.headers.get('Content-Type', '')

        rv = c.get(
            url_for('api_v1_lod.get_entity_ext', uuid=e.place.uuid, ext='ttl'))
        assert 'text/turtle' in rv.headers.get('Content-Type', '')

        for params in [
            {'caseStudy': e.case_study.id, 'limit': 1, 'page': 2},
            {'caseStudy': e.place.uuid, 'limit': 5, 'offset': 2},
            {'startDate': '1988-02-03', 'endDate': '1988-04-03'},
            {'startDate': '-400',
             'endDate': '2000-05',
             'caseStudy': e.case_study.uuid,
             'sortBy': 'name',
             'sort': 'desc'},
            {'startDate': '2000', 'endDate': '-500'},
            {'startDate': '2000-02', 'endDate': '1900-02'},
            {'endDate': '2004-02'},
            {'endDate': '2001-02', 'search': e.place.name},
            {'endDate': '2020-04'},
            {'startDate': '-400-02-28',
             'endDate': '-500-03-15',
             'typeId': e.boundary_mark.id},
            {'startDate': '   '}]:
            rv = c.get(url_for(
                'api_v1_lod.get_entities',
                entity_class='acquisition',
                **params))
            assert rv.status_code == HTTPStatus.OK

        for sort_field, sort_order in [
                ('startDate', 'asc'),
                ('start_date', 'desc'),
                ('endDate', 'asc'),
                ('end_date', 'desc')]:
            rv = c.get(url_for(
                'api_v1_lod.get_entities',
                entity_class='acquisition',
                sortBy=sort_field,
                sort=sort_order))
            assert rv.status_code == HTTPStatus.OK

        rv = c.get(url_for(
            'api_v1_lod.get_entities',
            entity_class='acquisition',
            sortBy='invalid_field'))
        assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        rv = c.get(url_for(
            'api_v1_lod.get_entities',
            entity_class='acquisition',
            startDate='0'))
        assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert b'There is no year 0' in rv.data

        for params in [
            {'startDate': '2000-13'},
            {'startDate': '2000-13-15'},
            {'startDate': '2001-02-29'},
            {'startDate': 'invalid'},
            {'startDate': '2020-01-01-01'},
            {'startDate': '999999999'},
            {'search': 'bad\x00search'}]:
            rv = c.get(
                url_for(
                    'api_v1_lod.get_entities',
                    entity_class='acquisition'),
                query_string=params)
            assert rv.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        rv = c.get(
            url_for(
                'api_v1_lod.get_entities',
                entity_class='type',
                limit=1,
                page=2))
        assert rv.status_code == HTTPStatus.OK
        assert 'prev' in rv.get_json()

        assert format_lod_entities([]) == {
            '@context': url_for('api_v1_lod.get_context', _external=True),
            'type': 'OrderedCollection',
            'totalItems': 0,
            'orderedItems': []}

        # Context endpoint test
        rv = c.get(url_for('api_v1_lod.get_context'))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        ctx = rv.get_json()
        assert '@context' in ctx
        assert 'crm' in ctx['@context']
        assert 'archaeo' in ctx['@context']
        assert 'geo' in ctx['@context']
        assert ctx['@context']['oa'] == 'http://www.w3.org/ns/oa#'
        assert ctx['@context']['annotations'] == {
            '@reverse': 'oa:hasTarget'}
        assert ctx['@context']['body_entity'] == {
            '@id': 'oa:hasBody', '@type': '@id'}
        assert ctx['@context']['Feature'] == 'crm:E25_Human-Made_Feature'

        # Ontology endpoint test
        rv = c.get(url_for('api_v1_lod.get_ontology'))
        assert rv.status_code == 200
        rv_ttl = c.get(url_for('api_v1_lod.get_ontology_ext', ext='ttl'))
        assert rv_ttl.status_code == 200
        assert 'text/turtle' in rv_ttl.headers.get('Content-Type')
        assert b'has_relationship_to' in rv_ttl.data

        rv = c.get(url_for(
            'api_v1_lod.get_entities', entity_class='acquisition',
            startDate='999999999'))
        assert rv.status_code == 422

        rv = c.get(
            url_for(
                'api_v1_lod.get_entity',
                uuid='7404a969-97ba-4861-a555-3a97be2be967'))
        assert rv.status_code == HTTPStatus.NOT_FOUND

    def test_la(self) -> None:
        c = self.client
        self.upload_logo()
        e = self.get_api_entities()
        with app.test_request_context():
            app.preprocess_request()
            e.file.link('P67', e.place)
            e.file.link('P2', e.open_license)

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.place.uuid))
        response = rv.headers.get('Content-Type')
        assert response and 'application/ld+json' in response
        rv_json = rv.get_json()
        assert rv_json[
                   '@context'] == 'https://linked.art/ns/v1/linked-art.json'
        assert '@graph' not in rv_json
        assert rv_json['type'] == 'HumanMadeObject'
        assert rv_json['current_location']['type'] == 'Place'
        assert rv_json['_label'] == 'Shire'

        rv = c.get(
            url_for(
                'api_v1_la.get_entity_ext',
                uuid=e.place.uuid,
                ext='ttl'))
        response = rv.headers.get('Content-Type')
        assert response and 'text/turtle' in response

        rv = c.get(
            url_for(
                'api_v1_la.get_entity',
                uuid='7404a969-97ba-4861-a555-3a97be2be967'))
        assert rv.status_code == HTTPStatus.NOT_FOUND

        for class_ in ['place', 'person', 'artifact', 'file', 'type']:
            rv = c.get(
                url_for('api_v1_la.get_entities', entity_class=class_))
            assert rv.status_code == HTTPStatus.OK
            rv_json = rv.get_json()
            assert rv_json['type'] == 'OrderedCollectionPage'
            assert rv_json['orderedItems']
            assert rv_json['partOf']['type'] == 'OrderedCollection'

        rv = c.get(
            url_for(
                'api_v1_la.get_entities',
                entity_class='type',
                limit=1,
                page=2))
        assert rv.status_code == HTTPStatus.OK
        assert 'prev' in rv.get_json()

        assert format_la_entities([]) == {
            '@context': [
                'https://linked.art/ns/v1/linked-art.json',
                'https://linked.art/ns/v1/search.json'],
            'type': 'OrderedCollection',
            'totalItems': 0,
            'orderedItems': []}

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.move.uuid))
        part = rv.get_json()['part'][0]
        assert part['type'] == 'Move'
        assert part['moved'][0]['id'].endswith(e.artifact.uuid)
        assert part['moved_to']['type'] == 'Place'
        assert part['moved_from']['type'] == 'Place'
        assert 'influenced_by' in rv.get_json()

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.empty_move.uuid))
        assert 'part' not in rv.get_json()

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.artifact.uuid))
        rv_json = rv.get_json()
        assert rv_json['produced_by']['type'] == 'Production'
        assert rv_json['destroyed_by']['type'] == 'Destruction'
        assert 'timespan' in rv_json['destroyed_by']
        assert 'changed_ownership_through' in rv_json
        assert 'modified_by' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.event.uuid))
        rv_json = rv.get_json()
        assert rv_json['type'] == 'Activity'
        assert 'took_place_at' in rv_json
        assert 'carried_out_by' in rv_json
        assert 'participant' in rv_json
        assert 'before' in rv_json
        assert 'timespan' in rv_json
        assert 'referred_to_by' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.event2.uuid))
        rv_json = rv.get_json()
        assert rv_json['part_of']['type'] == 'Activity'
        assert 'after' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.actor.uuid))
        rv_json = rv.get_json()
        assert rv_json['type'] == 'Person'
        assert 'member_of' in rv_json
        assert 'participated_in' in rv_json
        assert 'residence' in rv_json
        assert 'referred_to_by' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.file.uuid))
        rv_json = rv.get_json()
        assert rv_json['type'] == 'DigitalObject'
        assert 'dimension' in rv_json
        assert 'access_point' in rv_json
        assert 'created_by' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.source.uuid))
        rv_json = rv.get_json()
        assert rv_json['type'] == 'LinguisticObject'
        assert 'referred_to_by' in rv_json

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.bibliography.uuid))
        rv_json = rv.get_json()
        assert 'about' in rv_json

        rv = c.get(url_for(
            'api_v1_la.get_entity', uuid=e.stratigraphic_unit.uuid))
        assert 'attributed_by' in rv.get_json()

        rv = c.get(url_for('api_v1_la.get_entity', uuid=e.location.uuid))
        assert 'defined_by' in rv.get_json()

        rv = c.get(
            url_for('api_v1_la.get_entity', uuid=e.administrative_unit.uuid))
        assert 'defined_by' in rv.get_json()

        for entity in (e.group, e.production, e.translation):
            rv = c.get(url_for('api_v1_la.get_entity', uuid=entity.uuid))
            assert rv.status_code == HTTPStatus.OK

        for entity in (e.place, e.feature):
            rv = c.get(url_for('api_v1_la.get_entity', uuid=entity.uuid))
            rv_json = rv.get_json()
            assert rv_json['type'] == 'HumanMadeObject'

    def test_system(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_root.api_v1_index'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert rv_json['name'] == "OpenAtlas API"
        assert 'version' in rv_json
        assert 'openapiSchema' in rv_json
        assert 'documentation' in rv_json
        assert 'manual' in rv_json

        rv = c.get(url_for('api_v1_system.get_system_info'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'apiVersions' in rv_json
        assert isinstance(rv_json['apiVersions'], dict)
        assert 'defaultLanguage' in rv_json
        assert 'iiif' in rv_json
        assert isinstance(rv_json['iiif'], dict)
        assert rv_json['iiif']['version'] == (
            '3' if rv_json['iiif']['enabled'] else None)
        assert 'imageProcessing' in rv_json
        assert isinstance(rv_json['imageProcessing'], dict)
        assert 'logoFileId' in rv_json
        assert 'mapConfig' in rv_json
        assert isinstance(rv_json['mapConfig'], dict)
        assert 'siteName' in rv_json
        assert 'version' in rv_json

        rv = c.get(
            url_for(
                'api_v1_system.get_entity_count',
                case_study=e.case_study.id))
        assert 'counts' in rv.get_json()

        rv = c.get(url_for('api_v1_system.get_system_classes'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'locale' in rv_json
        assert 'results' in rv_json
        assert isinstance(rv_json['results'], list)
        rv = c.get(url_for('api_v1_system.get_system_classes', locale='de'))
        assert 'de' in rv.get_json()['locale']

        rv = c.get(url_for('api_v1_system.get_entity_count'))
        assert 'counts' in rv.get_json()

        rv = c.get(url_for('api_v1_system.get_system_properties'))
        assert rv.status_code == HTTPStatus.OK
        assert 'properties' in rv.get_json()

    def test_vocabulary(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_list'))
        assert rv.status_code == HTTPStatus.OK
        assert any(
            v['timespan']['start']['earliest']
            for v in rv.get_json()['data'].values()
            if v['timespan'])

        rv = c.get(url_for('api_v1_vocabulary.get_vocabulary_tree'))
        assert rv.status_code == HTTPStatus.OK
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
                id=e.open_license.id))
        assert rv.status_code == HTTPStatus.OK

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_item',
                id=e.place.id))
        assert rv.status_code == HTTPStatus.NOT_FOUND

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_tree_by_class',
                openatlas_class='place'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'place' in rv_json

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_standard_by_class',
                openatlas_class='place',
                case_study=e.case_study.id))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

    def test_vocabulary_skos(self) -> None:
        skos = 'http://www.w3.org/2004/02/skos/core#'
        c = self.client
        e = self.get_api_entities()
        root_uri = URIRef(url_for(
            'api.entity_uuid', uuid=e.license.uuid, _external=True))
        sub_uri = URIRef(url_for(
            'api.entity_uuid', uuid=e.open_license.uuid, _external=True))

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=e.license.id,
                ext='ttl'))
        assert rv.status_code == HTTPStatus.OK
        assert 'text/turtle' in rv.headers.get('Content-Type', '')
        graph = Dataset()
        graph.parse(data=rv.data, format='turtle')
        assert (root_uri, RDF.type, URIRef(f'{skos}ConceptScheme')) in graph
        assert (sub_uri, RDF.type, URIRef(f'{skos}Concept')) in graph
        assert (sub_uri, URIRef(f'{skos}topConceptOf'), root_uri) in graph
        assert (root_uri, URIRef(f'{skos}hasTopConcept'), sub_uri) in graph
        assert bool(
            list(graph.triples((None, URIRef(f'{skos}broader'), None))))
        assert bool(
            list(graph.triples((None, URIRef(f'{skos}narrower'), None))))
        assert bool(
            list(graph.triples((None, URIRef(f'{skos}inScheme'), root_uri))))
        assert bool(list(graph.objects(sub_uri, URIRef(f'{skos}exactMatch'))))
        assert bool(list(graph.objects(sub_uri, URIRef(f'{skos}closeMatch'))))
        assert bool(list(graph.objects(sub_uri, URIRef(f'{skos}scopeNote'))))

        rv = c.get(
            url_for('api_v1_vocabulary.get_vocabulary_skos', id=e.license.id))
        assert rv.status_code == HTTPStatus.OK
        assert 'application/ld+json' in rv.headers.get('Content-Type', '')

        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos',
                id=999999))
        assert rv.status_code == HTTPStatus.NOT_FOUND
        rv = c.get(
            url_for(
                'api_v1_vocabulary.get_vocabulary_skos_ext',
                id=999999,
                ext='ttl'))
        assert rv.status_code == HTTPStatus.NOT_FOUND

    def test_metadata(self) -> None:
        c = self.client
        e = self.get_api_entities()

        rv = c.get(url_for('api_v1_metadata.get_case_studies'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

        rv = c.get(
            url_for(
                'api_v1_metadata.get_case_study_by_id',
                id=e.case_study.id))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'id' in rv_json
        assert 'name' in rv_json

        rv = c.get(url_for('api_v1_metadata.get_case_study_by_id', id=99999))
        assert rv.status_code == HTTPStatus.NOT_FOUND

        rv = c.get(url_for('api_v1_metadata.get_agents'))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'data' in rv_json
        assert isinstance(rv_json['data'], list)

        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=999999))
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert rv.get_json()['details']['provided_id'] == '999999'

        rv = c.get(url_for('api_v1_metadata.get_agent_by_id', id=1))
        assert rv.status_code == HTTPStatus.OK
        rv_json = rv.get_json()
        assert 'name' in rv_json
        assert 'class' in rv_json

    def test_files(self) -> None:
        c = self.client
        self.upload_logo()
        e = self.get_api_entities()
        lic_url = 'https://creativecommons.org/licenses/by/4.0/'
        with app.test_request_context():
            app.preprocess_request()
            lic_ext_ref = insert('external_reference', lic_url)
            lic_ext_ref.link('P67', e.open_license)
            e.file.link('P2', e.open_license)
            e.file.link('P67', e.actor)
            e.file_not_public.link('P67', e.actor)
            e.file_without_licences.link('P67', e.actor)

        with c.get(
                url_for('api_v1_files.display_file', id=e.file.id)) as rv:
            assert rv.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
        with c.get(
                url_for(
                    'api_v1_files.display_file',
                    id=e.file_without_file.id)) as rv:
            assert rv.status_code == HTTPStatus.NOT_FOUND
        with c.get(
                url_for(
                    'api_v1_files.display_file',
                    id=e.file.id,
                    download=True)) as rv:
            assert rv.status_code == HTTPStatus.OK
            assert f'filename={e.file.id}.png' in rv.headers.get(
                'Content-Disposition', '')

        with c.get(
                url_for('api_v1_files.display_thumbnail', id=e.file.id)) as rv:
            assert rv.status_code in (HTTPStatus.OK, HTTPStatus.FOUND)
        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_without_file.id)) as rv:
            assert rv.status_code == HTTPStatus.NOT_FOUND
        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file.id,
                    download=True)) as rv:
            assert rv.status_code == HTTPStatus.OK
            assert f'filename={e.file.id}.png' in rv.headers.get(
                'Content-Disposition', '')

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_not_public.id)) as rv:
            assert rv.status_code == HTTPStatus.FORBIDDEN

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.file_without_licences.id)) as rv:
            assert rv.status_code == HTTPStatus.FORBIDDEN

        with c.get(
                url_for(
                    'api_v1_files.display_thumbnail',
                    id=e.place.id)) as rv:
            assert rv.status_code == HTTPStatus.NOT_FOUND

        rv = c.get(url_for('api_v1_files.get_public_files'))
        assert rv.status_code == HTTPStatus.OK
        assert 'data' in rv.get_json()

        rv = c.get(
            url_for('api_v1_files.get_public_files_by_entity', id=e.actor.id))
        assert rv.status_code == HTTPStatus.OK
        json_data = rv.get_json()
        assert 'data' in json_data
        file_ids = [item['id'] for item in json_data['data']]
        assert e.file.id in file_ids
        assert e.file_not_public.id not in file_ids
        assert e.file_without_licences.id not in file_ids
        file_item = next(
            item for item in json_data['data'] if item['id'] == e.file.id)
        assert file_item['iiifManifestUrl'].endswith(
            f'/api/1/iiif/{e.file.id}/manifest')

        rv = c.get(
            url_for('api_v1_files.get_public_files_by_entity', id=e.weight.id))
        assert rv.status_code == HTTPStatus.OK
        assert rv.get_json()['data'] == []
        assert rv.get_json()['totalItems'] == 0

    def test_iiif(self) -> None:
        c = self.client
        self.upload_logo()
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
            overlay_data = {
                'image_id': e.file.id,
                'bounding_box': (
                    '[[48.58653, 15.64356], [48.58709, 15.64294]]')}
            if db_overlay.get_by_object([e.file.id]):
                db_overlay.update(overlay_data)
            else:
                db_overlay.insert(overlay_data)

            AnnotationImage.insert(
                image_id=e.file.id,
                coordinates='10,10,50,50',
                entity_id=e.place.id,
                text='Sample IIIF annotation')
            annotations = AnnotationImage.get_by_file_id(e.file.id)
            annotation_id = annotations[0].id

        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_manifest',
                id=e.file.id))
        assert rv.status_code == HTTPStatus.OK
        manifest = rv.get_json()
        assert manifest['type'] == 'Manifest'
        assert manifest['@context'] == [
            'https://iiif.io/api/extension/georef/1/context.json',
            'https://iiif.io/api/presentation/3/context.json']
        assert manifest['id'].endswith(
            f'/api/1/iiif/{e.file.id}/manifest')
        assert manifest['rights'] == lic_url
        site_provider = manifest['provider'][0]
        assert site_provider['type'] == 'Agent'
        assert site_provider['label']['en'] == [
            c.get(url_for('api_v1_system.get_system_info')).get_json()[
                'siteName']]
        assert site_provider['homepage'][0] == {
            'id': url_for('overview', _external=True),
            'type': 'Text',
            'label': site_provider['label'],
            'format': 'text/html'}
        assert site_provider['logo']
        statement = manifest['requiredStatement']['value']['en'][0]
        assert 'Public domain' in statement

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_georeference', id=e.file.id))
        assert rv.status_code == HTTPStatus.OK
        georeference = rv.get_json()
        georeference_path = f'/api/1/iiif/{e.file.id}/georeference'
        assert georeference['id'].endswith(georeference_path)
        georeference_annotation = georeference['items'][0]
        assert georeference_annotation['motivation'] == 'georeferencing'
        georeference_source = georeference_annotation['target']['source']
        assert georeference_source['type'] == 'ImageService2'
        assert georeference_source['partOf'] == [{
            'id': manifest['id'],
            'type': 'Manifest'}]
        assert georeference_source['provider'] == [site_provider]
        features = georeference_annotation['body']['features']
        assert (
            [feature['geometry']['coordinates'] for feature in features]
            == [[15.64294, 48.58709], [15.64356, 48.58709],
                [15.64294, 48.58653]])

        rv = c.get(
            url_for('api_v1_iiif.get_iiif_canvas', id=e.file.id))
        assert rv.status_code == HTTPStatus.OK
        canvas = rv.get_json()
        canvas_path = f'/api/1/iiif/{e.file.id}/canvas'
        assert canvas['id'].endswith(canvas_path)
        assert manifest['items'][0]['id'].endswith(canvas_path)
        assert any(
            annotation_page['id'].endswith(georeference_path)
            for annotation_page in canvas['annotations'])

        # Image
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_image', id=e.file.id))
        assert rv.status_code == HTTPStatus.OK
        image = rv.get_json()
        image_path = f'/api/1/iiif/{e.file.id}/image'
        assert image['body']['service'][0]['type'] == 'ImageService2'
        assert image['id'].endswith(image_path)
        assert image['target'].endswith(canvas_path)
        assert canvas['items'][0]['items'][0]['id'].endswith(image_path)

        # Annotation list
        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation_list',
                id=e.file.id))
        assert rv.status_code == HTTPStatus.OK
        annotation_list = rv.get_json()
        annotation_list_path = f'/api/1/iiif/{e.file.id}/annotation-list'
        assert annotation_list['type'] == 'AnnotationPage'
        assert annotation_list['id'].endswith(annotation_list_path)
        assert canvas['annotations'][0]['id'].endswith(annotation_list_path)

        # Annotation
        rv = c.get(
            url_for(
                'api_v1_iiif.get_iiif_annotation',
                id=annotation_id))
        assert rv.status_code == HTTPStatus.OK
        annotation = rv.get_json()
        annotation_path = f'/api/1/iiif/{annotation_id}/annotation'
        assert annotation['type'] == 'Annotation'
        assert annotation['id'].endswith(annotation_path)
        assert annotation['target']['source'].endswith(canvas_path)

        with app.test_request_context():
            app.preprocess_request()
            set_logo()
        no_logo_manifest = c.get(
            url_for('api_v1_iiif.get_iiif_manifest', id=e.file.id)).get_json()
        no_logo_provider = no_logo_manifest['provider'][0]
        assert no_logo_provider['label'] == site_provider['label']
        assert no_logo_provider['homepage'] == site_provider['homepage']
        assert 'logo' not in no_logo_provider
        no_logo_georeference = c.get(
            url_for(
                'api_v1_iiif.get_iiif_georeference',
                id=e.file.id)).get_json()
        no_logo_source = no_logo_georeference['items'][0][
            'target']['source']
        assert no_logo_source['provider'] == [no_logo_provider]

        with app.test_request_context():
            app.preprocess_request()
            set_logo(e.file.id)

        openapi = c.get('/api/1/docs/openapi.json').get_json()
        iiif_paths = {
            f'/api/1/iiif/{{id}}/{endpoint}'
            for endpoint in (
                'manifest', 'canvas', 'image', 'annotation-list',
                'georeference', 'annotation')}
        assert iiif_paths <= openapi['paths'].keys()
        assert not any(
            path.startswith('/api/1/iiif/') and '{version}' in path
            for path in openapi['paths'])

        for path in (
                f'/api/1/iiif/{e.file.id}/manifest/3',
                f'/api/1/iiif/{e.file.id}/canvas/3',
                f'/api/1/iiif/{e.file.id}/image/3',
                f'/api/1/iiif/{e.file.id}/annotation-list/3',
                f'/api/1/iiif/{annotation_id}/annotation/3'):
            assert c.get(path).status_code == HTTPStatus.NOT_FOUND

        rv = c.get('/api/1/iiif/999999/manifest')
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert rv.get_json()['details']['provided_id'] == '999999'

        for id_ in [0, 999999]:
            rv = c.get(f'/api/1/iiif/{id_}/annotation')
            assert rv.status_code == HTTPStatus.NOT_FOUND
            assert rv.get_json()['details']['provided_id'] == str(id_)

        with app.test_request_context():
            app.preprocess_request()
            overlay = db_overlay.get_by_object([e.file.id])[0]
            db_overlay.remove(overlay['id'])
        rv = c.get(
            url_for('api_v1_iiif.get_iiif_georeference', id=e.file.id))
        assert rv.status_code == HTTPStatus.NOT_FOUND

    def test_search(self) -> None:
        c = self.client
        e = self.get_api_entities()
        with app.test_request_context():
            app.preprocess_request()
            insert('person', 'Smith', 'Exact match')
            insert('person', 'Smithson', 'Prefix match')
            insert('person', 'John Smith', 'Substring match')
            insert('person', 'Smyth', 'Phonetic match')
            insert('person', '1230', 'Numeric match')

        g.pop('types', None)
        rv = c.get(
            f'/api/1/search?typeId={e.boundary_mark.id}')
        assert rv.status_code == HTTPStatus.OK
        assert not hasattr(g, 'types')

        rv = c.get(
            url_for(
                'api_v1_frontend.search_entities',
                search='Smith',
                entityClass='person'))
        assert rv.status_code == HTTPStatus.OK
        data = rv.get_json()
        names = [item['name'] for item in data['data']]
        assert names[:4] == ['Smith', 'Smithson', 'John Smith', 'Smyth']
        assert data['data'][0]['systemClass'] == 'person'
        assert data['data'][0]['description'] == 'Exact match'

        rv = c.get('/api/1/search?search=0')
        assert rv.status_code == HTTPStatus.OK
        assert '1230' in [item['name'] for item in rv.get_json()['data']]

        rv = c.get(
            url_for(
                'api_v1_frontend.search_entities',
                search='Shire',
                entityClass='place'))
        assert rv.status_code == HTTPStatus.OK
        place_data = rv.get_json()['data']
        assert place_data[0]['name'] == 'Shire'
        assert place_data[0]['timespan'] is not None

        for params in [
            {'entityClass': 'place', 'limit': 1, 'page': 2},
            {'startDate': '-400', 'endDate': '2050-05'},
            {'typeId': e.boundary_mark.id},
            {'typeId': str(e.boundary_mark.uuid)},
            {'caseStudy': e.case_study.id},
            {'caseStudy': str(e.case_study.uuid)},
            {'sortBy': 'startDate', 'sort': 'desc'}]:
            rv = c.get(
                url_for('api_v1_frontend.search_entities', **params))
            assert rv.status_code == HTTPStatus.OK
            res = rv.get_json()
            assert 'totalItems' in res
            assert 'first' in res
            assert 'last' in res

        rv = c.get(
            url_for(
                'api_v1_frontend.search_entities',
                typeId=999999))
        assert rv.status_code == HTTPStatus.OK
        assert rv.get_json()['data'] == []
        assert rv.get_json()['totalItems'] == 0

    def test_docs(self) -> None:
        c = self.client
        for url in [
            '/api/1/docs/swagger',
            '/api/1/docs/openapi.json',
            '/api/1/docs/']:
            rv = c.get(url)
            assert rv.status_code == HTTPStatus.OK
        rv = c.get('/api/1/docs/Wrong!')
        assert rv.status_code == HTTPStatus.NOT_FOUND
        assert '/api/1/docs/swagger' in rv.get_json()['message']
