# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import BooleanField, HiddenField, IntegerField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app
from openatlas.models.network import Network
from openatlas.util.util import link, required_group


class LinkCheckForm(Form):
    domain = HiddenField()
    property = HiddenField()
    range = HiddenField()


@app.route('/overview/model', methods=["GET", "POST"])
def model_index():
    form = LinkCheckForm()
    form_classes = OrderedDict()
    for code, class_ in openatlas.classes.items():
        form_classes[code] = code + ' ' + class_.name
    form.domain.choices = form_classes.items()
    form.range.choices = form_classes.items()
    form_properties = OrderedDict()
    for code, property_ in openatlas.properties.items():
        form_properties[code] = code + ' ' + property_.name
    form.property.choices = form_properties.items()
    test_result = None
    if form.validate_on_submit():
        domain = openatlas.classes[form.domain.data]
        range_ = openatlas.classes[form.range.data]
        property_ = openatlas.properties[form.property.data]
        ignore = app.config['WHITELISTED_DOMAINS']
        domain_error = True
        if property_.find_object('domain_class_code', domain.code) or domain.code in ignore:
            domain_error = False
        range_error = True
        if property_.find_object('range_class_code', range_.code):
            range_error = False
        test_result = {
            'domain_error': domain_error,
            'range_error': range_error,
            'domain_whitelisted': True if domain.code in ignore else False,
            'domain': domain,
            'property': property_,
            'range': range_}
    else:
        domain = openatlas.classes['E1']
        property_ = openatlas.properties['P1']
        range_ = domain
        form.domain.data = domain.code
        form.property.data = property_.code
        form.range.data = range_.code
    return render_template(
        'model/index.html',
        form=form,
        test_result=test_result,
        domain=domain,
        property=property_,
        range=range_)


@app.route('/overview/model/class')
def class_index():
    table = {
        'name': 'classes',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    for class_id, class_ in openatlas.classes.items():
        table['data'].append([
            link(class_),
            class_.name])
    return render_template('model/class.html', table=table)


@app.route('/overview/model/property')
def property_index():
    classes = openatlas.classes
    properties = openatlas.properties
    table = {
        'name': 'properties',
        'header': ['code', 'name', 'inverse', 'domain', 'domain name', 'range', 'range name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }, '
                '3: { sorter: "class_code" }, 5: { sorter: "class_code" }}'}
    for property_id, property_ in properties.items():
        table['data'].append([
            link(property_),
            property_.name,
            property_.name_inverse,
            link(classes[property_.domain_class_code]),
            classes[property_.domain_class_code].name,
            link(classes[property_.range_class_code]),
            classes[property_.range_class_code].name])
    return render_template('model/property.html', table=table)


@app.route('/overview/model/class_view/<code>')
def class_view(code):
    classes = openatlas.classes
    class_ = classes[code]
    tables = OrderedDict()
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
        for code in getattr(class_, table):
            tables[table]['data'].append([link(classes[code]), classes[code].name])
    tables['domains'] = {
        'name': 'domains',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    tables['ranges'] = {
        'name': 'ranges',
        'header': ['code', 'name'],
        'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    for key, property_ in openatlas.properties.items():
        if code == property_.domain_class_code:
            tables['domains']['data'].append([link(property_), property_.name])
        elif code == property_.range_class_code:
            tables['ranges']['data'].append([link(property_), property_.name])

    data = {'info': [('code', class_.code), ('name', class_.name)]}
    return render_template('model/class_view.html', class_=class_, tables=tables, data=data)


@app.route('/overview/model/property_view/<code>')
def property_view(code):
    properties = openatlas.properties
    property_ = properties[code]
    classes = openatlas.classes
    tables = {
        'info': [
            ('code', property_.code),
            ('name', property_.name),
            ('inverse', property_.name_inverse),
            ('domain', link(classes[property_.domain_class_code]) + ' ' + classes[property_.domain_class_code].name),
            ('range', link(classes[property_.range_class_code]) + ' ' + classes[property_.range_class_code].name)]}
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }}'}
        for code in getattr(property_, table):
            tables[table]['data'].append([
                link(properties[code]),
                properties[code].name])
    return render_template('model/property_view.html', property=property_, tables=tables)


class NetworkForm(Form):
    orphans = BooleanField(default=False)
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = IntegerField(default=-800, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    save = SubmitField(_('apply'))


@app.route('/overview/network/', methods=["GET", "POST"])
@required_group('readonly')
def model_network():
    params = {
        'classes': {
            'E21': {'active': True,  'color':  '#34B522'},   # Person
            'E7':  {'active':  True,  'color':  '#E54A2A'},  # Activity
            'E31': {'active': False, 'color':  '#FFA500'},   # Document
            'E33': {'active': False, 'color':  '#FFA500'},   # Linguistic Object
            'E40': {'active': True,  'color':  '#34623C'},   # Legal Body
            'E74': {'active': True,  'color':  '#34623C'},   # Group
            'E53': {'active': False, 'color':  '#00FF00'},   # Places
            'E18': {'active': False, 'color':  '#FF0000'},   # Physical Object
            'E8':  {'active':  True,  'color':  '#E54A2A'},  # Acquisition
            'E12': {'active': True,  'color':  '#E54A2A'},   # Production
            'E6':  {'active':  True,  'color':  '#E54A2A'},  # Destruction
            'E84': {'active': False, 'color':  '#EE82EE'}},  # Information Carrier
        'properties': {
            'P107': {'active':  True},   # has current or former member
            'P11':  {'active':  True},   # had participant
            'P14':  {'active':  True},   # carried out by
            'P7':   {'active':  True},   # took place at
            'P74':  {'active':  True},   # has current or former residence
            'P67':  {'active':  True},   # refers to
            'OA7':  {'active':  True},   # has relationship to
            'OA8':  {'active':  True},   # appears for the first time in
            'OA9':  {'active':  True}},  # appears for the last time in
        'options': {
            'orphans': False,
            'width': 1200,
            'height': 600,
            'charge': -800,
            'distance': 80}}
    form = NetworkForm()
    if form.validate_on_submit():
        params['options']['orphans'] = form.orphans.data
        params['options']['width'] = form.width.data
        params['options']['height'] = form.height.data
        params['options']['charge'] = form.charge.data
        params['options']['distance'] = form.distance.data

    return render_template(
        'model/network.html',
        form=form,
        network_params=params,
        json_data=Network.get_network_json(params))
