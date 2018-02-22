# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from wtforms import BooleanField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, TableMultiField, build_form
from openatlas.models.date import DateMapper
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.models.node import NodeMapper
from openatlas.util.util import required_group


class RelationForm(DateForm):
    inverse = BooleanField(_('inverse'))
    actor = TableMultiField(_('actor'), [InputRequired()])
    origin_id = HiddenField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()

    def validate(self, extra_validators=None):
        valid = DateForm.validate(self)
        if hasattr(self, 'origin_id') and self.origin_id is not None:
            if self.origin_id.data in ast.literal_eval(self.actor.data):
                self.actor.errors.append(_("Can't link to itself."))
                valid = False
        return valid


@app.route('/relation/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def relation_insert(origin_id):
    origin = EntityMapper.get_by_id(origin_id)
    form = build_form(RelationForm, 'Actor Actor Relation')
    form.origin_id.data = origin.id
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            for actor_id in ast.literal_eval(form.actor.data):
                if form.inverse.data:
                    link_id = LinkMapper.insert(actor_id, 'OA7', origin.id, form.description.data)
                else:
                    link_id = origin.link('OA7', actor_id, form.description.data)
                DateMapper.save_link_dates(link_id, form)
                NodeMapper.save_link_nodes(link_id, form)
            g.cursor.execute('COMMIT')
            flash(_('entity created'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if form.continue_.data == 'yes':
            return redirect(url_for('relation_insert', origin_id=origin_id))
        return redirect(url_for('actor_view', id_=origin.id) + '#tab-relation')
    return render_template('relation/insert.html', origin=origin, form=form)


@app.route('/relation/update/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('editor')
def relation_update(id_, origin_id):
    link_ = LinkMapper.get_by_id(id_)
    domain = EntityMapper.get_by_id(link_.domain.id)
    range_ = EntityMapper.get_by_id(link_.range.id)
    origin = range_ if origin_id == range_.id else domain
    related = range_ if origin_id == domain.id else domain
    form = build_form(RelationForm, 'Actor Actor Relation', link_, request)
    del form.actor, form.insert_and_continue, form.origin_id
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            link_.delete()
            if form.inverse.data:
                link_id = related.link('OA7', origin, form.description.data)
            else:
                link_id = origin.link('OA7', related, form.description.data)
            DateMapper.save_link_dates(link_id, form)
            NodeMapper.save_link_nodes(link_id, form)
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('actor_view', id_=origin.id) + '#tab-relation')
    if origin.id == range_.id:
        form.inverse.data = True
    form.save.label.text = _('save')
    link_.set_dates()
    form.populate_dates(link_)
    return render_template('relation/update.html', origin=origin, form=form, related=related)
