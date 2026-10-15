from flask import url_for
from rdflib import RDF, Graph, Namespace

from openatlas import app
from openatlas.api.api_v1.context.lod_context import get_oa_ontology_uri
from tests.base import ApiTestCase


class ApiV1LodTest(ApiTestCase):

    def test_lod_context_endpoint(self) -> None:
        c = self.client
        rv = c.get(url_for('api_v1_lod.get_context'))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        data = rv.get_json()
        assert '@context' in data
        ctx = data['@context']
        assert ctx['@version'] == 1.1
        assert ctx['crm'] == 'http://www.cidoc-crm.org/cidoc-crm/'
        assert ctx['archaeo'] == 'http://www.cidoc-crm.org/cidoc-crm/CRMarchaeo/'
        assert ctx['geo'] == 'http://www.opengis.net/ont/geosparql#'
        assert ctx['Feature'] == 'archaeo:A6_Feature'
        assert ctx['StratigraphicUnit'] == 'archaeo:A8_Stratigraphic_Unit'
        assert ctx['BiologicalObject'] == 'crm:E20_Biological_Object'
        assert ctx['HumanMadeObject'] == 'crm:E22_Human-Made_Object'
        assert ctx['is_composed_of']['@id'] == 'crm:P46_is_composed_of'
        assert ctx['forms_part_of']['@id'] == 'crm:P46i_forms_part_of'
        assert ctx['has_geometry']['@id'] == 'geo:hasGeometry'
        assert ctx['as_wkt']['@id'] == 'geo:asWKT'
        assert ctx['has_relationship_to']['@id'] == 'oa:has_relationship_to'

    def test_lod_ontology_endpoint(self) -> None:
        c = self.client

        # Default JSON-LD
        rv = c.get(url_for('api_v1_lod.get_ontology'))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')

        # Formats via extension
        for ext, mime in [
            ('ttl', 'text/turtle'),
            ('xml', 'application/rdf+xml'),
            ('nt', 'application/n-triples'),
            ('json', 'application/ld+json'),
        ]:
            rv = c.get(url_for('api_v1_lod.get_ontology_ext', ext=ext))
            assert rv.status_code == 200
            assert mime in rv.headers.get('Content-Type')

        # Verify Turtle ontology content
        rv_ttl = c.get(url_for('api_v1_lod.get_ontology_ext', ext='ttl'))
        g_ont = Graph()
        g_ont.parse(data=rv_ttl.data.decode('utf-8'), format='turtle')
        oa = Namespace(get_oa_ontology_uri())
        assert (oa.has_relationship_to, RDF.type, None) in g_ont
        assert (oa.begins_in, RDF.type, None) in g_ont
        assert (oa.ends_in, RDF.type, None) in g_ont

    def test_lod_entity_formats(self) -> None:
        c = self.client
        e = self.get_api_entities()

        # JSON-LD entity
        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.place.uuid))
        assert rv.status_code == 200
        assert 'application/ld+json' in rv.headers.get('Content-Type')
        data = rv.get_json()
        assert str(e.place.uuid) in data['id']
        assert data['type'] == 'Place'
        assert data['label'] == 'Shire'

        # Turtle entity
        rv_ttl = c.get(url_for('api_v1_lod.get_entity_ext', uuid=e.place.uuid, ext='ttl'))
        assert rv_ttl.status_code == 200
        assert 'text/turtle' in rv_ttl.headers.get('Content-Type')
        g_ent = Graph()
        g_ent.parse(data=rv_ttl.data.decode('utf-8'), format='turtle')
        crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
        ent_uri = data['id']
        from rdflib import URIRef
        assert (URIRef(ent_uri), RDF.type, crm.E53_Place) in g_ent

    def test_lod_archaeo_hierarchy_and_shortcuts(self) -> None:
        c = self.client
        e = self.get_api_entities()
        with app.test_request_context():
            app.preprocess_request()
            # Archaeological hierarchy: Place contains Feature contains StratigraphicUnit contains Artifact
            e.feature.link('P46', e.place, inverse=True)
            e.feature.link('P46', e.stratigraphic_unit)
            e.stratigraphic_unit.link('P46', e.artifact)
            e.feature.link('P53', e.location)

            # OpenAtlas shortcuts: begins_in, ends_in, relationship_to
            e.actor.link('OA8', e.administrative_unit)
            e.actor.link('OA9', e.administrative_unit)
            e.actor.link('OA7', e.actor2, type_id=e.relation_sub.id)

        # 1. Test Feature
        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.feature.uuid))
        assert rv.status_code == 200
        feature_data = rv.get_json()
        assert feature_data['type'] == 'Feature'
        assert feature_data['label'] == 'Home of Baggins'
        assert feature_data['forms_part_of']['type'] == 'Place'
        assert any(item['type'] == 'StratigraphicUnit' for item in feature_data['is_composed_of'])
        assert feature_data['has_location']['type'] == 'Place'
        assert feature_data['has_location']['has_geometry']['type'] == 'Geometry'
        assert 'POINT' in feature_data['has_location']['has_geometry']['as_wkt']

        # 2. Test Stratigraphic Unit
        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.stratigraphic_unit.uuid))
        assert rv.status_code == 200
        su_data = rv.get_json()
        assert su_data['type'] == 'StratigraphicUnit'
        assert su_data['forms_part_of']['type'] == 'Feature'
        assert any(item['type'] == 'HumanMadeObject' for item in su_data['is_composed_of'])

        # 3. Test Human-Made Object (Artifact)
        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.artifact.uuid))
        assert rv.status_code == 200
        artifact_data = rv.get_json()
        assert artifact_data['type'] == 'HumanMadeObject'
        assert artifact_data['label'] == 'The One Ring'

        # 4. Test Shortcuts on Person
        rv = c.get(url_for('api_v1_lod.get_entity', uuid=e.actor.uuid))
        assert rv.status_code == 200
        actor_data = rv.get_json()
        assert actor_data['type'] == 'Person'
        assert actor_data['begins_in']['type'] == 'Place'
        assert actor_data['ends_in']['type'] == 'Place'
        assert any(rel['type'] == 'Person' for rel in actor_data['has_relationship_to'])

        # 5. Test Turtle serialization for Feature
        rv_ttl = c.get(url_for('api_v1_lod.get_entity_ext', uuid=e.feature.uuid, ext='ttl'))
        assert rv_ttl.status_code == 200
        assert b'archaeo:A6_Feature' in rv_ttl.data or b'A6_Feature' in rv_ttl.data
        assert b'asWKT' in rv_ttl.data

    def test_lod_collection_and_pagination(self) -> None:
        c = self.client
        rv = c.get(url_for('api_v1_lod.get_entities', entity_class='place', limit=2, page=1))
        assert rv.status_code == 200
        col = rv.get_json()
        assert col['type'] == 'OrderedCollectionPage'
        assert col['partOf']['type'] == 'OrderedCollection'
        assert col['partOf']['totalItems'] >= 1
        assert len(col['orderedItems']) <= 2
        assert 'first' in col['partOf']
        assert 'last' in col['partOf']
