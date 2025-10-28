import ast
from typing import Optional

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.util import hierarchy_crumbs, link, required_group
from openatlas.display.util2 import uc_first
from openatlas.forms.display import display_form
from openatlas.forms.entity_form import process_dates
from openatlas.forms.form import (
    link_detail_form, link_form, link_update_form)
from openatlas.models.entity import Entity, Link


@app.route('/link/delete/<int:id_>/<int:origin_id>', methods=['GET', 'POST'])
@required_group('contributor')
def link_delete(id_: int, origin_id: int) -> Response:
    Link.delete_(id_)
    flash(_('link removed'), 'info')
    return redirect(url_for('view', id_=origin_id))


@app.route(
    '/link/insert/<int:origin_id>/<relation_name>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_insert(origin_id: int, relation_name: str) -> str | Response:
    origin = Entity.get_by_id(origin_id)
    relation = origin.class_.relations[relation_name]
    form = link_form(origin, relation)
    if form.validate_on_submit():
        if request.form['checkbox_values']:
            origin.link_string(
                relation['property'],
                request.form['checkbox_values'],
                inverse=relation['inverse'])
        return redirect(
            f"{url_for('view', id_=origin.id)}#tab-" +
            relation_name.replace('_', '-'))
    return render_template(
        'content.html',
        content=display_form(form, 'checkbox-form'),
        title=relation['label'],
        crumbs=hierarchy_crumbs(origin) + [
            link(origin),
            f"+ {uc_first(relation['label'])}"])


@app.route(
    '/link/insert_detail/<int:origin_id>/<relation_name>',
    methods=['GET', 'POST'])
@app.route(
    '/link/insert_detail/<int:origin_id>/<relation_name>/<selection_id>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_insert_detail(
        origin_id: int,
        relation_name: str,
        selection_id: Optional[int] = None) -> str | Response:
    print(relation_name)
    origin = Entity.get_by_id(origin_id)
    relation = origin.class_.relations[relation_name]
    form = link_detail_form(origin, relation, selection_id)
    if form.validate_on_submit():
        ids = ast.literal_eval(getattr(form, relation_name).data)
        ids = ids if isinstance(ids, list) else [int(ids)]
        type_id = None
        if 'type' in relation:
            hierarchy = Entity.get_hierarchy(relation['type'])
            type_id = getattr(form, str(hierarchy.id)).data or None
        origin.link(
            relation['property'],
            Entity.get_by_ids(ids),
            form.description.data if 'description' in form else None,
            relation['inverse'],
            type_id,
            dates=process_dates(form))
        return redirect(
            f"{url_for('view', id_=origin.id)}#tab-" +
            relation_name.replace('_', '-'))
    return render_template(
        'content.html',
        content=display_form(form),
        title=_(origin.class_.group['name']),
        crumbs=[
            link(origin, index=True),
            origin,
            '+ ' + uc_first(relation['label'])])


@app.route(
    '/link/update/<int:id_>/<int:origin_id>/<relation>',
    methods=['GET', 'POST'])
@required_group('contributor')
def link_update(id_: int, origin_id: int, relation: str) -> str | Response:
    link_ = Link.get_by_id(id_)
    domain = Entity.get_by_id(link_.domain.id)
    range_ = Entity.get_by_id(link_.range.id)
    origin = domain if origin_id == domain.id else range_
    target = range_ if origin_id == domain.id else domain
    relation = origin.class_.relations[relation]
    form = link_update_form(link_, relation)
    origin_url = (
        f"{url_for('view', id_=origin.id)}#tab-" +
        relation['name'].replace('_', '-'))
    if form.validate_on_submit():
        data = {
            'description': form.description.data
            if hasattr(form, 'description') else None}
        if 'type' in relation:
            hierarchy = Entity.get_hierarchy(relation['type'])
            data['type_id'] = getattr(form, str(hierarchy.id)).data or None
        data.update(process_dates(form))
        try:
            link_.update(data)
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            g.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(origin_url)
    return render_template(
        'content.html',
        content=display_form(form),
        crumbs=[
            link(origin, index=True),
            link(origin.name, origin_url),
            target,
            _('edit')])
