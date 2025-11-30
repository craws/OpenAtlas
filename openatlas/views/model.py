import re
from typing import Optional

from flask import g, render_template, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, IntegerField, SelectField, SelectMultipleField, StringField,
    widgets)
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.display.table import Table
from openatlas.display.util import button, link, required_group
from openatlas.display.util2 import manual, uc_first
from openatlas.forms.field import SubmitField
from openatlas.forms.form import cidoc_form
from openatlas.models.entity import Entity
from openatlas.models.network import Network
from openatlas.models.openatlas_class import (
    get_class_count, get_db_relations, get_model_relations)


@app.route('/overview/model', methods=['GET', 'POST'])
@required_group('readonly')
def model_index() -> str:
    form = cidoc_form()
    result = None
    if form.validate_on_submit():
        domain = g.cidoc_classes[form.domain.data]
        range_ = g.cidoc_classes[form.range.data]
        property_ = g.properties[form.property.data]
        result = {
            'domain': domain,
            'property': property_,
            'range': range_,
            'domain_valid':
                property_.find_object('domain_class_code', domain.code),
            'range_valid':
                property_.find_object('range_class_code', range_.code)}
    relations = get_model_relations()
    invalid_relations = Table(['domain', 'property', 'range'])
    for row in get_db_relations():
        if row['property_code'] in ['P1'] or row['domain'] == 'type_tools' \
                or (row['property_code'] == 'P2'
                    and row['range'] == 'type') \
                or (row['property_code'] == 'P67'
                    and row['domain'] == 'reference_system') \
                or (row['property_code'] == 'P53'
                    and row['range'] == 'object_location'):
            continue
        if row['domain'] not in relations \
                or row['range'] not in relations[row['domain']] \
                or row['property_code'] \
                not in relations[row['domain']][row['range']]:
            invalid_relations.rows.append([
                g.classes[row['domain']].label,
                row['property_code'],
                g.classes[row['range']].label])  # pragma: no cover
    model_relations = Table(['domain', 'property', 'range', 'count'])
    for domain, data in relations.items():
        for range_, range_data in data.items():
            for property_, count in range_data.items():
                model_relations.rows.append([
                    g.classes[domain].label,
                    property_,
                    g.classes[range_].label,
                    count])
    return render_template(
        'model/index.html',
        form=form,
        result=result,
        title=_('model'),
        tables={
            'model_relations': model_relations,
            'invalid_relations': invalid_relations},
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
        _('group'),
        _('write access'),
        _('reference system'),
        'add type',
        'count'],
        defs=[
            {'orderDataType': 'cidoc-model', 'targets': [1]},
            {'sType': 'numeric', 'targets': [1]}])
    class_count = get_class_count()
    for class_ in g.classes.values():
        table.rows.append([
            class_.label,
            link(class_.cidoc_class),
            link(g.types[class_.standard_type_id])
            if class_.standard_type_id else '',
            uc_first(_((class_.group['name'].replace("_", " "))))
            if class_.group.get('name') else '',
            class_.write_access,
            _('allowed') if 'reference_system' in class_.extra else '',
            _('allowed') if class_.new_types_allowed else '',
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
    width = IntegerField(
        _('width'),
        default=1200,
        validators=[InputRequired()])
    height = IntegerField(
        _('height'),
        default=600,
        validators=[InputRequired()])
    charge = IntegerField(
        _('charge'),
        default=-80,
        validators=[InputRequired()])
    distance = IntegerField(
        _('distance'),
        default=80,
        validators=[InputRequired()])
    orphans = BooleanField(_('orphans'), default=False)
    depth = SelectField(
        _('depth'),
        default=1,
        choices=[(x, str(x)) for x in range(1, 13)])
    # noinspection PyTypeChecker
    classes = SelectMultipleField(
        _('colors'),
        widget=widgets.ListWidget(prefix_label=False))


@app.route('/overview/network/', methods=['GET', 'POST'])
@app.route('/overview/network/<int:dimensions>', methods=['GET', 'POST'])
@app.route(
    '/overview/network/<int:dimensions>/<int:id_>',
    methods=['GET', 'POST'])
@required_group('readonly')
def network(dimensions: Optional[int] = 0, id_: Optional[int] = None) -> str:
    entity = Entity.get_by_id(id_) if id_ else None
    render_kw = {
       'data-huebee': True,
       'class': f'data-huebee {app.config["CSS"]["string_field"]}'}
    classes = []
    for class_ in g.classes.values():
        color = class_.display.get('network_color')
        if class_.name == 'object_location':
            color = g.classes['place'].display.get('network_color')
        if color:
            classes.append(class_)
            setattr(
                NetworkForm,
                class_.name,
                StringField(default=color, render_kw=render_kw))
    setattr(NetworkForm, 'save', SubmitField(_('apply')))
    form = NetworkForm()
    form.classes.choices = [
        (class_.name, class_.label)
        for class_ in [x for x in classes if x.name != 'object_location']]
    colors = {}
    for class_ in classes:
        color_code = class_.display.get('network_color')
        if re.match(r"^(#)?[A-Fa-f0-9]+$", getattr(form, class_.name).data):
            color_code = getattr(form, class_.name).data
        colors[class_.name] = color_code
        getattr(form, class_.name).data = color_code
    if entity:
        json_data = Network.get_ego_network_json(
            colors,
            entity.id,
            int(form.depth.data),
            dimensions)
        crumbs = [link(entity, index=True), entity, _('network')]
    else:
        json_data = Network.get_network_json(
            colors,
            bool(form.orphans.data),
            dimensions)
        crumbs = [
            _('network visualization'),
            f'{dimensions}D' if dimensions else _('classic')]
    buttons = [manual('tools/network')]
    if json_data:
        if dimensions:
            buttons.append(
                button('classic', url_for('network', dimensions=0, id_=id_)))
        if dimensions != 2:
            buttons.append(
                button('2D', url_for('network', dimensions=2, id_=id_)))
        if dimensions != 3:
            buttons.append(
                button('3D', url_for('network', dimensions=3, id_=id_)))
        if not dimensions:
            buttons.append(
                button(
                    _('download'),
                    '#',
                    onclick="saveSvgAsPng("
                    "d3.select('#network-svg').node(), 'network.png')"))
    return render_template(
        'model/network.html',
        form=form,
        dimensions=dimensions,
        entity=entity,
        buttons=buttons,
        network_params={
            'classes': {},
            'options': {
                'width': form.width.data,
                'height': form.height.data,
                'charge': form.charge.data,
                'distance': form.distance.data}},
        json_data=json_data,
        title=_('model'),
        crumbs=crumbs)
