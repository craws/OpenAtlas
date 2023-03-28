from typing import Optional

from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, IntegerField, SelectMultipleField, StringField, widgets)
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import link, manual, required_group, uc_first
from openatlas.forms.field import SubmitField, TableField
from openatlas.models.entity import Entity
from openatlas.models.network import Network
from openatlas.models.openatlas_class import OpenatlasClass


class LinkCheckForm(FlaskForm):
    cidoc_domain = TableField('Domain', [InputRequired()])
    cidoc_property = TableField('Property', [InputRequired()])
    cidoc_range = TableField('Range', [InputRequired()])
    save = SubmitField(_('test'))


@app.route('/overview/model', methods=["GET", "POST"])
@required_group('readonly')
def model_index() -> str:
    form = LinkCheckForm()
    form_classes = {
        code: f'{code} {class_.name}'
        for code, class_ in g.cidoc_classes.items()}
    form.cidoc_domain.choices = form_classes
    form.cidoc_range.choices = form_classes
    form.cidoc_property.choices = {
        code: f'{code} {property_.name}'
        for code, property_ in g.properties.items()}
    result = None
    if form.validate_on_submit():
        domain = g.cidoc_classes[form.cidoc_domain.data]
        range_ = g.cidoc_classes[form.cidoc_range.data]
        property_ = g.properties[form.cidoc_property.data]
        result = {
            'domain': domain,
            'property': property_,
            'range': range_,
            'domain_valid':
                property_.find_object('domain_class_code', domain.code),
            'range_valid':
                property_.find_object('range_class_code', range_.code)}
    return render_template(
        'model/index.html',
        form=form,
        result=result,
        title=_('model'),
        buttons=[manual('model/index')],
        crumbs=[_('model')])


@app.route('/overview/model/class/<code>')
@required_group('readonly')
def class_entities(code: str) -> str:
    table = Table(
        ['name'],
        rows=[[link(entity)] for entity in Entity.get_by_cidoc_class(code)])
    return render_template(
        'content.html',
        content=table.display(),
        title=_('model'),
        crumbs=[
            [_('model'), url_for('model_index')],
            [_('classes'), url_for('cidoc_class_index')],
            link(g.cidoc_classes[code]),
            _('entities')])


@app.route('/overview/model/openatlas_class_index')
@required_group('readonly')
def openatlas_class_index() -> str:
    table = Table([
        'name',
        f"CIDOC {_('class')}",
        _('standard type'),
        _('view'),
        _('write access'),
        'alias',
        _('reference system'),
        'add type',
        _('color'),
        _('icon'),
        'count'],
        defs=[
            {'orderDataType': 'cidoc-model', 'targets': [1]},
            {'sType': 'numeric', 'targets': [1]}])
    class_count = OpenatlasClass.get_class_count()
    for class_ in g.classes.values():
        table.rows.append([
            class_.label,
            link(class_.cidoc_class),
            link(g.types[class_.standard_type_id])
            if class_.standard_type_id else '',
            (class_.view.replace("_", " ")) if class_.view else '',
            class_.write_access,
            _('allowed') if class_.alias_allowed else '',
            _('allowed') if class_.reference_system_allowed else '',
            _('allowed') if class_.new_types_allowed else '',
            class_.network_color,
            class_.icon,
            format_number(class_count[class_.name])
            if class_count[class_.name] else ''])
    return render_template(
        'content.html',
        content=table.display(),
        title=_('model'),
        crumbs=[
            [_('model'), url_for('model_index')],
            f"OpenAtlas {_('classes')}"])


@app.route('/overview/model/cidoc_class_index')
@required_group('readonly')
def cidoc_class_index() -> str:
    table = Table(
        ['code', 'name', 'count'],
        defs=[
            {'className': 'dt-body-right', 'targets': 2},
            {'orderDataType': 'cidoc-model', 'targets': [0]},
            {'sType': 'numeric', 'targets': [0]}])
    for class_ in g.cidoc_classes.values():
        count = ''
        if class_.count:
            count = format_number(class_.count)
            if class_.code not in ['E53', 'E41', 'E82']:
                count = link(
                    format_number(class_.count),
                    url_for('class_entities', code=class_.code))
        table.rows.append([link(class_), class_.name, count])
    return render_template(
        'content.html',
        content=table.display(),
        title=_('model'),
        crumbs=[[_('model'), url_for('model_index')], _('classes')])


