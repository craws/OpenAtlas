from typing import Union

from flask import g, render_template, url_for
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import SelectField, SubmitField

from openatlas import app
from openatlas.models.anthropology import SexEstimation
from openatlas.models.entity import Entity
from openatlas.models.type import Type
from openatlas.util.table import Table
from openatlas.util.util import button, is_authorized, required_group, uc_first


@app.route('/anthropology/index/<int:id_>')
@required_group('readonly')
def anthropology_index(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    return render_template(
        'anthropology/index.html',
        entity=entity,
        crumbs=[entity, _('anthropological analyzes')])


@app.route('/anthropology/sex/<int:id_>')
@required_group('readonly')
def anthropology_sex(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_, types=True)
    buttons = []
    if is_authorized('contributor'):
        buttons.append(
            button(
                _('edit'),
                url_for('anthropology_sex_update', id_=entity.id)))
    type_ids = SexEstimation.get_types(entity)
    table = Table(
        ['name', 'value'],
        rows=[[g.types[data['id']].name, data['description']] for data in type_ids])
    return render_template(
        'anthropology/sex.html',
        entity=entity,
        buttons=buttons,
        table=table,
        crumbs=[
            entity,
            [_('anthropological analyzes'),
             url_for('anthropology_index', id_=entity.id)],
            _('sex estimation')])


@app.route('/anthropology/sex/update/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def anthropology_sex_update(id_: int) -> Union[str, Response]:

    class Form(FlaskForm):
        pass

    entity = Entity.get_by_id(id_, types=True)

    choices = [(option, option) for option in SexEstimation.options.keys()]
    for features in SexEstimation.features.values():
        for feature, values in features.items():
            label = uc_first(feature.replace('_', ' '))
            description = ''
            if values['female'] or values['male']:
                description = \
                    f"Female: {values['female']}, male: {values['male']}"
            setattr(
                Form,
                feature,
                SelectField(
                    label,
                    choices=choices,
                    default='Not preserved',
                    description=description))
    setattr(Form, 'save', SubmitField(_('save')))

    form = Form()

    #  Add type information to features
    for group_id in Type.get_types('Features for sexing'):
        group = g.types[group_id]
        for type_id in group.subs:
            type_ = g.types[type_id]
            SexEstimation.features[group.name][type_.name]['type_id'] = type_.id

    if form.validate_on_submit():
        data = form.data
        data.pop('save')
        data.pop('csrf_token')
        SexEstimation.save(entity, data)
        return redirect(url_for('anthropology_sex', id_=entity.id))

    # Fill in data
    for type_, value in entity.types.items():
        getattr(form, type_.name).data = value

    return render_template(
        'anthropology/sex_update.html',
        entity=entity,
        form=form,
        crumbs=[
            entity,
            [_('anthropological analyzes'),
             url_for('anthropology_index', id_=entity.id)],
            [_('sex estimation'), url_for('anthropology_sex', id_=entity.id)],
            _('edit')])
