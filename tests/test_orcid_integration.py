from types import SimpleNamespace
from unittest.mock import patch

from flask import g
from wtforms import Form

from openatlas import app
from openatlas.forms.field import ReferenceField
from openatlas.views.ajax import orcid_proxy


def test_orcid_autocomplete_configuration() -> None:
    with app.test_request_context(), patch.dict(app.config, {
            'ORCID_CLIENT_ID': '', 'ORCID_CLIENT_SECRET': ''}):
        g.reference_systems = {1: SimpleNamespace(id=1, api='ORCID')}
        form = Form()
        field = ReferenceField(
            'ORCID', reference_system_id=1, _form=form, name='orcid')
        assert not getattr(field, 'reference_system_js', None)

        app.config['ORCID_CLIENT_ID'] = 'client'
        assert not getattr(
            ReferenceField(
                'ORCID', reference_system_id=1, _form=form, name='orcid'),
            'reference_system_js', None)
        app.config['ORCID_CLIENT_SECRET'] = 'secret'
        script = ReferenceField(
            'ORCID', reference_system_id=1, _form=form, name='orcid')
        assert '/proxy/orcid' in script.reference_system_js
        assert 'https://orcid.org/' in script.reference_system_js


def test_orcid_proxy() -> None:
    results = [{'id': '0000-0002-1825-0097', 'label': 'Jane Doe'}]
    with app.test_request_context('/proxy/orcid?query=Jane'), patch(
            'openatlas.views.ajax.search_orcid', return_value=results) as search:
        response = orcid_proxy.__wrapped__()
        assert response.get_json() == results
        search.assert_called_once_with('Jane')