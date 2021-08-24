from flask import g, url_for
from nose.tools import raises

from openatlas import app
from openatlas.api.v02.endpoints.content.class_mapping import ClassMapping
from openatlas.api.v02.resources.error import (
    EntityDoesNotExistError, FilterOperatorError, InvalidCidocClassCode,
    InvalidCodeError, InvalidLimitError, InvalidSearchDateError,
    InvalidSearchNumberError, InvalidSubunitError, NoSearchStringError,
    QueryEmptyError)
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from tests import api_data
from tests.base import TestBaseCase, insert_entity


class ApiTests(TestBaseCase):

    def test_api(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                place = insert_entity(
                    'Nostromos', 'place',
                    description='That is the Nostromos')
                if not place:  # Needed for Mypy
                    return  # pragma: no cover

                # Adding Dates to place
                place.begin_from = '2018-01-31'
                place.begin_to = '2018-03-01'
                place.begin_comment = 'Begin of the Nostromos'
                place.end_from = '2019-01-31'
                place.end_to = '2019-03-01'
                place.end_comment = 'Destruction of the Nostromos'
                place.update()

                location = place.get_linked_entity_safe('P53')
                Gis.add_example_geom(location)

                # Adding Type Settlement
                place.link('P2', Node.get_hierarchy('Place'))

                # Adding Alias
                alias = insert_entity('Cargo hauler', 'appellation')
                place.link('P1', alias)

                # Adding External Reference
                external_reference = insert_entity(
                    'https://openatlas.eu',
                    'external_reference')
                external_reference.link(
                    'P67',
                    place,
                    description='OpenAtlas Website')

                # Adding feature to place
                feature = insert_entity('Feature', 'feature', place)

                # Adding stratigraphic to place
                insert_entity('Strato', 'stratigraphic_unit', feature)

                # Adding Administrative Unit Node
                unit_node = Node.get_hierarchy('Administrative unit')

                # Adding File to place
                file = insert_entity('Datei', 'file')
                file.link('P67', place)
                file.link('P2', g.nodes[Node.get_hierarchy('License').subs[0]])

                # Adding Value Type
                value_type = Node.get_hierarchy('Dimensions')
                place.link('P2', Entity.get_by_id(value_type.subs[0]), '23.0')

                # Adding Geonames
                geonames = Entity.get_by_id(
                    ReferenceSystem.get_by_name('GeoNames').id)
                precision_id = Node.get_hierarchy(
                    'External reference match').subs[0]
                geonames.link(
                    'P67',
                    place,
                    description='2761369',
                    type_id=precision_id)

            # Test LinkedPlaces output
            self.maxDiff = None
            rv = self.app.get(url_for('api.entity', id_=place.id))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_linked_place_template)

            # Test Geojson output
            rv = self.app.get(
                url_for('api.entity', id_=place.id, format='geojson'))
            self.assertDictEqual(rv.get_json(), api_data.api_geojson_template)

            # ---Content---

            # /api/0.2/classes/
            rv = self.app.get(url_for('api.class_mapping'))
            self.assertAlmostEqual(rv.get_json(), ClassMapping.mapping)

            # /api/0.2/content/
            rv = self.app.get(url_for('api.content', lang='de'))
            self.assertDictEqual(rv.get_json(), api_data.api_content_de)
            rv = self.app.get(url_for('api.content', lang='en', download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_content_en)

            # /api/0.2/geometric_entities/
            rv = self.app.get(url_for('api.geometric_entities'))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_geometries_template)
            rv = self.app.get(url_for('api.geometric_entities', download=True))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_geometries_template)
            rv = self.app.get(url_for('api.geometric_entities', count=True))
            assert b'1' in rv.data
            rv = self.app.get(url_for(
                'api.geometric_entities',
                geometry='gisLineAll',
                count=True))
            assert b'0' in rv.data

            # /api/0.2/overview_count/
            rv = self.app.get(url_for('api.overview_count'))
            self.assertAlmostEqual(rv.get_json(), api_data.api_overview_count)

            # /api/0.2/overview_count/
            rv = self.app.get(url_for('api.system_class_count'))
            self.assertDictEqual(rv.get_json(), api_data.api_system_class_count)

            # ---Nodes---

            # /api/0.2/node_entities/
            rv = self.app.get(url_for('api.node_entities', id_=unit_node.id))
            self.assertDictEqual(rv.get_json(), api_data.api_node_entities)
            rv = self.app.get(
                url_for('api.node_entities', id_=unit_node.id, download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_node_entities)
            rv = self.app.get(
                url_for('api.node_entities', id_=unit_node.id, count=True))
            assert b'6' in rv.data

            # /api/0.2/node_entities_all/
            rv = self.app.get(
                url_for('api.node_entities_all', id_=unit_node.id))
            self.assertDictEqual(rv.get_json(), api_data.api_node_entities_all)
            rv = self.app.get(url_for(
                'api.node_entities_all',
                id_=unit_node.id,
                download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_node_entities_all)
            rv = self.app.get(
                url_for('api.node_entities_all', id_=unit_node.id, count=True))
            assert b'8' in rv.data

            # /api/0.2/subunit/
            rv = self.app.get(url_for('api.subunit', id_=place.id))
            self.assertDictEqual(rv.get_json(), api_data.api_subunit)
            rv = self.app.get(
                url_for('api.subunit', id_=place.id, download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_subunit)
            rv = self.app.get(url_for('api.subunit', id_=place.id, count=True))
            assert b'1' in rv.data

            # /api/0.2/subunit_hierarchy/
            rv = self.app.get(url_for('api.subunit_hierarchy', id_=place.id))
            self.assertDictEqual(rv.get_json(), api_data.api_subunit_hierarchy)
            rv = self.app.get(
                url_for('api.subunit_hierarchy', id_=place.id, download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_subunit_hierarchy)
            rv = self.app.get(
                url_for('api.subunit_hierarchy', id_=place.id, count=True))
            assert b'2' in rv.data

            # ---Entity---
            # /api/0.2/code/
            rv = self.app.get(url_for('api.code', code='reference'))
            print(rv.data)
            self.assertDictEqual(rv.get_json(), api_data.api_code_reference)

            rv = self.app.get(
                url_for('api.code', code='reference', format='geojson'))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_code_reference_geojson)
            rv = self.app.get(
                url_for('api.code', code='reference', download=True))
            self.assertDictEqual(rv.get_json(), api_data.api_code_reference)
            rv = self.app.get(url_for('api.code', code='place', count=True))
            assert b'3' in rv.data
            rv = self.app.get(url_for(
                'api.code',
                code='place',
                show='geometry',
                limit=2,
                sort='desc',
                first=feature.id))
            self.assertDictEqual(
                rv.get_json(), api_data.api_code_place_first_sort_show_limit)
            rv = self.app.get(url_for(
                'api.code',
                code='place',
                limit=10,
                sort='desc',
                column='name',
                filter='or|name|like|Nostromos'))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_code_place_limit_sort_column_filter)
            rv = self.app.get(url_for(
                'api.code',
                code='place',
                filter='or|id|eq|' + str(place.id)))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_code_place_filter_id)
            rv = self.app.get(url_for(
                'api.code',
                code='place',
                filter='or|begin_from|ge|2018-1-1'))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_code_place_filter_time)
            rv = self.app.get(
                url_for('api.code', code='reference', export='csv'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(
                url_for('api.entities_linked_to_entity', id_=place.id))
            self.assertDictEqual(
                rv.get_json(),
                api_data.api_entities_linked_entity)

            # Path Tests
            rv = self.app.get(url_for('api.class', class_code='E31'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(
                url_for('api.class', class_code='E31', format='geojson'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(
                url_for('api.class', class_code='E31', download=True))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(
                url_for('api.class', class_code='E18', export='csv'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api.latest', latest=10))
            assert b'Datei' in rv.data

            rv = self.app.get(url_for('api.latest', count=True, latest=2))
            assert b'2' in rv.data

            rv = self.app.get(
                url_for('api.system_class', system_class='appellation'))
            assert b'Cargo hauler' in rv.data
            rv = self.app.get(url_for(
                'api.system_class',
                system_class='appellation',
                format='geojson'))
            assert b'Cargo hauler' in rv.data

            rv = self.app.get(url_for('api.type_entities', id_=unit_node.id))
            assert b'Austria' in rv.data
            rv = self.app.get(
                url_for('api.type_entities_all', id_=unit_node.id))
            assert b'Austria' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                items='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                items='place',
                format='geojson'))
            assert b'Nostromos' in rv.data

            # Path test with download
            rv = self.app.get(
                url_for('api.entity', id_=place.id, download=True))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for('api.latest', latest=1, download=True))
            assert b'Datei' in rv.data

            rv = self.app.get(url_for(
                'api.system_class',
                system_class='appellation',
                download=True))
            assert b'Cargo hauler' in rv.data

            rv = self.app.get(
                url_for('api.query', classes='E31', download=True))
            assert b'https://openatlas.eu' in rv.data

            rv = self.app.get(url_for('api.overview_count', download=True))
            assert b'systemClass' in rv.data
            rv = self.app.get(url_for('api.class_mapping', download=True))
            assert b'systemClass' in rv.data

            # Path with export
            rv = self.app.get(url_for('api.entity', id_=place.id, export='csv'))
            assert b'Nostromos' in rv.data

            rv = self.app.get(
                url_for('api.system_class', system_class='place', export='csv'))
            assert b'Nostromos' in rv.data

            # Testing Subunit

            # Parameter: filter

            rv = self.app.get(url_for(
                'api.class',
                class_code='E18',
                filter='or|name|like|Nostr'))
            assert b'Nostromos' in rv.data

            # Parameter: last
            rv = self.app.get(
                url_for('api.class', class_code='E18', last=place.id))
            assert b'entities' in rv.data
            # Parameter: first
            rv = self.app.get(
                url_for('api.class', class_code='E18', first=place.id))
            assert b'entities' in rv.data

            # Parameter: show
            rv = self.app.get(
                url_for('api.class', class_code='E31', show='types'))
            assert b'https://openatlas.eu' in rv.data
            rv = self.app.get(
                url_for('api.class', class_code='E18', show='when'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(
                url_for('api.class', class_code='E31', show='none'))
            assert b'https://openatlas.eu' in rv.data

            # Parameter: count
            rv = self.app.get(
                url_for('api.class', class_code='E31', count=True))
            assert b'2' in rv.data

            rv = self.app.get(url_for(
                'api.system_class',
                system_class='appellation',
                count=True))
            assert b'1' in rv.data

            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='place'))
            assert b'Nostromos' in rv.data
            rv = self.app.get(url_for(
                'api.query',
                entities=place.id,
                classes='E18',
                codes='place',
                count=True))
            assert b'7' in rv.data

    @raises(EntityDoesNotExistError)
    def error_class_entity(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(
                url_for('api.class', class_code='E18', last=1231223121321))

    @raises(QueryEmptyError)
    def error_query_query(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.query'))

    @raises(InvalidSubunitError)
    def error_node_invalid(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.node_entities', id_=1234))

    @raises(InvalidSubunitError)
    def error_node_all_invalid(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.node_entities_all', id_=1234))

    @raises(InvalidCidocClassCode)
    def error_class_invalid(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.class', class_code='e99999999'))

    @raises(InvalidCodeError)
    def error_code_invalid(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.code', code='Invalid'))

    @raises(InvalidLimitError)
    def error_latest_invalid(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.latest', latest='99999999'))

    @raises(EntityDoesNotExistError)
    def error_subunit_entity(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.subunit', id_='99999999'))

    @raises(FilterOperatorError)
    def error_filter_operator_1(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.code', code='place',
                                 filter='Wrong|name|like|Nostromos'))

    @raises(FilterOperatorError)
    def error_filter_operator_2(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.code', code='place',
                                 filter='or|Wrong|like|Nostromos'))

    @raises(FilterOperatorError)
    def error_filter_operator_3(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.code', code='place',
                                 filter='or|name|Wrong|Nostromos'))

    @raises(NoSearchStringError)
    def error_filter_search(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(
                url_for('api.code', code='place', filter='or|name|Wrong|'))

    @raises(InvalidSearchDateError)
    def error_filter_date(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(url_for('api.code', code='place',
                                 filter='or|begin_from|like|WRONG'))

    @raises(InvalidSearchNumberError)
    def error_filter_date2(self) -> None:  # pragma: nocover
        with app.app_context():  # type: ignore
            self.app.get(
                url_for('api.code', code='place', filter='or|id|eq|WRONG'))
