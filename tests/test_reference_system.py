from flask import url_for

from openatlas import app
from openatlas.models.node import Node
from openatlas.models.reference_system import ReferenceSystem
from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        with app.app_context():  # type: ignore
            rv = self.app.get(url_for('reference_system_index'))
            assert b'GeoNames' in rv.data
            geonames = ReferenceSystem.get_by_name('GeoNames')
            wikidata = ReferenceSystem.get_by_name('Wikidata')
            precision_id = Node.get_hierarchy('External Reference Match').subs[0]

            rv = self.app.get(url_for('reference_system_insert'))
            assert b'Resolver URL' in rv.data
            data = {'name': 'Wikipedia',
                    'website_url': 'https://wikipedia.org',
                    'resolver_url': 'https://wikipedia.org',
                    'forms': [geonames.forms[0]]}
            rv = self.app.post(url_for('reference_system_insert'), follow_redirects=True, data=data)
            assert b'An entry has been created.' in rv.data
            wikipedia_id = ReferenceSystem.get_by_name('Wikipedia').id
            rv = self.app.get(url_for('reference_system_remove_form',
                                      system_id=wikipedia_id,
                                      form_id=geonames.forms[0]),
                              follow_redirects=True)
            assert b'Changes have been saved' in rv.data
            rv = self.app.get(url_for('reference_system_index', id_=wikipedia_id, action='delete'))
            assert b'The entry has been deleted' in rv.data

            rv = self.app.post(url_for('reference_system_update', id_=geonames.id))
            assert b'Website URL' in rv.data
            rv = self.app.post(url_for('reference_system_update', id_=geonames.id),
                               follow_redirects=True,
                               data={'name': 'GeoNames',
                                     Node.get_hierarchy('External Reference Match').id:
                                         precision_id,
                                     'website_url': 'https://www.geonames2.org/',
                                     'resolver_url': 'https://www.geonames2.org/'})
            assert b'Changes have been saved.' in rv.data

            rv = self.app.post(url_for('actor_insert', code='E21'), data={
                'name': 'Actor test',
                'reference_system_id_' + str(wikidata.id): 'Q123',
                self.precision_geonames: '',
                self.precision_wikidata: precision_id})
            person_id = rv.location.split('/')[-1]
            rv = self.app.get(url_for('entity_view', id_=wikidata.id), follow_redirects=True)
            assert b'Actor test' in rv.data
            rv = self.app.get(url_for('entity_view', id_=person_id), follow_redirects=True)
            assert b'Wikidata' in rv.data
            rv = self.app.get(url_for('actor_update', id_=person_id))
            assert b'Q123' in rv.data

            # Testing errors
            rv = self.app.post(url_for('reference_system_insert'),
                               follow_redirects=True,
                               data={'name': 'GeoNames'})
            assert b'The name is already in use.' in rv.data
            rv = self.app.get(url_for('reference_system_index', id_=geonames.id, action='delete'))
            assert b'Deletion not possible' in rv.data
            rv = self.app.post(url_for('actor_insert', code='E21'), data={
                'name': 'Actor with Wikidata but without precision',
                'reference_system_id_' + str(wikidata.id): 'Q123',
                self.precision_geonames: '',
                self.precision_wikidata: ''})
            assert b'required' in rv.data
            rv = self.app.post(url_for('actor_insert', code='E21'), data={
                'name': 'Actor with invalid Wikidata id',
                'reference_system_id_' + str(wikidata.id): 'invalid id',
                self.precision_geonames: '',
                self.precision_wikidata: precision_id})
            assert b'Wrong id format' in rv.data
            rv = self.app.post(url_for('place_insert'),
                               data={'name': 'Reference test',
                                     'reference_system_id_' + str(geonames.id): 'invalid id',
                                     self.precision_geonames: '',
                                     self.precision_wikidata: ''})
            assert b'Wrong id format' in rv.data
            rv = self.app.get(url_for('reference_system_remove_form',
                                      system_id=geonames.id,
                                      form_id=geonames.forms[0]),
                              follow_redirects=True)
            assert b'Changes have been saved' in rv.data
            rv = self.app.get(url_for('reference_system_index', id_=geonames.id, action='delete'))
            assert b'403 - Forbidden' in rv.data
