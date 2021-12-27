import ast
from typing import Union

from flask import flash, render_template, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app, logger
from openatlas.database.connect import Transaction
from openatlas.forms.form import build_form
from openatlas.forms.util import get_link_type, process_form_dates
from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.util.util import required_group, uc_first


@app.route('/relation/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def relation_insert(origin_id: int) -> Union[str, Response]:
    origin = Entity.get_by_id(origin_id)
    form = build_form('actor_actor_relation')
    form.relation_origin_id.data = origin.id
    if form.validate_on_submit():
        Transaction.begin()
        try:
            for actor in Entity.get_by_ids(ast.literal_eval(form.actor.data)):
                if form.inverse.data:
                    link_ = Link.get_by_id(
                        actor.link('OA7', origin, form.description.data)[0])
                else:
                    link_ = Link.get_by_id(
                        origin.link('OA7', actor, form.description.data)[0])
                link_.set_dates(process_form_dates(form))
                link_.type = get_link_type(form)
                link_.update()
            Transaction.commit()
            flash(_('entity created'), 'info')
        except Exception as e:  # pragma: no cover
            Transaction.rollback()
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            return redirect(url_for('relation_insert', origin_id=origin_id))
        return redirect(f"{url_for('view', id_=origin.id)}#tab-relation")
    return render_template(
        'display_form.html',
        form=form,
        title=_('relation'),
        crumbs=[
            [_('actor'), url_for('index', view='actor')],
            origin,
            f"+ {uc_first(_('relation'))}"])
