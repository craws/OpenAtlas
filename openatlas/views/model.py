# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict
from flask import render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import BooleanField, HiddenField, IntegerField, SubmitField
from wtforms.validators import InputRequired

import openatlas
from openatlas import app, PropertyMapper
from openatlas.models.classObject import ClassMapper
from openatlas.models.network import Network
from openatlas.util.util import link, required_group


class LinkCheckForm(Form):
    domain = HiddenField()
    property = HiddenField()
    range = HiddenField()


@app.route('/model', methods=["GET", "POST"])
def model_index():
    form = LinkCheckForm()
    form_classes = OrderedDict()
    for id_, class_ in openatlas.classes.items():
        form_classes[id_] = class_.code + ' ' + class_.name
    form.domain.choices = form_classes.items()
    form.range.choices = form_classes.items()
    form_properties = OrderedDict()
    for id_, property_ in openatlas.properties.items():
        form_properties[id_] = property_.code + ' ' + property_.name
    form.property.choices = form_properties.items()
    test_result = None
    if form.validate_on_submit():
        domain = openatlas.classes[int(form.domain.data)]
        range_ = openatlas.classes[int(form.range.data)]
        property_ = openatlas.properties[int(form.property.data)]
        ignore = app.config['WHITELISTED_DOMAINS']
        domain_error = True
        if property_.find_object('domain_id', domain.id) or domain.code in ignore:
            domain_error = False
        test_result = {
            'domain_error': domain_error,
            'range_error': False if property_.find_object('range_id', range_.id) else True,
            'domain_whitelisted': True if domain.code in ignore else False,
            'domain': domain,
            'property': property_,
            'range': range_}
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
        range=range_)


@app.route('/model/class')
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


@app.route('/model/property')
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
            link(classes[property_.domain_id]),
            classes[property_.domain_id].name,
            link(classes[property_.range_id]),
            classes[property_.domain_id].name])
    return render_template('model/property.html', table=table)


@app.route('/model/class_view/<int:class_id>')
def class_view(class_id):
    classes = openatlas.classes
    class_ = classes[class_id]
    tables = OrderedDict()
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
        for id_ in getattr(classes[class_id], table):
            tables[table]['data'].append([link(classes[id_]), classes[id_].name])
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
        if class_id == property_.domain_id:
            tables['domains']['data'].append([link(property_), property_.name])
        elif class_id == property_.range_id:
            tables['ranges']['data'].append([link(property_), property_.name])

    data = {'info': [('code', class_.code), ('name', class_.name)]}
    return render_template('model/class_view.html', class_=class_, tables=tables, data=data)


@app.route('/model/property_view/<int:property_id>')
def property_view(property_id):
    properties = openatlas.properties
    property_ = properties[property_id]
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = {
            'name': table,
            'header': ['code', 'name'],
            'data': [],
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }}'}
        for id_ in getattr(property_, table):
            tables[table]['data'].append([
                link(properties[id_]),
                properties[id_].name])
    return render_template(
        'model/property_view.html',
        property=property_,
        tables=tables,
        classes=openatlas.classes)


class NetworkForm(Form):
    orphans = BooleanField(default=False)
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = IntegerField(default=-800, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    save = SubmitField(_('apply'))


@app.route('/model/network/', methods=["GET", "POST"])
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
