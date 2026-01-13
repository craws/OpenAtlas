from flask import g, url_for
from flask_login import current_user

from openatlas import app
from tests.base import TestBaseCase, insert


class UserTests(TestBaseCase):
    def test_user(self) -> None:
        c = self.client
        data = {
            'active': '',
            'username': 'Ripley',
            'email': 'ripley@nostromo.org',
            'password': 'you_never_guess_this',
            'password2': 'you_never_guess_this',
            'group': 'admin',
            'name': 'Ripley Weaver',
            'real_name': '',
            'description': ''}
        rv = c.post(url_for('user_insert'), data=data)
        user_id = rv.location.split('/')[-1]

        data['password'] = 'too short'
        rv = c.post(url_for('user_insert'), data=data)
        assert b'match' in rv.data

        rv = c.post(
            url_for('user_insert'),
            data={
                'active': '',
                'username': 'Newt',
                'email': 'newt@nostromo.org',
                'password': 'you_never_guess_this',
                'password2': 'you_never_guess_this',
                'group': 'admin',
                'name': 'Newt',
                'continue_': 'yes',
                'real_name': '',
                'description': ''},
            follow_redirects=True)
        assert b'Newt' not in rv.data

        rv = c.get(url_for('user_view', id_=666))
        assert b'404' in rv.data

        rv = c.get(url_for('user_update', id_=self.alice_id))
        assert b'Alice' in rv.data

        data['description'] = 'The warrant officer'
        rv = c.post(
            url_for('user_update', id_=user_id),
            data=data,
            follow_redirects=True)
        assert b'The warrant officer' in rv.data

        rv = c.post(url_for('user_update', id_=1234), data=data)
        assert b'404' in rv.data

        rv = c.get(url_for('user_delete', id_=user_id), follow_redirects=True)
        assert b'User deleted' in rv.data

        rv = c.post(
            url_for('insert', class_='bibliography'),
            data={'name': 'test', 'description': 'test'},
            follow_redirects=True)
        assert b'An entry has been created' in rv.data

        rv = c.post(
            url_for('user_activity', user_id=user_id),
            data={'limit': 100, 'user': 0, 'action': 'all'})
        assert b'Activity' in rv.data

        rv = c.get(url_for('user_delete', id_=self.alice_id))
        assert b'403 - Forbidden' in rv.data

        with app.test_request_context():
            app.preprocess_request()
            person = insert('person', 'Hugo')
            insert('activity', 'Event Horizon').link('P11', person)

        rv = c.post(url_for('ajax_bookmark'), data={'entity_id': person.id})
        assert b'Remove bookmark' in rv.data

        with app.test_request_context():
            current_user.bookmarks = [person.id]

        rv = c.get('/')
        assert b'Hugo' in rv.data

        rv = c.post(url_for('ajax_bookmark'), data={'entity_id': person.id})
        assert b'Bookmark' in rv.data

        c.get(url_for('logout'))

        rv = c.get(url_for('user_activity'), follow_redirects=True)
        assert b'Login' in rv.data

        rv = c.get(url_for('user_insert'), follow_redirects=True)
        assert b'Forgot your password?' not in rv.data

        c.post(
            url_for('login'),
            data={'username': 'Editor', 'password': 'test'})
        rv = c.get(url_for('user_delete', id_=person.id))
        assert b'403 - Forbidden' in rv.data

        rv = c.post(url_for('insert', class_='reference_system'))
        assert b'403 - Forbidden' in rv.data

        rv = c.get(url_for('delete', id_=g.wikidata.id))
        assert b'403 - Forbidden' in rv.data

        c.get(url_for('logout'))
        c.post(
            url_for('login'),
            data={'username': 'Manager', 'password': 'test'})
        rv = c.get(url_for('settings', category='mail'))
        assert b'403 - Forbidden' in rv.data

        rv = c.get(url_for('user_update', id_=self.alice_id))
        assert b'403 - Forbidden' in rv.data

        c.get(url_for('logout'))
        c.post(
            url_for('login'),
            data={'username': 'Contributor', 'password': 'test'})
        rv = c.get(url_for('delete', id_=person.id))
        assert b'403 - Forbidden' in rv.data

        rv = c.get(url_for('update', id_=person.id))
        assert b'Hugo' in rv.data

        rv = c.get(url_for('view', id_=person.id))
        assert b'Hugo' in rv.data

        c.get(url_for('logout'))
        c.post(
            url_for('login'),
            data={'username': 'Readonly', 'password': 'test'})
        rv = c.get(url_for('view', id_=person.id))
        assert b'Hugo' in rv.data
