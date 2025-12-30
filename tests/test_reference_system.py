from typing import Any

from flask import g, url_for

from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        c = self.client
        rv = c.post(url_for('ajax_info_wikidata'), data={'id_': 'Q304037'})
        assert b'National Library of Austria' in rv.data

        rv = c.post(url_for('ajax_geonames_info'), data={'id_': '747712'})
        assert b'Edirne' in rv.data

        rv = c.post(url_for('ajax_gnd_info'), data={'id_': '118584596'})
        assert b'Mozart' in rv.data

        rv = c.get(url_for('insert', class_='reference_system'))
        assert b'resolver URL' in rv.data

        data: Any = {
            'name': 'Wikipedia',
            'website_url': 'https://wikipedia.org',
            'resolver_url': 'https://wikipedia.org'}
        rv = c.post(url_for('insert', class_='reference_system'), data=data)
        wikipedia_id = rv.location.split('/')[-1]

        data['reference_system_classes'] = ['place']
        rv = c.post(
            url_for('update', id_=wikipedia_id),
            data=data,
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        data['name'] = 'No name change for system classes'
        rv = c.post(
            url_for('update', id_=g.geonames.id),
            data=data,
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data and b'GeoNames' in rv.data

        rv = c.post(
            url_for('insert', class_='reference_system'),
            data={
                'name': 'Another system to test forms with more than 3',
                'website_url': '',
                'resolver_url': '',
                'reference_system_classes': ['place']},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(url_for('insert', class_='place'))
        assert b'reference-system-switch' in rv.data

        rv = c.get(
            url_for('delete', id_=wikipedia_id), follow_redirects=True)
        assert b'403 - Forbidden' in rv.data

        rv = c.get(
            url_for(
                'reference_system_remove_class',
                system_id=wikipedia_id,
                name='place'),
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.get(url_for('delete', id_=wikipedia_id), follow_redirects=True)
        assert b'The entry has been deleted' in rv.data

        rv = c.get(url_for('update', id_=g.geonames.id))
        assert b'website URL' in rv.data

        rv = c.post(
            url_for('insert', class_='person'),
            data={
                'name': 'Actor test',
                f'reference_system_id_{g.wikidata.id}':
                    ['Q123', self.precision_type.subs[0]],
                f'reference_system_id_{g.gnd.id}':
                    ['1158433263', self.precision_type.subs[0]]})
        person_id = rv.location.split('/')[-1]

        rv = c.get(url_for('view', id_=g.wikidata.id))
        assert b'Actor test' in rv.data

        rv = c.get(url_for('view', id_=person_id))
        assert b'Wikidata' in rv.data

        rv = c.get(url_for('update', id_=person_id))
        assert b'Q123' in rv.data

        rv = c.post(
            url_for('insert', class_='reference_system'),
            data={'name': 'GeoNames'},
            follow_redirects=True)
        assert b'A transaction error occurred' in rv.data

        rv = c.get(url_for('delete', id_=g.geonames.id))
        assert b'403 - Forbidden' in rv.data

        rv = c.get(
            url_for(
                'reference_system_remove_class',
                system_id=g.wikidata.id,
                name='person'),
            follow_redirects=True)
        assert b'403 - Forbidden' in rv.data

        rv = c.post(
            url_for('insert', class_='person'),
            data={
                'name': 'Test',
                'residence': '',
                'begins_in': '',
                'ends_in': '',
                f'reference_system_id_{g.wikidata.id}': ['invalid id', '']})
        assert b'Wrong id format' in rv.data

        rv = c.post(
            url_for('insert', class_='place'),
            data={
                'name': 'Test',
                f'reference_system_id_{g.geonames.id}': ['invalid id', '']})
        assert b'Wrong id format' in rv.data
