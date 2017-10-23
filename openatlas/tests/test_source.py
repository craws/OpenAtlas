# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import url_for

from openatlas import app
from openatlas.test_base import TestBaseCase


class SourceTest(TestBaseCase):

    def test_source(self):
        self.login()
        with app.app_context():
            rv = self.app.get(url_for('source_insert'))
            assert b'+ Source' in rv.data
            form_data = {'name': 'Test source'}
            rv = self.app.post(url_for('source_insert'), data=form_data)
            source_id = rv.location.split('/')[-1]
            form_data['continue_'] = 'yes'
            rv = self.app.post(url_for('source_insert'), data=form_data, follow_redirects=True)
            assert b'An entry has been created' in rv.data
            rv = self.app.get(url_for('source_index'))
            assert b'Test source' in rv.data
            rv = self.app.get(url_for('source_update', id_=source_id))
            assert b'Test source' in rv.data
            form_data['name'] = 'Test source updated'
            rv = self.app.post(
                url_for('source_update', id_=source_id),
                data=form_data,
                follow_redirects=True)
            assert b'Test source updated' in rv.data
            rv = self.app.get(url_for('translation_insert', source_id=source_id))
            assert b'+ Translation' in rv.data
            rv = self.app.post(
                url_for('translation_insert', source_id=source_id),
                data={'name': 'Test translation'})
            translation_id = rv.location.split('/')[-1]
            self.app.get(url_for('translation_update', id_=translation_id, source_id=source_id))
            rv = self.app.post(
                url_for('translation_update', id_=translation_id, source_id=source_id),
                data={'name': 'Translation updated'},
                follow_redirects=True)
            assert b'Translation updated' in rv.data
            rv = self.app.get(
                url_for('translation_delete', id_=translation_id, source_id=source_id),
                follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
            self.app.post(
                url_for('translation_insert', source_id=source_id),
                data={'name': 'Test translation continued', 'continue_': 'yes'},
                follow_redirects=True)
            rv = self.app.get(url_for('source_delete', id_=source_id), follow_redirects=True)
            assert b'The entry has been deleted.' in rv.data
