from flask import g, url_for

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.test_base import TestBaseCase


class PlaceTest(TestBaseCase):

    def test_place(self):
        with app.app_context():
            self.login()
            rv = self.app.get(url_for('place_insert'))
            assert b'+ Place' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                unit_node = NodeMapper.get_hierarchy_by_name('Administrative Unit')
                unit_sub1 = g.nodes[unit_node.subs[0]]
                unit_sub2 = g.nodes[unit_node.subs[1]]
                reference_id = EntityMapper.insert('E31', 'Ancient Books', 'edition').id
                place_node = NodeMapper.get_hierarchy_by_name('Place')
                source_id = EntityMapper.insert('E33', 'Tha source').id
            data = {'name': 'Asgard', 'alias-0': 'Valhöll',
                    unit_node.id: '[' + str(unit_sub1.id) + ',' + str(unit_sub2.id) + ']'}
            rv = self.app.post(url_for('place_insert', origin_id=reference_id), data=data,
                               follow_redirects=True)
            assert b'Asgard' in rv.data
            gis_points = """[{"type":"Feature", "geometry":{"type":"Point", "coordinates":[9,17]},
                    "properties":{"name":"Valhalla","description":"","shapeType":"centerpoint"}}]"""
            data['gis_points'] = gis_points
            gis_polygons = """[{"geometry":{
                "coordinates":[[[9.75307425847859,17.8111792731339],
                [9.75315472474904,17.8110005175436],[9.75333711496205,17.8110873417098],
                [9.75307425847859,17.8111792731339]]],"type":"Polygon"},
                "properties":{"count":4,"description":"","id":8,"name":"",
                "objectDescription":"","objectId":185,"shapeType":"Shape",
                "siteType":"Settlement","title":""},"type":"Feature"}]"""
            data['gis_polygons'] = gis_polygons
            data[place_node.id] = place_node.subs
            data['continue_'] = 'yes'
            rv = self.app.post(
                url_for('place_insert', origin_id=source_id), data=data, follow_redirects=True)
            assert b'Tha source' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                places = EntityMapper.get_by_codes('place')
                place_id = places[0].id
                place2_id = places[1].id
                location = LinkMapper.get_linked_entity(place2_id, 'P53')
                actor = EntityMapper.insert('E21', 'Milla Jovovich')
                actor.link('P74', location)
            assert b'Tha source' in rv.data
            rv = self.app.get(url_for('place_index'))
            assert b'Asgard' in rv.data
            rv = self.app.get(url_for('place_update', id_=place_id))
            assert b'Valhalla' in rv.data
            data['continue_'] = ''
            data['alias-1'] = 'Val-hall'
            rv = self.app.post(
                url_for('place_update', id_=place_id), data=data, follow_redirects=True)
            assert b'Val-hall' in rv.data
            with app.test_request_context():
                app.preprocess_request()
                event = EntityMapper.insert('E8', 'Valhalla rising')
                event.link('P7', location)
                event.link('P24', location)
            rv = self.app.get(
                url_for('place_view', id_=place2_id, unlink_id=place_id), follow_redirects=True)
            assert b'Link removed' in rv.data and b'Milla Jovovich' in rv.data

            # Place types
            rv = self.app.get(url_for('node_move_entities', id_=unit_sub1.id))
            assert b'Asgard' in rv.data
            # Test move entities of multiple node if link to new node exists
            rv = self.app.post(url_for('node_move_entities', id_=unit_sub1.id),
                               data={unit_node.id: unit_sub2.id, 'selection': location.id},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data
            # Test move entities of multiple node if link to new node doesn't exists
            rv = self.app.post(url_for('node_move_entities', id_=unit_sub2.id),
                               data={unit_node.id: unit_sub1.id, 'selection': location.id},
                               follow_redirects=True)
            assert b'Entities where updated' in rv.data

            # Subunits
            with app.app_context():
                self.app.get(url_for('place_insert', origin_id=place_id))
                name = "It's not a bug, it's a feature!"
                rv = self.app.post(url_for('place_insert', origin_id=place_id), data={'name': name})
                feat_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_insert', origin_id=feat_id))
                self.app.get(url_for('place_update', id_=feat_id))
                self.app.post(url_for('place_update', id_=feat_id), data={'name': name})
                name = "I'm a stratigraphic unit"
                rv = self.app.post(url_for('place_insert', origin_id=feat_id), data={'name': name})
                stratigraphic_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_insert', origin_id=stratigraphic_id))
                self.app.get(url_for('place_update', id_=stratigraphic_id))
                self.app.post(url_for('place_update', id_=stratigraphic_id), data={'name': name})
                dimension_node_id = NodeMapper.get_hierarchy_by_name('Dimensions').subs[0]
                data = {'name': 'You never find me', str(dimension_node_id): '50'}
                rv = self.app.post(url_for('place_insert', origin_id=stratigraphic_id), data=data)
                find_id = rv.location.split('/')[-1]
                self.app.get(url_for('place_update', id_=find_id))
                self.app.post(url_for('place_update', id_=find_id), data=data)
            rv = self.app.get(url_for('place_view', id_=feat_id))
            assert b'not a bug' in rv.data
            rv = self.app.get(url_for('place_view', id_=stratigraphic_id))
            assert b'a stratigraphic unit' in rv.data
            rv = self.app.get(url_for('place_view', id_=find_id))
            assert b'You never' in rv.data
            rv = self.app.get(url_for('place_delete', id_=place_id), follow_redirects=True)
            assert b'not possible if subunits' in rv.data
            rv = self.app.get(url_for('place_delete', id_=find_id), follow_redirects=True)

            assert b'The entry has been deleted.' in rv.data
