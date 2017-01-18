from openatlas.test_base import TestBaseCase


class IndexTestCase(TestBaseCase):

    def test_index(self):
        response = self.app.get('/')
        assert b'Overview' in response.data
        # response = self.app.get('/some_missing_site')
        # assert b'404' in response.data
        response = self.app.get('/index/changelog')
        assert b'Changelog' in response.data