@app.route('/overview/model/property')
@required_group('readonly')
def property_index() -> str:
    classes = g.cidoc_classes
    properties = g.properties
    table = Table(
        [
            'code', 'name', 'inverse', 'domain', 'domain name', 'range',
            'range name', 'count'],
        defs=[
            {'className': 'dt-body-right', 'targets': 7},
            {'orderDataType': 'cidoc-model', 'targets': [0, 3, 5]},
            {'sType': 'numeric', 'targets': [0, 3, 5]}])
    for property_ in properties.values():
        table.rows.append([
            link(property_),
            property_.name,
            property_.name_inverse,
            link(classes[property_.domain_class_code]),
            classes[property_.domain_class_code].name,
            link(classes[property_.range_class_code]),
            classes[property_.range_class_code].name,
            format_number(property_.count) if property_.count else ''])
    return render_template(
        'content.html',
        content=table.display(),
        title=_('model'),
        crumbs=[[_('model'), url_for('model_index')], _('properties')])


@app.route('/overview/model/cidoc_class_view/<code>')
@required_group('readonly')
def cidoc_class_view(code: str) -> str:
    class_ = g.cidoc_classes[code]
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = Table(paging=False, defs=[
            {'orderDataType': 'cidoc-model', 'targets': [0]},
            {'sType': 'numeric', 'targets': [0]}])
        for code_ in getattr(class_, table):
            tables[table].rows.append(
                [link(g.cidoc_classes[code_]), g.cidoc_classes[code_].name])
    tables['domains'] = Table(paging=False, defs=[
        {'orderDataType': 'cidoc-model', 'targets': [0]},
        {'sType': 'numeric', 'targets': [0]}])
    tables['ranges'] = Table(paging=False, defs=[
        {'orderDataType': 'cidoc-model', 'targets': [0]},
        {'sType': 'numeric', 'targets': [0]}])
    for property_ in g.properties.values():
        if class_.code == property_.domain_class_code:
            tables['domains'].rows.append([link(property_), property_.name])
        elif class_.code == property_.range_class_code:
            tables['ranges'].rows.append([link(property_), property_.name])
    return render_template(
        'model/cidoc_class_view.html',
        class_=class_,
        tables=tables,
        info={'code': class_.code, 'name': class_.name},
        title=_('model'),
        crumbs=[
            [_('model'), url_for('model_index')],
            [_('classes'), url_for('cidoc_class_index')],
            class_.code])


@app.route('/overview/model/property_view/<code>')
@required_group('readonly')
def property_view(code: str) -> str:
    property_ = g.properties[code]
    domain = g.cidoc_classes[property_.domain_class_code]
    range_ = g.cidoc_classes[property_.range_class_code]
    info = {
        'code': property_.code,
        'name': property_.name,
        'inverse': property_.name_inverse,
        'domain': f'{link(domain)} {domain.name}',
        'range': f'{link(range_)} {range_.name}'}
    tables = {}
    for table in ['super', 'sub']:
        tables[table] = Table(paging=False, defs=[
            {'orderDataType': 'cidoc-model', 'targets': [0]},
            {'sType': 'numeric', 'targets': [0]}])
        for code_ in getattr(property_, table):
            tables[table].rows.append(
                [link(g.properties[code_]), g.properties[code_].name])
    return render_template(
        'model/property_view.html',
        tables=tables,
        property_=property_,
        info=info,
        title=_('model'),
        crumbs=[
            [_('model'), url_for('model_index')],
            [_('properties'), url_for('property_index')],
            property_.code])


class NetworkForm(FlaskForm):
    width = IntegerField(default=1200, validators=[InputRequired()])
    height = IntegerField(default=600, validators=[InputRequired()])
    charge = StringField(default=-80, validators=[InputRequired()])
    distance = IntegerField(default=80, validators=[InputRequired()])
    orphans = BooleanField(default=False)
    classes = SelectMultipleField(
        _('classes'),
        widget=widgets.ListWidget(prefix_label=False))


@app.route('/overview/network/', methods=["GET", "POST"])
@app.route('/overview/network/<int:dimensions>', methods=["GET", "POST"])
@required_group('readonly')
def model_network(dimensions: Optional[int] = None) -> str:
    classes = [c for c in g.classes.values() if c.network_color]
    for class_ in classes:
        setattr(NetworkForm, class_.name, StringField(
            default=class_.network_color,
            render_kw={
                'data-huebee': True,
                'class': f'data-huebee {app.config["CSS"]["string_field"]}'}))
    setattr(NetworkForm, 'save', SubmitField(_('apply')))
    form = NetworkForm()
    form.classes.choices = []
    for class_ in classes:
        if class_.name == 'object_location':
            continue
        form.classes.choices.append((class_.name, uc_first(class_.label)))
    return render_template(
        'model/network2.html' if dimensions else 'model/network.html',
        form=form,
        dimensions=dimensions,
        network_params={
            'classes': {},
            'options': {
                'orphans': form.orphans.data,
                'width': form.width.data,
                'height': form.height.data,
                'charge': form.charge.data,
                'distance': form.distance.data}},
        json_data=Network.get_network_json(
            {c.name: getattr(form, c.name).data for c in classes},
            bool(form.orphans.data),
            dimensions),
        title=_('model'),
        crumbs=[
            _('network visualization'),
            f'{dimensions}D' if dimensions else _('classic')])
