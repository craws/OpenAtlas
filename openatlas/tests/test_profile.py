# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas.test_base import TestBaseCase


class ProfileTests(TestBaseCase):

    def test_profile(self):
        self.login()
        rv = self.app.get('/profile')
        assert b'alice@umbrella.net' in rv.data
        rv = self.app.post('/profile', data={'language': 'en', 'table_rows': '100'}, follow_redirects=True)
        assert b'100' in rv.data
        rv = self.app.get('/profile/update')
        assert b'Newsletter' in rv.data
        form_data = {
            'name': 'Alice Abernathy',
            'email': 'alice@umbrella.net',
            'show_email': '',
            'newsletter': '',
        }
        rv = self.app.post('/profile/update', data=form_data, follow_redirects=True)
        assert b'Alice Abernathy' in rv.data
        rv = self.app.get('/profile/password')
        assert b'Old password' in rv.data
        form_data = {
            'password_old': 'test',
            'password': 'you_never_guess_this',
            'password2': 'you_never_guess_this',
        }
        rv = self.app.post('/profile/password', data=form_data, follow_redirects=True)
        assert b'Your password has been updated' in rv.data
        form_data['password2'] = 'same same, but different'
        rv = self.app.post('/profile/password', data=form_data, follow_redirects=True)
        assert b'match' in rv.data
