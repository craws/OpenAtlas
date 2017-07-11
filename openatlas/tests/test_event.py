# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import openatlas
from openatlas.models.entity import EntityMapper
from openatlas.test_base import TestBaseCase


class EventTest(TestBaseCase):

    def test_event(self):
        root_event = EntityMapper.get_by_codes('E7')[0]
        rv = self.app.get('/event/insert/E7')
        assert '+ Activity' in rv.data
        form_data = {'name': 'Test event', 'description': 'Event description'}
        rv = self.app.post('/event/insert/E7', data=form_data)
        event_id = rv.location.split('/')[-1]
        form_data['continue_'] = 'yes'
        rv = self.app.post('/event/insert/E8', data=form_data, follow_redirects=True)
        assert 'Entity created' in rv.data
        rv = self.app.get('/event')
        assert 'Test event' in rv.data
        rv = self.app.get('/event/update/' + event_id)
        assert 'Test event' in rv.data
        form_data['name'] = 'Test event updated'
        rv = self.app.post('/event/update/' + event_id, data=form_data, follow_redirects=True)
        assert 'Test event updated' in rv.data
        # form_data['name'] = openatlas.app.config['EVENT_ROOT_NAME']
        # self.app.post('/event/insert/E7', data=form_data, follow_redirects=True)
        rv = self.app.post('/event/update/' + str(root_event.id), data=form_data, follow_redirects=True)
        assert 'Error' in rv.data
        rv = self.app.get('/event/delete/' + str(root_event.id), data=form_data, follow_redirects=True)
        assert 'Error' in rv.data
        rv = self.app.get('/event/delete/' + event_id, follow_redirects=True)
        assert 'Entity deleted' in rv.data
