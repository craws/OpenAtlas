from typing import Any

from flask import g, url_for

from openatlas import app
from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        with app.app_context():

            rv: Any = self.app.get(
                url_for('insert', class_='reference_system'))
            assert b'Resolver URL' in rv.data

            rv = self.app.post(
                url_for('insert', class_='reference_system'),
                data={
                    'name': 'Wikipedia',
                    'website_url': 'https://wikipedia.org',
                    'resolver_url': 'https://wikipedia.org',
                    'classes': ['place']})
            wikipedia_id = rv.location.split('/')[-1]

            rv = self.app.post(
                url_for('insert', class_='reference_system'),
                data={
                    'name': 'Another system to test forms with more than 3',
                    'website_url': '',
                    'resolver_url': '',
                    'classes': ['place']},
                follow_redirects=True)
            assert b'An entry has been created' in rv.data

            rv = self.app.get(url_for('insert', class_='place'))
            assert b'reference-system-switch' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='reference_system',
                    delete_id=wikipedia_id),
                follow_redirects=True)
            assert b'Deletion not possible if classes are attached' in rv.data

            rv = self.app.get(
                url_for(
                    'reference_system_remove_class',
                    system_id=wikipedia_id,
                    class_name='place'),
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='reference_system',
                    delete_id=wikipedia_id),
                follow_redirects=True)
            assert b'The entry has been deleted' in rv.data

            rv = self.app.get(url_for('update', id_=g.geonames.id))
            assert b'Website URL' in rv.data

            data: dict[Any, Any] = {
                'name': 'GeoNames',
                self.precision_type.id: self.precision_type.subs[0],
                'website_url': 'https://www.geonames2.org/',
                'resolver_url': 'https://www.geonames2.org/',
                'placeholder': ''}
            rv = self.app.post(
                url_for('update', id_=g.geonames.id),
                data=data,
                follow_redirects=True)
            assert b'Changes have been saved.' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person'),
                data={
                    'name': 'Actor test',
                    f'reference_system_id_{g.wikidata.id}':
                        ['Q123', self.precision_type.subs[0]]})
            person_id = rv.location.split('/')[-1]

            rv = self.app.get(url_for('view', id_=g.wikidata.id))
            assert b'Actor test' in rv.data

            rv = self.app.get(url_for('view', id_=person_id))
            assert b'Wikidata' in rv.data

            rv = self.app.get(url_for('update', id_=person_id))
            assert b'Q123' in rv.data

            rv = self.app.post(
                url_for('insert', class_='reference_system'),
                data={'name': 'GeoNames'},
                follow_redirects=True)
            assert b'A transaction error occurred' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='reference_system',
                    delete_id=g.geonames.id))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.get(
                url_for(
                    'reference_system_remove_class',
                    system_id=g.wikidata.id,
                    class_name='person'),
                follow_redirects=True)
            assert b'403 - Forbidden' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person'),
                data={
                    'name': 'Test',
                    f'reference_system_id_{g.wikidata.id}':
                        ['invalid id', '']})
            assert b'Wrong id format' in rv.data

            rv = self.app.post(
                url_for('insert', class_='place'),
                data={
                    'name': 'Test',
                    f'reference_system_id_{g.geonames.id}': ['invalid id', '']})
            assert b'Wrong id format' in rv.data
