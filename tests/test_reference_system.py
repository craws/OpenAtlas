from flask import url_for

from openatlas import app
from openatlas.models.reference_system import ReferenceSystem
from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.get(url_for('reference_system_index'))
            assert b'GeoNames' in rv.data

            rv = self.app.get(url_for('reference_system_insert'))
            assert b'Resolver URL' in rv.data
            data = {'name': 'Wikipedia',
                    'website_url': 'https://wikipedia.org',
                    'resolver_url': 'https://wikipedia.org'}
            rv = self.app.post(url_for('reference_system_insert'), follow_redirects=True, data=data)
            assert b'An entry has been created.' in rv.data

            geonames = ReferenceSystem.get_by_name('GeoNames')
            rv = self.app.post(url_for('reference_system_update', id_=geonames.id))
            assert b'Website URL' in rv.data
            rv = self.app.post(url_for('reference_system_update', id_=geonames.id),
                               follow_redirects=True,
                               data={'name': 'GeoNames',
                                     'website_url': 'https://www.geonames2.org/',
                                     'resolver_url': 'https://www.geonames2.org/',
                                     'forms-0': 6})
            assert b'Changes have been saved.' in rv.data

            geonames = ReferenceSystem.get_by_name('GeoNames')

            rv = self.app.get(url_for('entity', id_=geonames.id), follow_redirects=True)
            assert b'GeoNames' in rv.data

            # Testing errors
            rv = self.app.post(url_for('reference_system_insert'),
                               follow_redirects=True,
                               data={'name': 'GeoNames'})
            assert b'The name is already in use.' in rv.data
            rv = self.app.get(url_for('reference_system_index', id_=geonames.id, action='delete'))
            assert b'Deletion not possible' in rv.data
            rv = self.app.get(url_for('reference_system_remove_form', system_id=geonames.id, form_id=6),
                              follow_redirects=True)
            assert b'Changes have been saved' in rv.data
