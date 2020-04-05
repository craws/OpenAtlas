from flask import url_for

from openatlas import app
from openatlas.models.entity import Entity
from tests.base import TestBaseCase


class NoteTest(TestBaseCase):

    def test_note(self) -> None:
        with app.app_context():  # type: ignore
            with app.test_request_context():
                app.preprocess_request()  # type: ignore
                actor = Entity.insert('E21', 'Ripley')
            rv = self.app.get(url_for('note_insert', entity_id=actor.id))
            assert b'Note *' in rv.data
            rv = self.app.post(url_for('note_insert', entity_id=actor.id),
                               data={'description': 'A nice description'},
                               follow_redirects=True)
            assert b'Note added' in rv.data
            rv = self.app.get(url_for('index'))
            assert b'A nice description' in rv.data
            rv = self.app.get(url_for('note_update', entity_id=actor.id))
            assert b'A nice description' in rv.data
            rv = self.app.post(url_for('note_update', entity_id=actor.id),
                               data={'description': 'A very nice description'},
                               follow_redirects=True)
            assert b'Note updated' in rv.data
            rv = self.app.get(url_for('note_delete', entity_id=actor.id), follow_redirects=True)
            assert b'Note deleted' in rv.data
