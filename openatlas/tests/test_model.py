# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from openatlas import ClassMapper, PropertyMapper
from openatlas.test_base import TestBaseCase


class ModelTests(TestBaseCase):

    def test_model(self):
        response = self.app.get('/model')
        assert 'Browse' in response.data
        response = self.app.get('/model/class')
        assert 'E1' in response.data
        response = self.app.get('/model/class_view/' + str(ClassMapper.get_by_code('E2').id))
        assert 'E2' in response.data
        response = self.app.get('/model/property')
        assert 'P1' in response.data
        response = self.app.get('/model/property_view/' + str(PropertyMapper.get_by_code('P68').id))
        assert 'P68' in response.data
        form_data = {
            'domain': ClassMapper.get_by_code('E1').id,
            'range': ClassMapper.get_by_code('E1').id,
            'property': PropertyMapper.get_by_code('P1').id
        }
        response = self.app.post('/model', data=form_data)
        assert 'Wrong' in response.data
