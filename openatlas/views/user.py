from typing import Any, Optional

import bcrypt
from flask import abort, flash, g, render_template, request, url_for
from flask_babel import format_number, lazy_gettext as _
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (
    BooleanField, HiddenField, PasswordField, SelectField, StringField,
    TextAreaField, validators)
from wtforms.validators import Email, InputRequired

from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, description, display_info, link, required_group, send_mail)
from openatlas.display.util2 import (
    format_date, is_authorized, manual, sanitize, uc_first)
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField, generate_password_field
from openatlas.models.entity import Entity
from openatlas.models.user import User


class UserForm(FlaskForm):
    user_id: Optional[int] = None
    active = BooleanField(_('active'), default=True)
    username: Any = StringField(
        _('username'),
        [InputRequired()],
        render_kw={'autofocus': True})
    group = SelectField(_('group'), choices=[])
    email: Any = StringField(_('email'), [InputRequired(), Email()])
    password: Any = PasswordField(_('password'), [InputRequired()])
    password2: Any = PasswordField(_('repeat password'), [InputRequired()])
    generate_password = generate_password_field()
    show_passwords = BooleanField(_('show passwords'))
    real_name = StringField(_('full name'), description=_('tooltip full name'))
    description = TextAreaField(_('info'))
    send_info = BooleanField(_('send account information'))
    save = SubmitField(_('save'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()

    def validate(self, extra_validators: validators = None) -> bool:
        valid = FlaskForm.validate(self)
        username = ''
        user_email = ''
        if self.user_id and (user := User.get_by_id(self.user_id)):
            username = user.username
            user_email = user.email
        if username != self.username.data \
                and User.get_by_username(self.username.data):
            self.username.errors.append(_('error username exists'))
            valid = False
        if user_email != self.email.data \
                and User.get_by_email(self.email.data):
            self.email.errors.append(_('error email exists'))
            valid = False
        if getattr(self, 'password'):
            if self.password.data != self.password2.data:
                self.password.errors.append(_('error passwords must match'))
                self.password2.errors.append(_('error passwords must match'))
                valid = False
            if len(self.password.data) < g.settings['minimum_password_length']:
                self.password.errors.append(_('error password too short'))
                valid = False
        return valid


class ActivityForm(FlaskForm):
    action_choices = (
        ('all', _('all')),
        ('insert', _('insert')),
        ('update', _('update')),
        ('delete', _('delete')))
    limit = SelectField(
        _('limit'),
        choices=((0, _('all')), (100, 100), (500, 500)),
        default=100,
        coerce=int)
    user = SelectField(
        _('user'),
        choices=([(0, _('all'))]),
        default=0,
        coerce=int)
    action = SelectField(_('action'), choices=action_choices, default='all')
    save = SubmitField(_('apply'))


@app.route('/user/activity', methods=['GET', 'POST'])
@app.route('/user/activity/<int:user_id>', methods=['GET', 'POST'])
@app.route(
    '/user/activity/<int:user_id>/<int:entity_id>',
    methods=['GET', 'POST'])
@required_group('readonly')
def user_activity(user_id: int = 0, entity_id: Optional[int] = None) -> str:
    form = ActivityForm()
    form.user.choices = [(0, _('all'))] + User.get_users_for_form()
    limit = 100
    user_id = user_id or 0
    action = 'all'
    if form.validate_on_submit():
        limit = int(form.limit.data)
        user_id = int(form.user.data)
        action = form.action.data
    form.user.data = user_id
    table = Table(
        ['date', 'user', 'action', 'class', 'entity'],
        order=[[0, 'desc']])
    for row in User.get_activities(limit, user_id, action, entity_id):
        try:
            entity = Entity.get_by_id(row['entity_id'])
            entity_name = link(entity)
        except AttributeError:  # Entity already deleted
            entity = None
            entity_name = f"id {row['entity_id']}"
        user = User.get_by_id(row['user_id'])
        table.rows.append([
            format_date(row['created']),
            link(user) if user else f"id {row['user_id']}",
            _(row['action']),
            entity.class_.label if entity else '',
            entity_name])
    return render_template(
        'content.html',
        content=display_form(form) + table.display(),
        title=_('user'),
        crumbs=[[_('user'), url_for('admin_index')], _('activity')])


@app.route('/user/view/<int:id_>')
@required_group('readonly')
def user_view(id_: int) -> str:
    user = User.get_by_id(id_)
    if not user:
        abort(404)
    count = ''
    if x := User.get_created_entities_count(user.id):
        count = link(format_number(x), url_for("user_entities", id_=user.id))
    info = {
        _('username'): user.username,
        _('group'): user.group,
        _('full name'): user.real_name,
        _('email'):
            user.email
            if is_authorized('manager') or user.settings['show_email'] else '',
        _('created entities'): count,
        _('activity'):
            link(_('log'),  url_for('user_activity', user_id=user.id)),
        _('language'): user.settings['language'],
        _('last login'): format_date(user.login_last_success),
        _('failed logins'):
            user.login_failed_count if is_authorized('manager') else ''}
    buttons = [manual('admin/user')]
    if is_authorized('manager'):
        if user.group != 'admin' or current_user.group == 'admin':
            buttons.append(
                button(_('edit'), url_for('user_update', id_=user.id)))
        if user.id != current_user.id and (
                user.group != 'admin' or current_user.group == 'admin'):
            name = user.username.replace('"', '').replace("'", '')
            buttons.append(
                button(
                    _('delete'),
                    f"{url_for('user_delete', id_=user.id)}#tab-user",
                    onclick=""
                    f"return confirm('{_('Delete %(name)s?', name=name)}')"))
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'info',
                content=display_info(info) + description(user.description),
                buttons=buttons)},
        title=user.username,
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-user"],
            user.username])


