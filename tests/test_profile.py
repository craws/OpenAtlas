from flask import url_for

from tests.base import TestBaseCase


class ProfileTests(TestBaseCase):

    def test_profile(self) -> None:
        c = self.client
        rv = c.get(url_for('profile_settings', category='profile'))
        assert b'alice@example.com' in rv.data

        rv = c.post(
            url_for('profile_settings', category='profile'),
            data={
                'name': 'Alice Abernathy',
                'email': 'alice@umbrella.net',
                'show_email': ''},
            follow_redirects=True)
        assert b'saved' in rv.data and b'Alice Abernathy' in rv.data

        rv = c.post(
            url_for('profile_settings', category='display'),
            data={
                'language': 'en',
                'table_rows': 10,
                'map_zoom_default': 10,
                'map_zoom_max': 10},
            follow_redirects=True)
        assert b'saved' in rv.data

        rv = c.get(url_for('profile_password'))
        assert b'old password' in rv.data

        new_pass = 'you_never_guess_this'
        data = {
            'password_old': 'test',
            'password': new_pass,
            'password2': new_pass}
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'Your password has been updated' in rv.data

        data['password2'] = 'short'
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'match' in rv.data

        data['password_old'] = new_pass
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'New password is like old one' in rv.data

        data['password'] = 'short'
        rv = c.post(
            url_for('profile_password'),
            data=data,
            follow_redirects=True)
        assert b'too short' in rv.data
