import pathlib
from typing import Any

from flask import g, url_for

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.overlay import Overlay
from openatlas.models.type import Type
from tests.base import TestBaseCase


class PlaceTest(TestBaseCase):

    def test_place(self) -> None:
        with app.app_context():
            rv: Any = self.app.get(url_for('insert', class_='place'))
            assert b'+ Place' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                unit_type = Type.get_hierarchy('Administrative unit')
                unit_sub1 = g.types[unit_type.subs[0]]
                unit_sub2 = g.types[unit_type.subs[1]]
                human_remains_type = Type.get_hierarchy('Human remains')
                human_remains_type_sub = g.types[human_remains_type.subs[0]]
                reference = Entity.insert(
                    'external_reference',
                    'https://openatlas.eu')
                place_type = Type.get_hierarchy('Place')
                source = Entity.insert('source', 'Necronomicon')
            data = {
                'name': 'Asgard',
                'alias-0': 'Valhöll',
                unit_type.id: str([unit_sub1.id, unit_sub2.id]),
                self.geonames: ['123456', self.precision_type.subs[0]]
            }
            rv = self.app.post(
                url_for('insert', class_='place', origin_id=reference.id),
                data=data,
                follow_redirects=True)
            assert b'Asgard' in rv.data and b'An entry has been' in rv.data
            rv = self.app.get(url_for('view', id_=self.precision_type.subs[0]))
            assert b'Asgard' in rv.data

            rv = self.app.get(
                url_for('view', id_=g.reference_system_geonames.id))
            assert b'Asgard' in rv.data

            data['gis_points'] = """[{
                "type": "Feature",
                "geometry": {"type":"Point","coordinates":[9,17]},
                "properties": {
                    "name": "Valhalla",
                    "description": "",
                    "shapeType": "centerpoint"}}]"""
            data['gis_lines'] = """[{
                "type": "Feature",
                "geometry":{
                    "type": "LineString",
                    "coordinates": [
                        [9.75307425847859,17.8111792731339],
                        [9.75315472474904,17.8110005175436],
                        [9.75333711496205,17.8110873417098]]},
                "properties": {
                    "name": "",
                    "description": "",
                    "shapeType": "line"}}]"""
            data['gis_polygons'] = """[{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [9.75307425847859,17.8111792731339],
                        [9.75315472474904,17.8110005175436],
                        [9.75333711496205,17.8110873417098],
                        [9.75307425847859,17.8111792731339]]]},
                "properties":{
                    "name": "",
                    "description": "",
                    "shapeType": "shape"}}]"""
            data[place_type.id] = place_type.subs
            rv = self.app.post(
                url_for('insert', class_='place', origin_id=source.id),
                data=data,
                follow_redirects=True)
            assert b'Necronomicon' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                places = Entity.get_by_class('place')
                place = places[0]
                place2 = places[1]
                location = place2.get_linked_entity_safe('P53')
                actor = Entity.insert('person', 'Milla Jovovich')
                actor.link('P74', location)
            assert b'Necronomicon' in rv.data

            rv = self.app.get(url_for('index', view='place'))
            assert b'Asgard' in rv.data

            rv = self.app.get(url_for('update', id_=place.id))
            assert b'Valhalla' in rv.data

            data['continue_'] = ''
            data['alias-1'] = 'Val-hall'
            data['geonames_id'] = '321'
            rv = self.app.post(
                url_for('update', id_=place.id),
                data=data,
                follow_redirects=True)
            assert b'Val-hall' in rv.data

            rv = self.app.get(url_for('view', id_=place.id+1))
            assert b'be viewed directly' in rv.data

            rv = self.app.post(
                url_for('update', id_=place.id),
                data=data,
                follow_redirects=True)
            assert b'Val-hall' in rv.data

            data['geonames_precision'] = ''
            rv = self.app.post(
                url_for('update', id_=place.id),
                data=data,
                follow_redirects=True)
            assert b'Val-hall' in rv.data

            data['geonames_id'] = ''
            rv = self.app.post(
                url_for('update', id_=place.id),
                data=data,
                follow_redirects=True)
            assert b'Val-hall' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                event = Entity.insert('acquisition', 'Valhalla rising')
                event.link('P7', location)
            rv = self.app.get(url_for('view', id_=place2.id))
            assert rv.data and b'Valhalla rising' in rv.data

            data['gis_polygons'] = """[{
                "type": "Feature", 
                "geometry": {
                    "type": "Polygon", 
                    "coordinates": [[
                        [298.9893436362036, -5.888919049309554], 
                        [299.00444983737543, -5.9138487869408545],
                        [299.00650977389887, -5.893358673645309], 
                        [298.9848804404028, -5.9070188333813585],
                        [298.9893436362036, -5.888919049309554]]]},
                "properties": {
                "name": "", 
                "description": "", 
                "shapeType": "shape"}}]"""
            rv = self.app.post(
                url_for('update', id_=place.id),
                data=data,
                follow_redirects=True)
            assert b'An invalid geometry was entered' in rv.data

            path = pathlib.Path(app.root_path) \
                / 'static' / 'images' / 'layout' / 'logo.png'
            with open(path, 'rb') as img:
                rv = self.app.post(
                    url_for('insert', class_='file', origin_id=place.id),
                    data={'name': 'X-Files', 'file': img},
                    follow_redirects=True)
            assert b'An entry has been created' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                file = Entity.get_by_class('file')[0]
                link_id = Link.insert(file, 'P67', place)[0]

            rv = self.app.get(
                url_for(
                    'overlay_insert',
                    image_id=file.id,
                    place_id=place.id,
                    link_id=link_id))
            assert b'X-Files' in rv.data

            data = {
                'top_left_easting': 42,
                'top_left_northing': 12,
                'top_right_easting': 43,
                'top_right_northing': 13,
                'bottom_left_easting': 10,
                'bottom_left_northing': 20}
            rv = self.app.post(
                url_for(
                    'overlay_insert',
                    image_id=file.id,
                    place_id=place.id,
                    link_id=link_id),
                data=data,
                follow_redirects=True)
            assert b'Edit' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                overlay = Overlay.get_by_object(place)
                overlay_id = overlay[list(overlay.keys())[0]].id
            rv = self.app.get(
                url_for(
                    'overlay_update',
                    id_=overlay_id,
                    place_id=place.id,
                    link_id=link_id))
            assert b'42' in rv.data

            rv = self.app.post(
                url_for(
                    'overlay_update',
                    id_=overlay_id,
                    place_id=place.id,
                    link_id=link_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            self.app.get(
                url_for(
                    'overlay_remove',
                    id_=overlay_id,
                    place_id=place.id),
                follow_redirects=True)

            rv = self.app.get(url_for('entity_add_file', id_=place.id))
            assert b'Link file' in rv.data

            rv = self.app.post(
                url_for('entity_add_file', id_=place.id),
                data={'checkbox_values': str([file.id])},
                follow_redirects=True)
            assert b'X-Files' in rv.data

            rv = self.app.get(
                url_for('reference_add', id_=reference.id, view='place'))
            assert b'Val-hall' in rv.data

            rv = self.app.get(url_for('entity_add_reference', id_=place.id))
            assert b'Link reference' in rv.data

            rv = self.app.post(
                url_for('entity_add_reference', id_=place.id),
                data={'reference': reference.id, 'page': '777'},
                follow_redirects=True)
            assert b'777' in rv.data

            rv = self.app.get(url_for('type_move_entities', id_=unit_sub1.id))
            assert b'Asgard' in rv.data

            # Test move entities of multiple type if link to new type exists
            rv = self.app.post(
                url_for('type_move_entities', id_=unit_sub1.id),
                follow_redirects=True,
                data={
                    unit_type.id: unit_sub2.id,
                    'selection': location.id,
                    'checkbox_values': str([location.id])})
            assert b'Entities were updated' in rv.data

            # Test move entities of multiple type
            rv = self.app.post(
                url_for('type_move_entities', id_=unit_sub2.id),
                follow_redirects=True,
                data={
                    unit_type.id: unit_sub1.id,
                    'selection': location.id,
                    'checkbox_values': str([location.id])})
            assert b'Entities were updated' in rv.data

            # Subunits
            data = {
                'name': "Try continue",
                'continue_': 'sub'}
            rv = self.app.post(
                url_for('insert', class_='place'),
                data=data,
                follow_redirects=True)
            assert b'Insert and add strati' in rv.data

            data['name'] = "It's not a bug, it's a feature!"
            data['place'] = place.id
            rv = self.app.post(
                url_for('insert', class_='feature', origin_id=place.id),
                data=data)
            feat_id = rv.location.split('/')[-1]

            self.app.get(url_for('insert', class_='place', origin_id=feat_id))
            self.app.get(url_for('update', id_=feat_id))
            self.app.post(url_for('update', id_=feat_id), data=data)

            rv = self.app.get(
                url_for(
                    'insert',
                    class_='stratigraphic_unit',
                    origin_id=feat_id),
                data=data)
            assert b'Insert and add human remains' in rv.data

            data['name'] = "I'm a stratigraphic unit"
            data['place'] = feat_id
            rv = self.app.post(
                url_for(
                    'insert',
                    class_='stratigraphic_unit',
                    origin_id=feat_id),
                data=data)
            strati_id = rv.location.split('/')[-1]

            self.app.get(url_for('update', id_=strati_id))
            self.app.post(
                url_for('update', id_=strati_id),
                data={'name': "I'm a stratigraphic unit", 'place': feat_id})
            rv = self.app.get(
                url_for(
                    'insert',
                    class_='human_remains',
                    origin_id=strati_id))
            assert b"I'm a stratigraphic unit" in rv.data

            data = {
                'name': 'You never find me',
                'artifact_super': strati_id,
                Type.get_hierarchy('Dimensions').subs[0]: 50}
            rv = self.app.post(
                url_for('insert', class_='artifact', origin_id=strati_id),
                data=data)
            find_id = rv.location.split('/')[-1]

            rv = self.app.post(
                url_for('update', id_=find_id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            # Create a second artifact to test siblings pager
            rv = self.app.post(
                url_for('insert', class_='artifact', origin_id=strati_id),
                follow_redirects=True,
                data=data)
            assert b'An entry has been created' in rv.data

            self.app.get(url_for('update', id_=find_id))
            data = {
                'name': 'My human remains',
                'actor': actor.id,
                'human_remains_super': strati_id,
                human_remains_type.id: str([human_remains_type_sub.id])
            }
            rv = self.app.post(
                url_for('insert', class_='human_remains', origin_id=strati_id),
                data=data)
            human_remains_id = rv.location.split('/')[-1]

            rv = self.app.get(
                url_for('insert', class_='human_remains', origin_id=strati_id))
            assert b'exists' in rv.data

            rv = self.app.get(url_for('view', id_=human_remains_id))
            assert b'My human remains' in rv.data

            rv = self.app.get(url_for('update', id_=human_remains_id))
            assert b'My human remains' in rv.data

            rv = self.app.get('/')
            assert b'My human remains' in rv.data

            rv = self.app.get(url_for('view', id_=human_remains_type_sub.id))
            assert b'My human remains' in rv.data

            rv = self.app.get(
                url_for('index', view='artifact', delete_id=human_remains_id),
                follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data

            # Anthropological features
            rv = self.app.get(url_for('anthropology_index', id_=strati_id))
            assert b'Sex estimation' in rv.data

            rv = self.app.get(url_for('sex', id_=strati_id))
            assert b'Anthropological analyses' in rv.data

            rv = self.app.post(
                url_for('sex_update', id_=strati_id),
                follow_redirects=True,
                data={'Glabella': 'Female'})
            assert b'-2.0' in rv.data

            rv = self.app.post(
                url_for('sex_update', id_=strati_id),
                data={'Glabella': 'Female'},
                follow_redirects=True)
            assert b'-2.0' in rv.data

            rv = self.app.get(url_for('sex_update', id_=strati_id))
            assert b'Glabella' in rv.data

            rv = self.app.post(
                url_for('update', id_=strati_id),
                data={'name': 'New name'},
                follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            rv = self.app.get(url_for('view', id_=feat_id))
            assert b'not a bug' in rv.data

            rv = self.app.get(url_for('view', id_=find_id))
            assert b'You never' in rv.data

            rv = self.app.get(
                url_for('index', view='place', delete_id=place.id),
                follow_redirects=True)
            assert b'not possible if subunits' in rv.data

            rv = self.app.get(
                url_for('index', view='place', delete_id=find_id),
                follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data

            rv = self.app.get(
                url_for('index', view='place', delete_id=place2.id))
            assert b'The entry has been deleted.' in rv.data
