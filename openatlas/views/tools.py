from typing import Union

from flask import flash, g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.util import (
    button, display_form, is_authorized, manual, required_group, uc_first)
from openatlas.models.tools import SexEstimation, get_sex_types, update_carbon
from openatlas.models.entity import Entity


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


def print_sex_result(entity: Entity) -> str:
    calculation = SexEstimation.calculate(entity)
    if calculation is None:
        return ''
    return \
        'Ferembach et al. 1979: ' \
        f'<span class="anthro-result">{calculation}</span>' \
        f' - {_("corresponds to")} "{name_result(calculation)}"'


@app.route('/anthropology/index/<int:id_>')
@required_group('readonly')
def tools_index(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    dating_buttons = [
        button(
            _('radiocarbon dating'),
            url_for('carbon_update', id_=entity.id))]
    sex_buttons = [
        manual('tools/anthropological_analyses'),
        button(_('sex estimation'), url_for('sex', id_=entity.id)),
        print_sex_result(entity)]
    return render_template(
        'content.html',
        entity=entity,
        buttons=dating_buttons + sex_buttons,
        crumbs=[entity, _('anthropological analyses')])


@app.route('/tools/sex/<int:id_>')
@required_group('readonly')
def sex(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, types=True)
    buttons = [manual('tools/anthropological_analyses')]
    if is_authorized('contributor'):
        buttons.append(button(_('edit'), url_for('sex_update', id_=entity.id)))
    data = []
    for item in SexEstimation.get_types(entity):
        type_ = g.types[item['id']]
        feature = SexEstimation.features[type_.name]
        data.append({
            'name': type_.name,
            'category': feature['category'],
            'feature_value': feature['value'],
            'option_value': SexEstimation.options[item['description']],
            'value': item['description']})
    return render_template(
        'tools/sex.html',
        entity=entity,
        buttons=buttons,
        data=data,
        result=print_sex_result(entity),
        crumbs=[
            entity,
            [_('tools'), url_for('tools_index', id_=entity.id)],
            _('sex estimation')])


@app.route('/anthropology/sex/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def sex_update(id_: int) -> Union[str, Response]:

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
               f"{uc_first(feature.replace('_', ' '))} ({values['category']})",
               choices=choices,
               default='Not preserved',
               description=description))
    setattr(Form, 'save', SubmitField(_('save')))
    form = Form()
    types = get_sex_types(entity.id)
    if form.validate_on_submit():
        data = form.data
        data.pop('save', None)
        data.pop('csrf_token', None)
        try:
            Transaction.begin()
            SexEstimation.save(entity, data, types)
            Transaction.commit()
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('sex', id_=entity.id))

    for dict_ in types:
        getattr(form, g.types[dict_['id']].name).data = dict_['description']
    return render_template(
        'content.html',
        content=display_form(
            form,
            manual_page='tools/anthropological_analyses'),
        entity=entity,
        crumbs=[
            entity,
            [_('tools'), url_for('tools_index', id_=entity.id)],
            [_('sex estimation'), url_for('sex', id_=entity.id)],
            _('edit')])


@app.route('/tools/carbon/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def carbon_update(id_: int) -> Union[str, Response]:

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
    if form.validate_on_submit():
        update_carbon(
            entity,
            data={
                'labId': form.lab_id.data,
                'specId': form.spec_id.data,
                'radiocarbonYear': form.radiocarbon_year.data,
                'range': form.range.data,
                'timeScale': 'BP'})

    return render_template(
        'content.html',
        entity=entity,
        content=display_form(form),
        crumbs=[
            entity,
            [_('tools'), url_for('tools_index', id_=entity.id)],
            [_('radiocarbon dating'), url_for('carbon_update', id_=entity.id)],
            _('edit')])
