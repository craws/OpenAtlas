from typing import Any

from flask import url_for

from openatlas import app
from openatlas.models.reference_system import ReferenceSystem
from openatlas.models.type import Type
from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        with app.app_context():
            rv: Any = self.app.get(url_for('index', view='reference_system'))
            assert b'GeoNames' in rv.data

            geonames = ReferenceSystem.get_by_name('GeoNames')
            wikidata = ReferenceSystem.get_by_name('Wikidata')
            precision_id = \
                Type.get_hierarchy('External reference match').subs[0]
            rv = self.app.get(url_for('insert', class_='reference_system'))
            assert b'Resolver URL' in rv.data

            data: dict[Any, Any] = {
                'name': 'Wikipedia',
                'website_url': 'https://wikipedia.org',
                'resolver_url': 'https://wikipedia.org',
                'classes': ['place']}
            rv = self.app.post(
                url_for('insert', class_='reference_system'),
                data=data,
                follow_redirects=True)
            assert b'An entry has been created.' in rv.data

            wikipedia_id = ReferenceSystem.get_by_name('Wikipedia').id
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

            rv = self.app.get(url_for('update', id_=geonames.id))
            assert b'Website URL' in rv.data

            data = {
                'name': 'GeoNames',
                Type.get_hierarchy('External reference match').id:
                    precision_id,
                'website_url': 'https://www.geonames2.org/',
                'resolver_url': 'https://www.geonames2.org/',
                'placeholder': ''}
            rv = self.app.post(
                url_for('update', id_=geonames.id),
                follow_redirects=True, data=data)
            assert b'Changes have been saved.' in rv.data

            rv = self.app.post(
                url_for('update', id_=geonames.id),
                follow_redirects=True,
                data=data)
            assert b'https://www.geonames2.org/' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person'),
                data={
                    'name': 'Actor test',
                    f'reference_system_id_{wikidata.id}': 'Q123',
                    self.precision_geonames: '',
                    self.precision_wikidata: precision_id})
            person_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('view', id_=wikidata.id))
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
                    delete_id=geonames.id))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person'),
                data={
                    'name': 'Actor with Wikidata but without precision',
                    f'reference_system_id_{wikidata.id}': 'Q123',
                    self.precision_geonames: '',
                    self.precision_wikidata: ''})
            assert b'required' in rv.data

            rv = self.app.post(
                url_for('insert', class_='person'),
                data={
                    'name': 'Actor with invalid Wikidata id',
                    f'reference_system_id_{wikidata.id}': 'invalid id',
                    self.precision_geonames: '',
                    self.precision_wikidata: precision_id})
            assert b'Wrong id format' in rv.data

            rv = self.app.post(
                url_for('insert', class_='place'),
                data={
                    'name': 'Reference test',
                    f'reference_system_id_{geonames.id}': 'invalid id',
                    self.precision_geonames: '',
                    self.precision_wikidata: ''})
            assert b'Wrong id format' in rv.data

            rv = self.app.get(
                url_for(
                    'reference_system_remove_class',
                    system_id=geonames.id,
                    class_name='place'),
                follow_redirects=True)
            assert b'Changes have been saved' in rv.data

            rv = self.app.get(
                url_for(
                    'index',
                    view='reference_system',
                    delete_id=geonames.id))
            assert b'403 - Forbidden' in rv.data
