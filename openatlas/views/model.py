# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import openatlas
from flask import render_template
from openatlas import app
from openatlas.models.classObject import ClassMapper


@app.route('/model')
def model_index():
    return render_template('model/index.html')


@app.route('/model/class')
def model_class():
    table_classes = {
        'name': 'classes',
        'header': ['code', 'name'],
        'data': []
    }
    for class_id, class_ in ClassMapper.get_all().iteritems():
        table_classes['data'].append([
            '<a href="/model/class_view/' + str(class_.id) + '">' + class_.code + '</a>',
            class_.name_translated
        ])
    return render_template('model/class.html', table_classes=table_classes)


@app.route('/model/class_view/<int:class_id>')
def model_class_view(class_id):
    return render_template('model/class_view.html', class_id=class_id, classes=ClassMapper.get_all())


@app.route('/model/property')
def model_property():
    return render_template('model/property.html')
