# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class ContentTests(TestBaseCase):

    def test_content(self):
        rv = self.app.get('/content/view/contact')
        assert b'Edit' in rv.data
        rv = self.app.get('/content/update/contact')
        assert b'Save' in rv.data
        form_data = {'en': 'contact', 'de': 'german'}
        rv = self.app.post('/content/update/contact', data=form_data, follow_redirects=True)
        assert b'german' in rv.data
        rv = self.app.get('/content')
        assert b'Text' in rv.data
