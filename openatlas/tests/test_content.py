# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas.test_base import TestBaseCase


class ContentTestCase(TestBaseCase):

    def test_content(self):
        response = self.app.get('/content/view/contact')
        assert b'Edit' in response.data
        response = self.app.get('/content/update/contact')
        assert b'Save' in response.data
        form_data = {'en': 'contact', 'de': 'Kontakt'}
        response = self.app.post('/content/update/contact', data=form_data, follow_redirects=True)
        assert b'Kontakt' in response.data
        response = self.app.get('/content')
        assert b'Text' in response.data