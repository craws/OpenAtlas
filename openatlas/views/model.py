# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import g, render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (BooleanField, HiddenField, IntegerField, SelectMultipleField, StringField,
                     SubmitField, widgets)
from wtforms.validators import InputRequired

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
    for code, class_ in g.classes.items():
        form_classes[code] = code + ' ' + class_.name
    form.domain.choices = form_classes.items()
    form.range.choices = form_classes.items()
    form_properties = OrderedDict()
    for code, property_ in g.properties.items():
        form_properties[code] = code + ' ' + property_.name
    form.property.choices = form_properties.items()
    test_result = None
    if form.validate_on_submit():
        domain = g.classes[form.domain.data]
        range_ = g.classes[form.range.data]
        property_ = g.properties[form.property.data]
        domain_is_valid = property_.find_object('domain_class_code', domain.code)
        range_is_valid = property_.find_object('range_class_code', range_.code)
        test_result = {
            'domain_error': False if domain_is_valid else True,
            'range_error': False if range_is_valid else True,
            'domain': domain,
            'property': property_,
            'range': range_}
    else:
        domain = g.classes['E1']
        property_ = g.properties['P1']
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
        'id': 'classes', 'header': ['code', 'name'], 'data': [],
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    for class_id, class_ in g.classes.items():
        table['data'].append([link(class_), class_.name])
    return render_template('model/class.html', table=table)


