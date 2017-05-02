# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from collections import OrderedDict
from flask import render_template
from flask_wtf import Form
from wtforms import HiddenField

import openatlas
from openatlas import app, ClassMapper, PropertyMapper
from openatlas.util.util import link


class LinkCheckForm(Form):
    domain = HiddenField()
    property = HiddenField()
    range = HiddenField()


@app.route('/model', methods=["GET", "POST"])
def model_index():
    form = LinkCheckForm()
    form_classes = OrderedDict()
    for id_, class_ in openatlas.classes.iteritems():
        form_classes[id_] = class_.code + ' ' + class_.name
    form.domain.choices = form_classes.iteritems()
    form.range.choices = form_classes.iteritems()
    form_properties = OrderedDict()
    for id_, property_ in openatlas.properties.iteritems():
        form_properties[id_] = property_.code + ' ' + property_.name
    form.property.choices = form_properties.iteritems()
    test_result = None
    if form.validate_on_submit():
        domain = openatlas.classes[int(form.domain.data)]
        range_ = openatlas.classes[int(form.range.data)]
        property_ = openatlas.properties[int(form.property.data)]
        ignore = app.config['WHITELISTED_DOMAINS']
        test_result = {
            'domain_error': False if property_.find_object('domain_id', domain.id) or domain.code in ignore else True,
            'range_error': False if property_.find_object('range_id', range_.id) else True,
            'domain_whitelisted': True if domain.code in ignore else False,
            'domain': domain,
            'property': property_,
            'range': range_
        }
    else:
        domain = ClassMapper.get_by_code('E1')
        property_ = PropertyMapper.get_by_code('P1')
        range_ = domain
        form.domain.data = domain.id
        form.property.data = property_.id
        form.range.data = range_.id
    return render_template(
        'model/index.html',
        form=form,
        test_result=test_result,
        domain=domain,
        property=property_,
        range=range_,
    )


@app.route('/model/class')
def model_class():
    table = {
        'name': 'classes',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
    }
    for class_id, class_ in openatlas.classes.iteritems():
        table['data'].append([
            link(class_),
            class_.name
        ])
    return render_template('model/class.html', table=table)


@app.route('/model/property')
def model_property():
    classes = openatlas.classes
    properties = openatlas.properties
    table = {
        'name': 'properties',
        'header': ['code', 'name', 'inverse', 'domain', 'domain name', 'range', 'range name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }, 3: { sorter: "class_code" }, '
                '5: { sorter: "class_code" }}'
    }
    for property_id, property_ in properties.iteritems():
        table['data'].append([
            link(property_),
            property_.name,
            property_.name_inverse,
            link(classes[property_.domain_id]),
            classes[property_.domain_id].name,
            link(classes[property_.range_id]),
            classes[property_.domain_id].name
        ])
    return render_template('model/property.html', table=table)


@app.route('/model/class_view/<int:class_id>')
def model_class_view(class_id):
    classes = openatlas.classes
    properties = openatlas.properties
    tables = OrderedDict()
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
        }
        for id_ in getattr(classes[class_id], table):
            tables[table]['data'].append([link(classes[id_]), classes[id_].name])
    tables['domains'] = {
            'name': 'domains',
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
    }
    tables['ranges'] = {
            'name': 'ranges',
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'
    }
    for id_, property_ in properties.iteritems():
        if class_id == property_.domain_id:
            tables['domains']['data'].append([link(properties[id_]), properties[id_].name])
        elif class_id == property_.range_id:
            tables['ranges']['data'].append([link(properties[id_]), properties[id_].name])

    return render_template('model/class_view.html', class_=classes[class_id], tables=tables)


@app.route('/model/property_view/<int:property_id>')
def model_property_view(property_id):
    properties = openatlas.properties
    property_ = properties[property_id]
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }}'
        }
        for id_ in getattr(property_, table):
            tables[table]['data'].append([
                link(properties[id_]),
                properties[id_].name
            ])
    return render_template('model/property_view.html', property=property_, tables=tables, classes=openatlas.classes)
