# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class IndexTests(TestBaseCase):

    def test_index(self):
        rv = self.app.get('/')
        assert b'Overview' in rv.data
        rv = self.app.get('/some_missing_site')
        assert b'404' in rv.data
        rv = self.app.get('/index/changelog')
        assert b'Version' in rv.data
        rv = self.app.get('/index/contact')
        assert b'Contact' in rv.data
        rv = self.app.get('/index/credits')
        assert b'Stefan Eichert' in rv.data
        self.app.get('/index/setlocale/en')
        rv = self.app.get('/login')
        assert b'Password' in rv.data
        rv = self.app.post('/login', data={'username': 'Never', 'password': 'wrong'})
        assert b'No user with this name found' in rv.data
        rv = self.app.post('/login', data={'username': 'Alice', 'password': 'wrong'})
        assert b'Wrong Password' in rv.data
        rv = self.app.post('/login', data={'username': 'inactive', 'password': 'test'})
        assert b'This user is not activated' in rv.data
        for i in range(4):
            rv = self.app.post('/login', data={'username': 'inactive', 'password': 'wrong'})
        assert b'Too many login attempts' in rv.data
        self.login()
        rv = self.app.get('/')
        assert b'0' in rv.data
        rv = self.app.get('/index/setlocale/de', follow_redirects=True)
        assert b'Quelle' in rv.data
        rv = self.app.get('/logout', follow_redirects=True)
        assert b'Password' in rv.data
        rv = self.app.get('/404')
        assert b'404' in rv.data