@app.route('/overview/model/property')
def property_index():
    classes = g.classes
    properties = g.properties
    table = {
        'id': 'properties', 'data': [],
        'header': ['code', 'name', 'inverse', 'domain', 'domain name', 'range', 'range name'],
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
    classes = g.classes
    class_ = classes[code]
    tables = OrderedDict()
    for table in ['super', 'sub']:
        tables[table] = {
            'id': table, 'header': ['code', 'name'], 'data': [], 'show_pager': False,
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
        for code in getattr(class_, table):
            tables[table]['data'].append([link(classes[code]), classes[code].name])
    tables['domains'] = {
        'id': 'domains', 'header': ['code', 'name'], 'data': [], 'show_pager': False,
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    tables['ranges'] = {
        'id': 'ranges', 'header': ['code', 'name'], 'data': [], 'show_pager': False,
        'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "class_code" }}'}
    for key, property_ in g.properties.items():
        if code == property_.domain_class_code:
            tables['domains']['data'].append([link(property_), property_.name])
        elif code == property_.range_class_code:
            tables['ranges']['data'].append([link(property_), property_.name])
    data = {'info': [('code', class_.code), ('name', class_.name)]}
    return render_template('model/class_view.html', class_=class_, tables=tables, data=data)


@app.route('/overview/model/property_view/<code>')
def property_view(code):
    property_ = g.properties[code]
    domain = g.classes[property_.domain_class_code]
    range_ = g.classes[property_.range_class_code]
    tables = {
        'info': [
            ('code', property_.code),
            ('name', property_.name),
            ('inverse', property_.name_inverse),
            ('domain', link(domain) + ' ' + domain.name),
            ('range', link(range_) + ' ' + range_.name)]}
    for table in ['super', 'sub']:
        tables[table] = {
            'id': table, 'header': ['code', 'name'], 'data': [], 'show_pager': False,
            'sort': 'sortList: [[0, 0]],headers: {0: { sorter: "property_code" }}'}
        for code in getattr(property_, table):
            tables[table]['data'].append([link(g.properties[code]), g.properties[code].name])
    return render_template('model/property_view.html', property=property_, tables=tables)


class NetworkForm(Form):
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = StringField(default=-800, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    orphans = BooleanField(default=False)
    classes = SelectMultipleField(
        _('classes'),
        [InputRequired()],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        default=['E21', 'E7', 'E40', 'E74', 'E8', 'E12', 'E6'],
        choices=([
            ('E21', 'Person'),
            ('E7', 'Activity'),
            ('E31', 'Document'),
            ('E33', 'Linguistic Object'),
            ('E40', 'Legal Body'),
            ('E74', 'Group'),
            ('E53', 'Places'),
            ('E18', 'Physical Object'),
            ('E8', 'Acquisition'),
            ('E12', 'Production'),
            ('E6', 'Destruction'),
            ('E84', 'Information Carrier')]))
    properties = SelectMultipleField(
        _('properties'),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        default=['P107', 'P24', 'P23', 'P11', 'P14', 'P7', 'P74', 'P67', 'OA7', 'OA8', 'OA9'],
        choices=([
            ('P107', 'has current or former member'),
            ('P24', 'transferred title of'),
            ('P23', 'transferred title to'),
            ('P11', 'had participant'),
            ('P14', 'carried out by'),
            ('P7', 'took place at'),
            ('P74', 'has current or former residence'),
            ('P67', 'refers to'),
            ('OA7', 'has relationship to'),
            ('OA8', 'appears for the first time in'),
            ('OA9', 'appears for the last time in')]))
    color_E21 = StringField('Person', default='#34B522', render_kw={'data-huebee': True})
    color_E7 = StringField('Activity', default='#E54A2A', render_kw={'data-huebee': True})
    color_E31 = StringField('Document', default='#FFA500', render_kw={'data-huebee': True})
    color_E33 = StringField('Linguistic Object', default='#FFA500', render_kw={'data-huebee': True})
    color_E40 = StringField('Legal Body', default='#34623C', render_kw={'data-huebee': True})
    color_E74 = StringField('Group', default='#34623C', render_kw={'data-huebee': True})
    color_E53 = StringField('Places', default='#00FF00', render_kw={'data-huebee': True})
    color_E18 = StringField('Physical Object', default='#FF0000', render_kw={'data-huebee': True})
    color_E8 = StringField('Acquisition', default='#E54A2A', render_kw={'data-huebee': True})
    color_E12 = StringField('Production', default='#E54A2A', render_kw={'data-huebee': True})
    color_E6 = StringField('Destruction', default='#E54A2A', render_kw={'data-huebee': True})
    color_E84 = StringField('Information Carrier', default='#EE82EE', render_kw={'data-huebee': True})
    save = SubmitField(_('apply'))


@app.route('/overview/network/', methods=["GET", "POST"])
@required_group('readonly')
def model_network():
    form = NetworkForm()
    form.classes.process(request.form)
    if not form.classes.data:
        form.classes.data = []
    params = {
        'classes': {
            'E21': {'active': ('E21' in form.classes.data), 'color': form.color_E21.data},
            'E7':  {'active': ('E7' in form.classes.data), 'color': form.color_E7.data},
            'E31': {'active': ('E31' in form.classes.data), 'color': form.color_E31.data},
            'E33': {'active': ('E33' in form.classes.data), 'color': form.color_E33.data},
            'E40': {'active': ('E40' in form.classes.data), 'color': form.color_E40.data},
            'E74': {'active': ('E74' in form.classes.data), 'color': form.color_E74.data},
            'E53': {'active': ('E53' in form.classes.data), 'color': form.color_E53.data},
            'E18': {'active': ('E18' in form.classes.data), 'color': form.color_E18.data},
            'E8':  {'active': ('E8' in form.classes.data), 'color': form.color_E8.data},
            'E12': {'active': ('E12' in form.classes.data), 'color': form.color_E12.data},
            'E6':  {'active': ('E6' in form.classes.data), 'color': form.color_E6.data},
            'E84': {'active': ('E84' in form.classes.data), 'color': form.color_E84.data}},
        'properties': {
            'P107': {'active': ('P107' in form.properties.data)},
            'P24':  {'active': ('P24' in form.properties.data)},
            'P23':  {'active': ('P23' in form.properties.data)},
            'P11':  {'active': ('P11' in form.properties.data)},
            'P14':  {'active': ('P14' in form.properties.data)},
            'P7':   {'active': ('P7' in form.properties.data)},
            'P74':  {'active': ('P74' in form.properties.data)},
            'P67':  {'active': ('P67' in form.properties.data)},
            'OA7':  {'active': ('OA7' in form.properties.data)},
            'OA8':  {'active': ('OA8' in form.properties.data)},
            'OA9':  {'active': ('OA9' in form.properties.data)}},
        'options': {
            'orphans': False,
            'width': 1200,
            'height': 600,
            'charge': -800,
            'distance': 80}}
    if form.validate_on_submit():
        params['options']['orphans'] = form.orphans.data
        params['options']['width'] = form.width.data
        params['options']['height'] = form.height.data
        params['options']['charge'] = form.charge.data
        params['options']['distance'] = form.distance.data
    data = Network.get_network_json(params)
    return render_template('model/network.html', form=form, network_params=params, json_data=data)
