# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from openatlas import app
from openatlas.models.classObject import ClassMapper
from openatlas.models.property import PropertyMapper
from openatlas.util.util import link


@app.route('/model')
def model_index():
    return render_template('model/index.html')


@app.route('/model/class')
def model_class():
    classes = ClassMapper.get_all()
    table = {
        'name': 'classes',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
    }
    for class_id, class_ in classes.iteritems():
        table['data'].append([
            link(class_),
            class_.name_translated
        ])
    return render_template('model/class.html', table=table)


@app.route('/model/property')
def model_property():
    properties = PropertyMapper.get_all()
    classes = ClassMapper.get_all()
    table = {
        'name': 'properties',
        'header': ['code', 'name', 'inverse', 'domain', 'range'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }, 3: { sorter: "class_code" }, 4: { sorter: "class_code" }}'
    }
    for property_id, property_ in properties.iteritems():
        table['data'].append([
            link(property_),
            property_.name_translated,
            property_.name_inverse_translated,
            link(classes[property_.domain_id]) + ' ' + classes[property_.domain_id].name_translated,
            link(classes[property_.range_id]) + ' ' + classes[property_.domain_id].name_translated
        ])
    return render_template('model/property.html', table=table)


@app.route('/model/class_view/<int:class_id>')
def model_class_view(class_id):
    classes = ClassMapper.get_all()
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
        }
        for id_ in getattr(classes[class_id], table):
            tables[table]['data'].append([
                link(classes[id_]),
                classes[id_].name_translated
            ])
    return render_template('model/class_view.html', class_=classes[class_id], tables=tables)
