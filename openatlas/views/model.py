# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from collections import OrderedDict
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import SelectField

import openatlas
from openatlas import app
from openatlas.models.classObject import ClassMapper
from openatlas.models.property import PropertyMapper
from openatlas.util.util import link, uc_first


class LinkCheckForm(Form):
    domain = SelectField(uc_first(_('domain')), choices=[], coerce=int)
    property = SelectField(uc_first(_('property')), choices=[], coerce=int)
    range = SelectField(uc_first(_('range')), choices=[], coerce=int)


@app.route('/model', methods=["GET", "POST"])
def model_index():
    form = LinkCheckForm()
    form_classes = OrderedDict()
    for id_, class_ in openatlas.classes.iteritems():
        form_classes[id_] = class_.code + ' ' + class_.get_i18n('name')
    form.domain.choices = form_classes.iteritems()
    form.range.choices = form_classes.iteritems()
    form_properties = OrderedDict()
    for id_, property_ in openatlas.properties.iteritems():
        form_properties[id_] = property_.code + ' ' + property_.get_i18n('name')
    form.property.choices = form_properties.iteritems()
    if form.validate_on_submit():
        domain = openatlas.classes[int(form.domain.data)]
        range = openatlas.classes[int(form.range.data)]
        property = openatlas.properties[int(form.property.data)]
        # whitelistDomains = Zend_Registry::get('config')->get('linkcheckIgnoreDomains')->toArray();
        test_result = {}
        test_result['domain_error'] = False if property.find_object('id', domain.id) else True
        test_result['range_error'] = False if property.find_object('id', range.id) else True
        test_result['domain_whitelisted'] = True if domain.code in ['E61'] else False
        test_result['domain'] = domain
        test_result['property'] = property
        test_result['range'] = range
        return render_template('model/index.html', form=form, test_result=test_result)
    return render_template('model/index.html',form=form)


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
            class_.get_i18n('name')
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
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }, 3: { sorter: "class_code" }, 5: { sorter: "class_code" }}'
    }
    for property_id, property_ in properties.iteritems():
        table['data'].append([
            link(property_),
            property_.get_i18n('name'),
            property_.get_i18n('name_inverse'),
            link(classes[property_.domain_id]),
            classes[property_.domain_id].get_i18n('name'),
            link(classes[property_.range_id]),
            classes[property_.domain_id].get_i18n('name')
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
            tables[table]['data'].append([link(classes[id_]), classes[id_].get_i18n('name')])
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
    for id_, property in properties.iteritems():
        if class_id == property.domain_id:
            tables['domains']['data'].append([link(properties[id_]), properties[id_].get_i18n('name')])
        elif class_id == property.range_id:
            tables['ranges']['data'].append([link(properties[id_]), properties[id_].get_i18n('name')])

    return render_template('model/class_view.html', class_=classes[class_id], tables=tables)


@app.route('/model/property_view/<int:property_id>')
def model_property_view(property_id):
    properties = openatlas.properties
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }}'
        }
        for id_ in getattr(properties[property_id], table):
            tables[table]['data'].append([
                link(properties[id_]),
                properties[id_].get_i18n('name')
            ])
    return render_template('model/property_view.html', property=properties[property_id], tables=tables, classes=openatlas.classes)