@app.route('/user/delete/<int:id_>')
@required_group('manager')
def user_delete(id_: int) -> Response:
    user = User.get_by_id(id_)
    if not user \
            or user.id == current_user.id \
            or (user.group == 'admin' and not is_authorized('admin')):
        abort(403)
    user.delete()
    flash(_('user deleted'), 'info')
    return redirect(f"{url_for('admin_index')}#tab-user")


@app.route('/user/entities/<int:id_>')
@required_group('readonly')
def user_entities(id_: int) -> str:
    table = Table([
        'name',
        'class',
        'type',
        'begin',
        'end',
        'created'])
    if user := User.get_by_id(id_):
        for entity in user.get_entities():
            table.rows.append([
                link(entity),
                entity.class_.label,
                link(entity.standard_type),
                entity.first,
                entity.last,
                format_date(entity.created)])
    return render_template(
        'content.html',
        content=table.display(),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-user"],
            user,
            _('created entities')])


@app.route('/user/update/<int:id_>', methods=['GET', 'POST'])
@required_group('manager')
def user_update(id_: int) -> str | Response:
    user = User.get_by_id(id_)
    if not user:
        abort(404)
    if user.group == 'admin' and current_user.group != 'admin':
        abort(403)
    form = UserForm(obj=user)
    form.user_id = id_
    del (
        form.password,
        form.password2,
        form.send_info,
        form.insert_and_continue,
        form.show_passwords,
        form.generate_password)
    form.group.choices = get_groups()
    if user and form.validate_on_submit():
        # Active is always True for current user to prevent self deactivation
        user.active = True if user.id == current_user.id else form.active.data
        user.real_name = form.real_name.data
        user.username = form.username.data
        user.email = form.email.data
        user.description = form.description.data
        user.group = form.group.data
        user.update()
        flash(_('info update'), 'info')
        return redirect(url_for('user_view', id_=id_))
    if user.id == current_user.id:
        del form.active
    return render_template(
        'content.html',
        content=display_form(form, manual_page='admin/user'),
        title=user.username,
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-user"],
            user,
            _('edit')])


@app.route('/user/insert', methods=['GET', 'POST'])
@required_group('manager')
def user_insert() -> str | Response:
    form = UserForm()
    form.group.choices = get_groups()
    if not g.settings['mail']:
        del form.send_info
    if form.validate_on_submit():
        user_id = User.insert({
            'username': sanitize(form.username.data),
            'real_name': sanitize(form.real_name.data) or '',
            'info': sanitize(form.description.data) or '',
            'email': form.email.data,
            'active': form.active.data,
            'group_name': form.group.data,
            'password': bcrypt.hashpw(
                form.password.data.encode('utf-8'),
                bcrypt.gensalt()).decode('utf-8')})
        flash(_('user created'), 'info')
        if g.settings['mail'] and form.send_info.data:
            subject = _(
                'Your account information for %(sitename)s',
                sitename=g.settings['site_name'])
            body = \
                _('Account information for %(username)s',
                  username=form.username.data) + \
                f" {_('at')} {request.scheme}" \
                f"://{request.headers['Host']}\n\n" \
                f"{uc_first(_('username'))}: {form.username.data}\n" \
                f"{uc_first(_('password'))}: {form.password.data}\n"
            if send_mail(subject, body, form.email.data, False):
                flash(
                    _('Sent account information mail to %(email)s.',
                      email=form.email.data),
                    'info')
            else:  # pragma: no cover
                flash(
                    _('Failed to send account details to %(email)s.',
                      email=form.email.data),
                    'error')
        if hasattr(form, 'continue_') and form.continue_.data == 'yes':
            return redirect(url_for('user_insert'))
        return redirect(url_for('user_view', id_=user_id))
    return render_template(
        'tabs.html',
        tabs={
            'user': Tab(
                'user',
                content=display_form(
                    form,
                    'user-form',
                    manual_page='admin/user'))},
        title=_('user'),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-user"],
            '+&nbsp;<span class="uc-first d-inline-block">' + _('user')
            + '</span>'])


@app.route('/install', methods=['GET', 'POST'])
def first_admin() -> str | Response:
    if g.admins_available:
        abort(403)
    form = UserForm()
    del form.send_info, form.active, form.group, form.insert_and_continue
    if form.validate_on_submit():
        User.insert({
            'username': sanitize(form.username.data),
            'real_name': sanitize(form.real_name.data) or '',
            'info': sanitize(form.description.data) or '',
            'email': None,
            'active': True,
            'group_name': 'admin',
            'password': bcrypt.hashpw(
                form.password.data.encode('utf-8'),
                bcrypt.gensalt()).decode('utf-8')})
        flash(_('user created'), 'info')
        return redirect(url_for('login'))
    return render_template(
        'content.html',
        content=display_form(form),
        crumbs=[
            _('Welcome to OpenAtlas. Please add an admin user to continue.')])


def get_groups() -> list[tuple[str, str]]:
    choices = [(name, name) for name in [  # Weakest to strongest permissions
        'readonly',
        'contributor',
        'editor',
        'manager']]
    if is_authorized('admin'):
        choices.append(('admin', 'admin'))
    return choices
