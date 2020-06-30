from typing import Any, Dict, Optional

from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (BooleanField, HiddenField, IntegerField, SelectMultipleField, StringField,
                     SubmitField, widgets)
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.network import Network
from openatlas.util.table import Table
from openatlas.util.util import link, required_group, uc_first


class LinkCheckForm(FlaskForm):  # type: ignore
    domain = HiddenField()
    property = HiddenField()
    range = HiddenField()
    test = SubmitField(uc_first(_('test')))


@app.route('/overview/model', methods=["GET", "POST"])
@required_group('readonly')
def model_index() -> str:
    form = LinkCheckForm()
    form_classes = {}
    for code, class_ in g.classes.items():
        form_classes[code] = code + ' ' + class_.name
    form.domain.choices = form_classes.items()
    form.range.choices = form_classes.items()
    form_properties = {}
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
        test_result = {'domain': domain,
                       'property': property_,
                       'range': range_,
                       'domain_error': False if domain_is_valid else True,
                       'range_error': False if range_is_valid else True}
    else:
        domain = g.classes['E1']
        property_ = g.properties['P1']
        range_ = domain
        form.domain.data = domain.code
        form.property.data = property_.code
        form.range.data = range_.code
    return render_template('model/index.html',
                           form=form,
                           test_result=test_result,
                           domain=domain,
                           property=property_,
                           range=range_)


@app.route('/overview/model/class/<code>')
@required_group('readonly')
def class_entities(code: str) -> str:
    table = Table(['name'], rows=[[link(entity)] for entity in Entity.get_by_class_code(code)])
    return render_template('model/class_entities.html', table=table, class_=g.classes[code])


@app.route('/overview/model/class')
@required_group('readonly')
def class_index() -> str:
    table = Table(['code', 'name', 'count'],
                  defs=[{'className': 'dt-body-right', 'targets': 2},
                        {'orderDataType': 'cidoc-model', 'targets': [0]},
                        {'sType': 'numeric', 'targets': [0]}])
    for class_id, class_ in g.classes.items():
        count = ''
        if class_.count:
            if class_.code in ['E53', 'E41', 'E82']:
                count = format_number(class_.count)
            else:
                url = url_for('class_entities', code=class_.code)
                count = '<a href="' + url + '">' + format_number(class_.count) + '</a>'
        table.rows.append([link(class_), class_.name, count])
    return render_template('model/class.html', table=table)


@app.route('/overview/model/property')
@required_group('readonly')
def property_index() -> str:
    classes = g.classes
    properties = g.properties
    table = Table(['code', 'name', 'inverse', 'domain', 'domain name', 'range', 'range name',
                   'count'],
                  defs=[{'className': 'dt-body-right', 'targets': 7},
                        {'orderDataType': 'cidoc-model', 'targets': [0, 3, 5]},
                        {'sType': 'numeric', 'targets': [0]}])
    for property_id, property_ in properties.items():
        table.rows.append([link(property_),
                           property_.name,
                           property_.name_inverse,
                           link(classes[property_.domain_class_code]),
                           classes[property_.domain_class_code].name,
                           link(classes[property_.range_class_code]),
                           classes[property_.range_class_code].name,
                           format_number(property_.count) if property_.count else ''])
    return render_template('model/property.html', table=table)


@app.route('/overview/model/class_view/<code>')
@required_group('readonly')
def class_view(code: str) -> str:
    class_ = g.classes[code]
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = Table(paging=False,
                              defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                    {'sType': 'numeric', 'targets': [0]}])
        for code_ in getattr(class_, table):
            tables[table].rows.append([link(g.classes[code_]), g.classes[code_].name])
    tables['domains'] = Table(paging=False,
                              defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                    {'sType': 'numeric', 'targets': [0]}])
    tables['ranges'] = Table(paging=False,
                             defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                   {'sType': 'numeric', 'targets': [0]}])
    for key, property_ in g.properties.items():
        if class_.code == property_.domain_class_code:
            tables['domains'].rows.append([link(property_), property_.name])
        elif class_.code == property_.range_class_code:
            tables['ranges'].rows.append([link(property_), property_.name])
    return render_template('model/class_view.html',
                           class_=class_,
                           tables=tables,
                           info={'code': class_.code, 'name': class_.name})


@app.route('/overview/model/property_view/<code>')
@required_group('readonly')
def property_view(code: str) -> str:
    property_ = g.properties[code]
    domain = g.classes[property_.domain_class_code]
    range_ = g.classes[property_.range_class_code]
    info = {'code': property_.code,
            'name': property_.name,
            'inverse': property_.name_inverse,
            'domain': link(domain) + ' ' + domain.name,
            'range': link(range_) + ' ' + range_.name}
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = Table(paging=False,
                              defs=[{'orderDataType': 'cidoc-model', 'targets': [0]},
                                    {'sType': 'numeric', 'targets': [0]}])
        for code in getattr(property_, table):
            tables[table].rows.append([link(g.properties[code]), g.properties[code].name])
    return render_template('model/property_view.html', property=property_, tables=tables, info=info)


class NetworkForm(FlaskForm):  # type: ignore
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = StringField(default=-80, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    orphans = BooleanField(default=False)
    classes = SelectMultipleField(_('classes'), widget=widgets.ListWidget(prefix_label=False))
    kw_params = {'data-huebee': True, 'class': 'data-huebee'}
    color_E7 = StringField(default='#0000FF', render_kw=kw_params)
    color_E8 = StringField(default='#0000FF', render_kw=kw_params)
    color_E9 = StringField(default='#0000FF', render_kw=kw_params)
    color_E18 = StringField(default='#FF0000', render_kw=kw_params)
    color_E21 = StringField(default='#34B522', render_kw=kw_params)
    color_E31 = StringField(default='#FFA500', render_kw=kw_params)
    color_E33 = StringField(default='#FFA500', render_kw=kw_params)
    color_E40 = StringField(default='#34623C', render_kw=kw_params)
    color_E53 = StringField(default='#00FF00', render_kw=kw_params)
    color_E74 = StringField(default='#34623C', render_kw=kw_params)
    color_E84 = StringField(default='#EE82EE', render_kw=kw_params)
    save = SubmitField(_('apply'))


@app.route('/overview/network/', methods=["GET", "POST"])
@app.route('/overview/network/<int:dimensions>', methods=["GET", "POST"])
@required_group('readonly')
def model_network(dimensions: Optional[int] = None) -> str:
    form = NetworkForm()
    form.classes.choices = []
    params: Dict[str, Any] = {'classes': {},
                              'options': {'orphans': form.orphans.data,
                                          'width': form.width.data,
                                          'height': form.height.data,
                                          'charge': form.charge.data,
                                          'distance': form.distance.data}}
    for code in Network.classes:
        form.classes.choices.append((code, g.classes[code].name))
        params['classes'][code] = {'color': getattr(form, 'color_' + code).data}
    return render_template('model/network2.html' if dimensions else 'model/network.html',
                           form=form,
                           dimensions=dimensions,
                           network_params=params,
                           json_data=Network.get_network_json(form, params, dimensions))
