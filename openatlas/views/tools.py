from typing import Any

from flask import flash, g, json, render_template, request, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.tab import Tab
from openatlas.display.util import (
    button, display_info, link, remove_link, required_group)
from openatlas.display.util2 import is_authorized, manual
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.entity import Entity, Link
from openatlas.models.tools import (
    SexEstimation, get_carbon_link, get_sex_types, update_carbon)


def name_result(result: float) -> str:
    # Needed for translations
    _('female')
    _('likely female')
    _('indifferent')
    _('likely male')
    _('male')
    _('corresponds to')
    for label, value in SexEstimation.result.items():
        if result < value:
            return _(label)
    return ''  # pragma: no cover


def start_crumbs(entity: Entity) -> list[Any]:
    crumbs: list[Any] = [[_('place'), url_for('index', view='place')]]
    for super_ in entity.get_structure()['supers']:
        crumbs.append(link(super_))
    crumbs.append(entity)
    return crumbs


def sex_result(entity: Entity) -> str:
    calculation = SexEstimation.calculate(entity)
    if calculation is None:
        return ''
    return \
        '<h1 class="uc-first">' + _('sex estimation') + '</h1>' \
        'Ferembach et al. 1979: ' \
        f'<span class="anthro-result">{calculation}</span> - ' + \
        _('corresponds to') + f' "{name_result(calculation)}"'


def carbon_result(entity: Entity) -> str:
    if link_ := get_carbon_link(entity):
        return '<h1 class="uc-first">' + _('radiocarbon dating') + '</h1>' + \
            display_info(json.loads(link_.description))
    return ''


@app.route('/tools/index/<int:id_>')
@required_group('readonly')
def tools_index(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_)
    tabs = {
        'info': Tab(
            'info',
            content=carbon_result(entity) + sex_result(entity),
            buttons=[
                manual('tools/anthropological_analyses'),
                button(
                    _('radiocarbon dating'),
                    url_for('carbon', id_=entity.id)),
                button(_('sex estimation'), url_for('sex', id_=entity.id))])}
    return render_template(
        'tabs.html',
        tabs=tabs,
        entity=entity,
        crumbs=start_crumbs(entity) + [_('tools')])


@app.route('/tools/sex/<int:id_>')
@required_group('readonly')
def sex(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_, types=True)
    buttons = [manual('tools/anthropological_analyses')]
    types = SexEstimation.get_types(entity)
    if is_authorized('contributor'):
        buttons.append(button(_('edit'), url_for('sex_update', id_=entity.id)))
        if types:
            buttons.append(button(
                _('delete'),
                url_for('sex_delete', id_=id_),
                onclick="return confirm('" + _('delete') + "?')"))
    data = []
    for item in types:
        type_ = g.types[item['id']]
        feature = SexEstimation.features[type_.name]
        data.append({
            'name': type_.name,
            'category': feature['category'],
            'feature_value': feature['value'],
            'option_value': SexEstimation.options[item['description']],
            'value': item['description']})
    return render_template(
        'tabs.html',
        entity=entity,
        tabs={
            'info': Tab(
                'sex estimation',
                content=render_template(
                    'tools/sex.html',
                    data=data,
                    result=sex_result(entity)),
                buttons=buttons)},
        crumbs=start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            _('sex estimation')])


@app.route('/tools/sex/delete/<int:id_>')
@required_group('contributor')
def sex_delete(id_: int) -> str | Response:
    try:
        Transaction.begin()
        for dict_ in get_sex_types(id_):
            Link.delete_(dict_['link_id'])
        Transaction.commit()
    except Exception as e:  # pragma: no cover
        Transaction.rollback()
        g.logger.log('error', 'database', 'transaction failed', e)
        flash(_('error transaction'), 'error')
    return redirect(url_for('tools_index', id_=id_))


@app.route('/tools/sex/update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def sex_update(id_: int) -> str | Response:

    class Form(FlaskForm):
        pass

    entity = Entity.get_by_id(id_, types=True)
    choices = [(option, option) for option in SexEstimation.options]
    for feature, values in SexEstimation.features.items():
        description = ''
        if values['female'] or values['male']:
            description = f"Female: {values['female']}, male: {values['male']}"
        setattr(
           Form,
           feature,
           SelectField(
               f"{feature} ({values['category']})",
               choices=choices,
               default='Not preserved',
               description=description))
    setattr(Form, 'save', SubmitField(_('save')))
    form = Form()
    if form.validate_on_submit():
        data = form.data
        data.pop('save', None)
        data.pop('csrf_token', None)
        try:
            Transaction.begin()
            SexEstimation.save(entity, data)
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('sex', id_=entity.id))

    for item in get_sex_types(entity.id):
        getattr(form, g.types[item['id']].name).data = item['description']
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'sex estimation',
                content=display_form(
                    form,
                    manual_page='tools/anthropological_analyses'))},
        entity=entity,
        crumbs=start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            [_('sex estimation'), url_for('sex', id_=entity.id)],
            _('edit')])


@app.route('/tools/carbon/<int:id_>')
@required_group('readonly')
def carbon(id_: int) -> str | Response:
    entity = Entity.get_by_id(id_, types=True)
    buttons = [manual('tools/radiocarbon_dating')]
    if is_authorized('contributor'):
        buttons.append(
            button(_('edit'), url_for('carbon_update', id_=entity.id)))
        if link_ := get_carbon_link(entity):
            buttons.append(
                str(remove_link(_('radiocarbon dating'), link_, entity)))
    return render_template(
        'tabs.html',
        entity=entity,
        tabs={
            'info': Tab(
                'radiocarbon dating',
                content=carbon_result(entity),
                buttons=buttons)},
        crumbs=start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            _('radiocarbon dating')])


@app.route('/tools/carbon/update/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def carbon_update(id_: int) -> str | Response:

    class Form(FlaskForm):
        lab_id = StringField(
            f"{_('laboratory')} {_('ID')}",
            [InputRequired()],
            render_kw={'placeholder': 'VERA'})
        spec_id = StringField(
            f"{_('specimen')} {_('ID')}",
            [InputRequired()],
            render_kw={'placeholder': '23432A'})
        radiocarbon_year = IntegerField(
            _('radiocarbon year'),
            [InputRequired()],
            render_kw={'placeholder': '2040'})
        range = IntegerField(
            _('range'),
            [InputRequired()],
            render_kw={'placeholder': '30'})
        save = SubmitField(_('save'))

    entity = Entity.get_by_id(id_)
    form = Form()
    carbon_link = get_carbon_link(entity)
    if form.validate_on_submit():
        update_carbon(
            entity,
            data={
                'labId': form.lab_id.data,
                'specId': form.spec_id.data,
                'radiocarbonYear': form.radiocarbon_year.data,
                'range': form.range.data,
                'timeScale': 'BP'},
            link_=carbon_link)
        flash(_('info update'), 'info')
        return redirect(url_for('tools_index', id_=entity.id))
    if request.method == 'GET' and carbon_link:
        data = json.loads(carbon_link.description)
        form.lab_id.data = data['labId']
        form.spec_id.data = data['specId']
        form.radiocarbon_year.data = data['radiocarbonYear']
        form.range.data = data['range']
    return render_template(
        'tabs.html',
        entity=entity,
        tabs={'info': Tab('radiocarbon dating', content=display_form(form))},
        crumbs=start_crumbs(entity) + [
            [_('tools'), url_for('tools_index', id_=entity.id)],
            [_('radiocarbon dating'), url_for('carbon_update', id_=entity.id)],
            _('edit')])
