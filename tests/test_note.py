from flask import url_for

from openatlas import app
from openatlas.models.user import User
from tests.base import TestBaseCase, insert


class NoteTest(TestBaseCase):

    def test_note(self) -> None:
        with app.app_context():
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = insert('person', 'Ripley')

            rv = self.app.get(url_for('note_insert', entity_id=actor.id))
            assert b'Description' in rv.data

            rv = self.app.post(
                url_for('note_insert', entity_id=actor.id),
                data={'description': 'A nice description'},
                follow_redirects=True)
            assert b'Note added' in rv.data

            rv = self.app.get(url_for('overview'))
            assert b'A nice description' in rv.data

            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                note_id = User.get_notes_by_user_id(self.alice_id)[0]['id']

            rv = self.app.get(url_for('note_update', id_=note_id))
            assert b'A nice description' in rv.data

            rv = self.app.post(
                url_for('note_update', id_=note_id),
                data={'description': 'A sad description', 'public': True},
                follow_redirects=True)
            assert b'Note updated' in rv.data

            rv = self.app.get(url_for('note_view', id_=note_id))
            assert b'A sad description' in rv.data

            self.login('Manager')
            rv = self.app.get(url_for('note_view', id_=note_id))
            assert b'Set private' in rv.data

            rv = self.app.get(
                url_for('note_set_private', id_=note_id),
                follow_redirects=True)
            assert b'Note updated' in rv.data

            rv = self.app.get(url_for('note_view', id_=note_id))
            assert b'403 - Forbidden' in rv.data

            self.login('Editor')
            rv = self.app.get(url_for('note_set_private', id_=note_id))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.get(url_for('note_update', id_=note_id))
            assert b'403 - Forbidden' in rv.data

            rv = self.app.get(url_for('note_delete', id_=note_id))
            assert b'403 - Forbidden' in rv.data

            self.login('Alice')
            rv = self.app.get(
                url_for('note_delete', id_=note_id),
                follow_redirects=True)
            assert b'Note deleted' in rv.data
