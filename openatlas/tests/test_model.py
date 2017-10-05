# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from openatlas import PropertyMapper
from openatlas.models.classObject import ClassMapper
from openatlas.test_base import TestBaseCase


class ModelTests(TestBaseCase):

    def test_model(self):
        rv = self.app.get('/model')
        assert b'Browse' in rv.data
        rv = self.app.get('/model/class')
        assert b'E1' in rv.data
        rv = self.app.get('/model/class_view/' + str(ClassMapper.get_by_code('E2').id))
        assert b'E2' in rv.data
        rv = self.app.get('/model/property')
        assert b'P1' in rv.data
        rv = self.app.get('/model/property_view/' + str(PropertyMapper.get_by_code('P68').id))
        assert b'P68' in rv.data
        form_data = {
            'domain': ClassMapper.get_by_code('E1').id,
            'range': ClassMapper.get_by_code('E1').id,
            'property': PropertyMapper.get_by_code('P1').id}
        rv = self.app.post('/model', data=form_data)
        assert b'Wrong' in rv.data
