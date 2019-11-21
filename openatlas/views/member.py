# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast
from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import HiddenField, SubmitField, TextAreaField
from wtforms.validators import InputRequired

from openatlas import app, logger
from openatlas.forms.forms import DateForm, TableMultiField, build_form, get_link_type
from openatlas.models.entity import EntityMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import required_group


class MemberForm(DateForm):
    actor = TableMultiField(_('actor'), [InputRequired()])
    group = TableMultiField(_('actor'), [InputRequired()])
    origin_id = HiddenField()
    description = TextAreaField(_('description'))
    save = SubmitField(_('insert'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()

    def validate(self) -> bool:
        valid = DateForm.validate(self)
        if hasattr(self, 'actor') and self.actor is not None:
            if self.origin_id.data in ast.literal_eval(self.actor.data):
                self.actor.errors.append(_("Can't link to itself."))
                valid = False
        if hasattr(self, 'group') and self.group is not None:
            if self.origin_id.data in ast.literal_eval(self.group.data):
                self.group.errors.append(_("Can't link to itself."))
                valid = False
        return valid


@app.route('/membership/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def membership_insert(origin_id: int) -> Union[str, Response]:
    origin = EntityMapper.get_by_id(origin_id)
    form = build_form(MemberForm, 'Member')
    del form.actor
    form.origin_id.data = origin.id
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            for actor in EntityMapper.get_by_ids(ast.literal_eval(form.group.data)):
                link_ = LinkMapper.get_by_id(actor.link('P107', origin, form.description.data))
                link_.set_dates(form)
                link_.type = get_link_type(form)
                link_.update()
            g.cursor.execute('COMMIT')
            flash(_('entity created'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if form.continue_.data == 'yes':
            return redirect(url_for('membership_insert', origin_id=origin_id))
        return redirect(url_for('actor_view', id_=origin.id) + '#tab-member-of')
    return render_template('member/insert.html', origin=origin, form=form)


@app.route('/member/insert/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def member_insert(origin_id: int) -> Union[str, Response]:
    origin = EntityMapper.get_by_id(origin_id)
    form = build_form(MemberForm, 'Member')
    del form.group
    form.origin_id.data = origin.id
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            for actor in EntityMapper.get_by_ids(ast.literal_eval(form.actor.data)):
                link_ = LinkMapper.get_by_id(
                    origin.link('P107', actor, form.description.data))
                link_.set_dates(form)
                link_.type = get_link_type(form)
                link_.update()
            g.cursor.execute('COMMIT')
            flash(_('entity created'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        if form.continue_.data == 'yes':
            return redirect(url_for('member_insert', origin_id=origin_id))
        return redirect(url_for('actor_view', id_=origin.id) + '#tab-member')
    return render_template('member/insert.html', origin=origin, form=form)


@app.route('/member/update/<int:id_>/<int:origin_id>', methods=['POST', 'GET'])
@required_group('contributor')
def member_update(id_: int, origin_id: int) -> Union[str, Response]:
    link_ = LinkMapper.get_by_id(id_)
    domain = EntityMapper.get_by_id(link_.domain.id)
    range_ = EntityMapper.get_by_id(link_.range.id)
    origin = range_ if origin_id == range_.id else domain
    form = build_form(MemberForm, 'Member', link_, request)
    del form.actor, form.group, form.insert_and_continue
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            link_.delete()
            link_ = LinkMapper.get_by_id(domain.link('P107', range_, form.description.data))
            link_.set_dates(form)
            link_.type = get_link_type(form)
            link_.update()
            g.cursor.execute('COMMIT')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        tab = '#tab-member-of' if origin.id == range_.id else '#tab-member'
        return redirect(url_for('actor_view', id_=origin.id) + tab)
    form.save.label.text = _('save')
    form.populate_dates(link_)
    related = range_ if origin_id == domain.id else domain
    return render_template('member/update.html', origin=origin, form=form, related=related)
