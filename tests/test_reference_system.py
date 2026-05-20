from flask import url_for

from openatlas.models.entity import get_reference_system_by_name_safe
from tests.base import TestBaseCase


class ReferenceSystemTest(TestBaseCase):
    def test_reference_system(self) -> None:
        c = self.client
        c.get('/')
        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Wikidata').id),
            data={'id_': 'Q304037'})
        assert b'National Library of Austria' in rv.data

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('GeoNames').id),
            data={'id_': '747712'})
        assert b'Edirne' in rv.data

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('GND').id),
            data={'id_': '118584596'})
        assert b'Mozart' in rv.data

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Cadaster').id),
            data={'id_': '01004/784/1'})
        assert b'784/1' in rv.data

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Cadaster').id),
            data={'id_': '01004/78/99'})
        assert b'nicht vorhanden' in rv.data

        rv = c.get(url_for('insert', class_='reference_system'))
        assert b'resolver URL' in rv.data

        data: dict[str, str | list[str]] = {
            'name': 'OpenAtlas',
            'website_url': 'https://demo.openatlas.eu',
            'resolver_url': 'https://demo.openatlas.eu/entity/',
            'api': 'OpenAtlas'}
        rv = c.post(url_for('insert', class_='reference_system'), data=data)
        system_id = rv.location.split('/')[-1]

        rv = c.post(
            url_for('ajax_external_api', system_id=system_id),
            data={'id_': '5117'})
        assert b'Albrecht' in rv.data

        data['reference_system_classes'] = ['place']
        rv = c.post(
            url_for('update', id_=system_id),
            data=data,
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        geonames = get_reference_system_by_name_safe('geonames')
        data['name'] = 'No name change for system classes'
        rv = c.post(
            url_for('update', id_=geonames.id),
            data=data,
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data and b'GeoNames' in rv.data

        rv = c.post(
            url_for('insert', class_='reference_system'),
            data={
                'name': 'Another system to test forms with more than 3',
                'website_url': '',
                'resolver_url': '',
                'reference_system_classes': ['place'],
                'api': ''},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.get(url_for('insert', class_='place'))
        assert b'reference-system-switch' in rv.data

        rv = c.get(
            url_for('delete', id_=system_id), follow_redirects=True)
        assert b'403 - Forbidden' in rv.data

        rv = c.get(
            url_for(
                'reference_system_remove_class',
                system_id=system_id,
                name='place'),
            follow_redirects=True)
        assert b'Changes have been saved' in rv.data

        rv = c.get(url_for('delete', id_=system_id), follow_redirects=True)
        assert b'The entry has been deleted' in rv.data

        rv = c.get(url_for('update', id_=geonames.id))
        assert b'website URL' in rv.data

        gnd = get_reference_system_by_name_safe('gnd')
        wikidata = get_reference_system_by_name_safe('wikidata')
        rv = c.post(
            url_for('insert', class_='person'),
            data={
                'name': 'Actor test',
                f'reference_system_id_{wikidata.id}':
                    ['Q123', self.precision_type.subs[0]],
                f'reference_system_id_{gnd.id}':
                    ['1158433263', self.precision_type.subs[0]]})
        person_id = rv.location.split('/')[-1]

        rv = c.get(url_for('view', id_=wikidata.id))
        assert b'Actor test' in rv.data

        rv = c.get(url_for('view', id_=person_id))
        assert b'Wikidata' in rv.data

        rv = c.get(url_for('update', id_=person_id))
        assert b'Q123' in rv.data

        rv = c.post(
            url_for('insert', class_='reference_system'),
            data={'name': 'GeoNames', 'api': ''},
            follow_redirects=True)
        assert b'A transaction error occurred' in rv.data

        rv = c.get(url_for('delete', id_=geonames.id))
        assert b'403 - Forbidden' in rv.data

        rv = c.get(
            url_for(
                'reference_system_remove_class',
                system_id=wikidata.id,
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
                f'reference_system_id_{wikidata.id}': ['invalid id', '']})
        assert b'Wrong id format' in rv.data

        rv = c.post(
            url_for('insert', class_='place'),
            data={
                'name': 'Test',
                f'reference_system_id_{geonames.id}': ['invalid id', '']})
        assert b'Wrong id format' in rv.data
