# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import render_template
from openatlas import app
from openatlas.models.classObject import ClassMapper
from openatlas.util.util import link


@app.route('/model')
def model_index():
    return render_template('model/index.html')


@app.route('/model/class')
def model_class():
    classes = ClassMapper.get_all()
    table_classes = {
        'name': 'classes',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
    }
    for class_id, class_ in classes.iteritems():
        table_classes['data'].append([
            link(class_),
            class_.name_translated
        ])
    return render_template('model/class.html', table_classes=table_classes)


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


@app.route('/model/property')
def model_property():
    return render_template('model/property.html')
