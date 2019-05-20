# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import g, render_template
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (BooleanField, HiddenField, IntegerField, SelectMultipleField, StringField,
                     SubmitField, widgets)
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.network import Network
from openatlas.util.table import Table
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
        test_result = {'domain': domain, 'property': property_, 'range': range_,
                       'domain_error': False if domain_is_valid else True,
                       'range_error': False if range_is_valid else True}
    else:
        domain = g.classes['E1']
        property_ = g.properties['P1']
        range_ = domain
        form.domain.data = domain.code
        form.property.data = property_.code
        form.range.data = range_.code
    return render_template('model/index.html', form=form, test_result=test_result, domain=domain,
                           property=property_, range=range_)


@app.route('/overview/model/class')
def class_index():
    table = Table(['code', 'name'], sort='[[0, 0]]', headers='{0:{sorter:"class_code"}}')
    for class_id, class_ in g.classes.items():
        table.rows.append([link(class_), class_.name])
    return render_template('model/class.html', table=table)


@app.route('/overview/model/property')
def property_index():
    classes = g.classes
    properties = g.properties
    table = Table(
        ['code', 'name', 'inverse', 'domain', 'domain name', 'range', 'range name'],
        sort='[[0, 0]]',
        headers='{0:{sorter:"property_code"},3:{sorter:"class_code"},5:{sorter:"class_code"}}')
    for property_id, property_ in properties.items():
        table.rows.append([link(property_),
                           property_.name,
                           property_.name_inverse,
                           link(classes[property_.domain_class_code]),
                           classes[property_.domain_class_code].name,
                           link(classes[property_.range_class_code]),
                           classes[property_.range_class_code].name])
    return render_template('model/property.html', table=table)


@app.route('/overview/model/class_view/<code>')
def class_view(code):
    class_ = g.classes[code]
    tables = OrderedDict()
    for table in ['super', 'sub']:
        tables[table] = Table(['code', 'name'], pager=False, sort='[[0, 0]]',
                              headers='{0:{sorter:"class_code"}}')
        for code in getattr(class_, table):
            tables[table].rows.append([link(g.classes[code]), g.classes[code].name])
    tables['domains'] = Table(['code', 'name'], pager=False, sort='[[0, 0]]',
                              headers='{0:{sorter:"property_code"}}')
    tables['ranges'] = Table(['code', 'name'], pager=False, sort='[[0, 0]]',
                             headers='{0:{sorter:"property_code"}}')
    for key, property_ in g.properties.items():
        if code == property_.domain_class_code:
            tables['domains'].rows.append([link(property_), property_.name])
        elif code == property_.range_class_code:
            tables['ranges'].rows.append([link(property_), property_.name])
    return render_template('model/class_view.html', class_=class_, tables=tables,
                           data={'info': [('code', class_.code), ('name', class_.name)]})


@app.route('/overview/model/property_view/<code>')
def property_view(code):
    property_ = g.properties[code]
    domain = g.classes[property_.domain_class_code]
    range_ = g.classes[property_.range_class_code]
    tables = {'info': [('code', property_.code),
                       ('name', property_.name),
                       ('inverse', property_.name_inverse),
                       ('domain', link(domain) + ' ' + domain.name),
                       ('range', link(range_) + ' ' + range_.name)]}
    for table in ['super', 'sub']:
        tables[table] = Table(['code', 'name'], pager=False, sort='[[0, 0]]',
                              headers='{0:{sorter:"property_code"}}')
        for code in getattr(property_, table):
            tables[table].rows.append([link(g.properties[code]), g.properties[code].name])
    return render_template('model/property_view.html', property=property_, tables=tables)


class NetworkForm(Form):
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = StringField(default=-800, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    orphans = BooleanField(default=False)
    classes = SelectMultipleField(_('classes'),
                                  option_widget=widgets.CheckboxInput(),
                                  widget=widgets.ListWidget(prefix_label=False),
                                  default=['E21', 'E7', 'E40', 'E74', 'E8', 'E12', 'E6'])
    properties = SelectMultipleField(
        _('properties'),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        default=['P107', 'P24', 'P23', 'P11', 'P14', 'P7', 'P74', 'P67', 'OA7', 'OA8', 'OA9'])
    kw_params = {'data-huebee': True, 'class': 'data-huebee'}
    color_E21 = StringField(default='#34B522', render_kw=kw_params)
    color_E7 = StringField(default='#E54A2A', render_kw=kw_params)
    color_E31 = StringField(default='#FFA500', render_kw=kw_params)
    color_E33 = StringField(default='#FFA500', render_kw=kw_params)
    color_E40 = StringField(default='#34623C', render_kw=kw_params)
    color_E74 = StringField(default='#34623C', render_kw=kw_params)
    color_E53 = StringField(default='#00FF00', render_kw=kw_params)
    color_E18 = StringField(default='#FF0000', render_kw=kw_params)
    color_E8 = StringField(default='#E54A2A', render_kw=kw_params)
    color_E12 = StringField(default='#E54A2A', render_kw=kw_params)
    color_E6 = StringField(default='#E54A2A', render_kw=kw_params)
    color_E84 = StringField(default='#EE82EE', render_kw=kw_params)
    save = SubmitField(_('apply'))


@app.route('/overview/network/', methods=["GET", "POST"])
@required_group('readonly')
def model_network():
    form = NetworkForm()
    form.classes.choices = []
    form.properties.choices = []
    params = {'classes': {}, 'properties': {}, 'options': {'orphans': form.orphans.data,
                                                           'width': form.width.data,
                                                           'height': form.height.data,
                                                           'charge': form.charge.data,
                                                           'distance': form.distance.data}}
    for code in ['E21', 'E7', 'E31', 'E33', 'E40', 'E74', 'E53', 'E18', 'E8', 'E12', 'E6', 'E84']:
        form.classes.choices.append((code, g.classes[code].name))
        params['classes'][code] = {'active': (code in form.classes.data),
                                   'color': getattr(form, 'color_' + code).data}
    for code in ['P107', 'P24', 'P23', 'P11', 'P14', 'P7', 'P74', 'P67', 'OA7', 'OA8', 'OA9']:
        form.properties.choices.append((code, g.properties[code].name))
        params['properties'][code] = {'active': (code in form.properties.data)}
    return render_template('model/network.html', form=form, network_params=params,
                           json_data=Network.get_network_json(params))
