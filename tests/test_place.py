from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.models.overlay import Overlay
from tests.base import TestBaseCase


class PlaceTest(TestBaseCase):

    def test_place(self) -> None:
        with app.app_context():  # type: ignore
            self.login()
            rv = self.app.get(url_for('place_insert'))
            assert b'+ Place' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                unit_node = Node.get_hierarchy('Administrative Unit')
                unit_sub1 = g.nodes[unit_node.subs[0]]
                unit_sub2 = g.nodes[unit_node.subs[1]]
                reference = Entity.insert('E31', 'https://openatlas.eu', 'external reference')
                place_node = Node.get_hierarchy('Place')
                source = Entity.insert('E33', 'Necronomicon')
            data = {'name': 'Asgard',
                    'alias-0': 'Valhöll',
                    'geonames_id': '123',
                    'geonames_precision': True,
                    unit_node.id: str([unit_sub1.id, unit_sub2.id])}
            rv = self.app.post(url_for('place_insert', origin_id=reference.id), data=data,
                               follow_redirects=True)
            assert b'Asgard' in rv.data
            data['gis_points'] = """[{
                "type":"Feature",
                "geometry":{"type":"Point","coordinates":[9,17]},
                "properties":{"name":"Valhalla","description":"","shapeType":"centerpoint"}}]"""
            data['gis_lines'] = """[{
                "type":"Feature",
                "geometry":{
                    "type":"LineString",
                    "coordinates":[[9.75307425847859,17.8111792731339],
                    [9.75315472474904,17.8110005175436],[9.75333711496205,17.8110873417098]]},
                "properties":{"name":"","description":"","shapeType":"line"}}]"""
            data['gis_polygons'] = """[{
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates":[[[9.75307425847859,17.8111792731339],
                    [9.75315472474904,17.8110005175436],[9.75333711496205,17.8110873417098],
                    [9.75307425847859,17.8111792731339]]]},
                "properties":{"name":"","description":"","shapeType":"shape"}}]"""
            data[place_node.id] = place_node.subs
            data['continue_'] = 'yes'
            rv = self.app.post(url_for('place_insert', origin_id=source.id), data=data,
                               follow_redirects=True)
            assert b'Necronomicon' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                places = Entity.get_by_system_type('place')
                place = places[0]
                place2 = places[1]
                location = place2.get_linked_entity_safe('P53')
                actor = Entity.insert('E21', 'Milla Jovovich')
                actor.link('P74', location)
            assert b'Necronomicon' in rv.data
            rv = self.app.get(url_for('place_index'))
            assert b'Asgard' in rv.data
            rv = self.app.get(url_for('place_update', id_=place.id))
            assert b'Valhalla' in rv.data
            data['continue_'] = ''
            data['alias-1'] = 'Val-hall'
            data['geonames_id'] = '321'
            rv = self.app.post(url_for('place_update', id_=place.id), data=data,
                               follow_redirects=True)
            assert b'Val-hall' in rv.data

            # Test with same GeoNames id
            rv = self.app.post(url_for('place_update', id_=place.id), data=data,
                               follow_redirects=True)
            assert b'Val-hall' in rv.data

            # Test with same GeoNames id but different precision
            data['geonames_precision'] = ''
            rv = self.app.post(url_for('place_update', id_=place.id), data=data,
                               follow_redirects=True)
            assert b'Val-hall' in rv.data

            # Test update without the previous GeoNames id
            data['geonames_id'] = ''
            rv = self.app.post(url_for('place_update', id_=place.id), data=data,
                               follow_redirects=True)
            assert b'Val-hall' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = Entity.insert('E8', 'Valhalla rising')
                event.link('P7', location)
                event.link('P24', location)
            rv = self.app.get(url_for('entity_view', id_=place2.id))
            assert rv.data and b'Valhalla rising' in rv.data

            # Test invalid geom
            data['gis_polygons'] = """[{"type": "Feature", "geometry":
                {"type": "Polygon", "coordinates": [
                [[298.9893436362036, -5.888919049309554], [299.00444983737543, -5.9138487869408545],
                 [299.00650977389887, -5.893358673645309], [298.9848804404028, -5.9070188333813585],
                 [298.9893436362036, -5.888919049309554]]]},
                "properties": {"name": "", "description": "", "shapeType": "shape"}}]"""
            rv = self.app.post(url_for('place_insert', origin_id=source.id), data=data,
                               follow_redirects=True)
            assert b'An invalid geometry was entered' in rv.data

            # Test Overlays
            path = app.config['ROOT_PATH'].joinpath('static', 'images', 'layout', 'logo.png')
            with open(path, 'rb') as img:
                rv = self.app.post(
                    url_for('file_insert', origin_id=place.id),
                    data={'name': 'X-Files', 'file': img}, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                file = Entity.get_by_system_type('file')[0]
                link_id = Link.insert(file, 'P67', place)[0]
            rv = self.app.get(url_for('overlay_insert', image_id=file.id, place_id=place.id,
                                      link_id=link_id))
            assert b'X-Files' in rv.data
            data = {'top_left_easting': 42, 'top_left_northing': 12,
                    'bottom_right_easting': 43, 'bottom_right_northing': 13}
            rv = self.app.post(url_for('overlay_insert', image_id=file.id, place_id=place.id,
                                       link_id=link_id), data=data, follow_redirects=True)
            assert b'Edit' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                overlay = Overlay.get_by_object(place)
                overlay_id = overlay[list(overlay.keys())[0]].id
            rv = self.app.get(url_for('overlay_update', id_=overlay_id, place_id=place.id,
                                      link_id=link_id))
            assert b'42' in rv.data
            rv = self.app.post(url_for('overlay_update', id_=overlay_id, place_id=place.id,
                                       link_id=link_id), data=data, follow_redirects=True)
            assert b'Changes have been saved' in rv.data
            self.app.get(url_for('overlay_remove', id_=overlay_id, place_id=place.id),
                         follow_redirects=True)

            # Add to place
            rv = self.app.get(url_for('place_add_file', id_=place.id))
            assert b'Add File' in rv.data

            rv = self.app.post(url_for('place_add_file', id_=place.id),
                               data={'checkbox_values': str([file.id])}, follow_redirects=True)
            assert b'X-Files' in rv.data

            rv = self.app.get(url_for('place_add_source', id_=place.id))
            assert b'Add Source' in rv.data
            rv = self.app.post(url_for('place_add_source', id_=place.id),
                               data={'checkbox_values': str([source.id])}, follow_redirects=True)
            assert b'Necronomicon' in rv.data

            rv = self.app.get(url_for('place_add_reference', id_=place.id))
            assert b'Add Reference' in rv.data
            rv = self.app.post(url_for('place_add_reference', id_=place.id),
                               data={'reference': reference.id, 'page': '777'},
                               follow_redirects=True)
            assert b'777' in rv.data

            # Place types
            rv = self.app.get(url_for('node_move_entities', id_=unit_sub1.id))
            assert b'Asgard' in rv.data

            # Test move entities of multiple node if link to new node exists
            rv = self.app.post(url_for('node_move_entities', id_=unit_sub1.id),
                               data={unit_node.id: unit_sub2.id, 'selection': location.id,
                                     'checkbox_values': str([location.id])},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data

            # Test move entities of multiple node if link to new node doesn't exists
            rv = self.app.post(url_for('node_move_entities', id_=unit_sub2.id),
                               data={unit_node.id: unit_sub1.id, 'selection': location.id,
                                     'checkbox_values': str([location.id])},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data

            # Subunits
            with app.app_context():  # type: ignore
                self.app.get(url_for('place_insert', origin_id=place.id))
                rv = self.app.post(url_for('place_insert', origin_id=place.id),
                                   data={'name': "It's not a bug, it's a feature!"})
                feat_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_insert', origin_id=feat_id))
                self.app.get(url_for('place_update', id_=feat_id))
                self.app.post(url_for('place_update', id_=feat_id),
                              data={'name': "It's not a bug, it's a feature!"})
                rv = self.app.post(url_for('place_insert', origin_id=feat_id),
                                   data={'name':  "I'm a stratigraphic unit"})
                stratigraphic_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_insert', origin_id=stratigraphic_id))
                self.app.get(url_for('place_update', id_=stratigraphic_id))
                self.app.post(url_for('place_update', id_=stratigraphic_id),
                              data={'name': "I'm a stratigraphic unit"})
                dimension_node_id = Node.get_hierarchy('Dimensions').subs[0]
                data = {'name': 'You never find me', str(dimension_node_id): '50'}
                rv = self.app.post(url_for('place_insert', origin_id=stratigraphic_id), data=data)
                find_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_update', id_=find_id))
                self.app.post(url_for('place_update', id_=find_id), data=data)
            rv = self.app.get(url_for('entity_view', id_=feat_id))
            assert b'not a bug' in rv.data
            rv = self.app.get(url_for('entity_view', id_=stratigraphic_id))
            assert b'a stratigraphic unit' in rv.data
            rv = self.app.get(url_for('entity_view', id_=find_id))
            assert b'You never' in rv.data
            rv = self.app.get(url_for('place_index', action='delete', id_=place.id),
                              follow_redirects=True)
            assert b'not possible if subunits' in rv.data
            rv = self.app.get(url_for('place_index', action='delete', id_=find_id),
                              follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
            rv = self.app.get(url_for('place_index', action='delete', id_=place2.id))
            assert b'The entry has been deleted.' in rv.data
