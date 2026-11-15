from http import HTTPStatus
from typing import Any

from flask import url_for
from werkzeug.exceptions import ImATeapot

from openatlas.models.entity import get_reference_system_by_name_safe
from tests.base import TestBaseCase


def assert_ajax_call(rv: Any, assert_string: str) -> None:
    if rv.status_code == HTTPStatus.OK:
        try:
            assert assert_string in rv.get_data(as_text=True)
        except AssertionError:  # pragma: no cover
            assert b'<table class="table table-no-style">' in rv.data


class ReferenceSystemTest(TestBaseCase):

    def test_reference_system(self) -> None:
        c = self.client
        c.get('/')
        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Wikidata').id),
            data={'id_': 'Q304037'})
        assert_ajax_call(rv, 'National Library of Austria')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('GeoNames').id),
            data={'id_': '747712'})
        assert_ajax_call(rv, 'Edirne')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('GND').id),
            data={'id_': '118584596'})
        assert_ajax_call(rv, 'Mozart')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Getty AAT').id),
            data={'id_': '300011798'})
        assert_ajax_call(rv, 'bone and bone components materials')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Kulturpool').id),
            data={'id_': 'dfc50104-275f-44b7-aa9f-00975528a671'})
        assert_ajax_call(rv, 'Thanatos')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('DOI').id),
            data={'id_': '10.1163/9789004712126_015'})
        assert_ajax_call(rv, 'OpenAtlas: An Open-Source Application')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('DOI').id),
            data={'id_': '10.5194/ica-proc-4-14-2021'})
        assert_ajax_call(rv, 'Beyond East and West')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('VIAF').id),
            data={'id_': '95218067'})
        assert_ajax_call(rv, 'Tolkien, J.R.R. (John Ronald Reuel), 1892-1973')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('ChronOntology').id
            ),
            data={'id_': '4qH80NOs7z4u'})
        assert_ajax_call(rv, 'El Adam phase')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('DOI').id),
            data={'id_': '10.11141/ia.64.11'})
        assert_ajax_call(rv, 'Integrating Data on Early Medieval Graves')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Cadaster').id),
            data={'id_': '01004/784/1'})
        assert_ajax_call(rv, '784/1')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('Cadaster').id),
            data={'id_': '01004/78/99'})
        assert_ajax_call(rv, 'nicht vorhanden')


        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('ROR').id),
            data={'id_': '028bsh698'})
        assert_ajax_call(rv, 'ACDH')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('ROR').id),
            data={'id_': '99999999999'})
        assert_ajax_call(rv, '"number_of_results": 0')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('ORCID').id),
            data={'id_': '0000-0001-7608-7446'})
        assert_ajax_call(rv, 'Bernhard')

        rv = c.post(
            url_for(
                'ajax_external_api',
                system_id=get_reference_system_by_name_safe('ORCID').id),
            data={'id_': '99999999999'})
        assert_ajax_call(rv, '<table class="table table-no-style">')

        rv = c.get(url_for('insert', class_='reference_system'))
        assert b'resolver URL' in rv.data

        try:
            get_reference_system_by_name_safe('non-existing')
        except ImATeapot:
            pass

        data: dict[str, str | list[str]] = {
            'name': 'OpenAtlas',
            'website_url': 'https://demo.openatlas.eu',
            'resolver_url': 'https://demo.openatlas.eu/entity/',
            'api': 'OpenAtlas'}
        rv = c.post(url_for('insert', class_='reference_system'), data=data)
        system_id = rv.location.split('/')[-1]

        rv = c.post(
            url_for('ajax_external_api', system_id=system_id),
            data={'id_': '19729'})
        assert_ajax_call(rv, 'Thunau Obere Holzwiese')

        apis_url = 'https://discworld.acdh-dev.oeaw.ac.at/'
        apis: dict[str, str | list[str]] = {
            'name': 'APIS',
            'website_url': apis_url,
            'resolver_url': f'{apis_url}/api/entity/',
            'api': 'APIS'}
        rv = c.post(url_for('insert', class_='reference_system'), data=apis)
        system_id = rv.location.split('/')[-1]

        rv = c.post(
            url_for('ajax_external_api', system_id=system_id),
            data={'id_': '12'})
        assert_ajax_call(rv, 'Carrot')

        rv = c.get(url_for('apis_proxy', system_url=apis_url, search='Carr'))

        assert_ajax_call(rv, 'Carrot')

        rv = c.get(url_for('viaf_proxy', query='Tolkien'))
        assert_ajax_call(rv, 'Tolkien')

        rv = c.get(url_for('apis_proxy', system_url='wrong', search='Carr'))
        assert_ajax_call(rv, 'error')

        rv = c.get(url_for('crossref_proxy', rows='10', query='OpenAtlas'))
        assert_ajax_call(rv, 'OpenAtlas')

        rv = c.get(url_for('crossref_proxy', rows='wrong', query='Open'))
        assert_ajax_call(rv, 'error')

        rv = c.get(url_for('ror_proxy', query='028bsh698'))
        assert_ajax_call(rv, 'ACDH')

        rv = c.get(url_for('ror_proxy', query='99999999999999999'))
        assert_ajax_call(rv, '"items": []')

        rv = c.get(url_for('orcid_proxy', query='0000-0001-7608-7446'))
        assert_ajax_call(rv, 'Bernhard')

        rv = c.get(url_for('orcid_proxy', query='99999999999999999'))
        assert_ajax_call(rv, '"items": []')

        rv = c.get(url_for('chronontology_proxy', size='10', q='Wien*'))
        assert_ajax_call(rv, 'results')

        rv = c.get(url_for('chronontology_proxy', size='wrong', q='Wien*'))
        assert_ajax_call(rv, 'error')

        data['reference_system_classes'] = ['place']

        rv = c.get(url_for('chronontology_proxy', size='10', q='Wien*'))
        assert_ajax_call(rv, 'Wien')

        rv = c.get(url_for('chronontology_proxy', size='wrong', q='Wien*'))
        assert_ajax_call(rv, 'error')

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
