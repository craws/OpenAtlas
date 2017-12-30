# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import abort, flash, render_template, session, url_for, request
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms.validators import Email, InputRequired, Length
from wtforms import (BooleanField, HiddenField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)

from openatlas import app
from openatlas.models.user import User, UserMapper
from openatlas.util.util import (format_date, link, required_group, send_mail, uc_first,
                                 is_authorized)


class UserForm(Form):
    user_id = None
    active = BooleanField(_('active'), default=True)
    username = StringField(_('username'), [InputRequired()])
    group = SelectField(_('group'), choices=[])
    email = StringField(_('email'), [InputRequired(), Email()])
    password = PasswordField(_('password'), [InputRequired()])
    password2 = PasswordField(_('repeat password'), [InputRequired()])
    show_passwords = BooleanField(_('show passwords'))
    real_name = StringField(_('name'))
    description = TextAreaField(_('info'))
    send_info = BooleanField(_('send account information'))
    save = SubmitField(_('save'))
    insert_and_continue = SubmitField(_('insert and continue'))
    continue_ = HiddenField()

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        user = UserMapper.get_by_id(self.user_id) if self.user_id else User()
        if user.username != self.username.data and UserMapper.get_by_username(self.username.data):
            self.username.errors.append(str(_('error username exists')))
            valid = False
        if user.email != self.email.data and UserMapper.get_by_email(self.email.data):
            self.email.errors.append(str(_('error email exists')))
            valid = False
        if getattr(self, 'password'):
            if self.password.data != self.password2.data:
                self.password.errors.append(_('error passwords must match'))
                self.password2.errors.append(_('error passwords must match'))
                valid = False
            if len(self.password.data) < session['settings']['minimum_password_length']:
                self.password.errors.append(_('error password too short'))
                valid = False
        return valid


@app.route('/admin/user/view/<int:id_>')
@required_group('manager')
def user_view(id_):
    user = UserMapper.get_by_id(id_)
    data = {'info': [
        (_('username'), link(user)),
        (_('group'), user.group),
        (_('name'), user.real_name),
        (_('email'), user.email),
        (_('language'), user.settings['language']),
        (_('last login'), format_date(user.login_last_success)),
        (_('failed logins'), user.login_failed_count)]}
    return render_template('user/view.html', user=user, data=data)


@app.route('/admin/user')
@required_group('manager')
def user_index():
    tables = {'user': {
        'name': 'user',
        'sort': 'sortList: [[3, 1]]',
        'header': ['username', 'group', 'email', 'newsletter', 'created', 'last login'],
        'data': []}}
    for user in UserMapper.get_all():
        tables['user']['data'].append([
            link(user),
            user.group,
            user.email,
            user.settings['newsletter'],
            format_date(user.created),
            format_date(user.login_last_success)])
    return render_template('user/index.html', tables=tables)


@app.route('/admin/user/update/<int:id_>', methods=['POST', 'GET'])
@required_group('manager')
def user_update(id_):
    user = UserMapper.get_by_id(id_)
    if user.group == 'admin' and current_user.group != 'admin':
        abort(403)
    form = UserForm()
    form.user_id = id_
    del form.password, form.password2, form.send_info, form.insert_and_continue, form.show_passwords
    form.group.choices = get_groups()
    if form.validate_on_submit():
        user.active = form.active.data
        if user.id == current_user.id:  # don't allow setting oneself as inactive
            user.active = True
        user.real_name = form.real_name.data
        user.username = form.username.data
        user.email = form.email.data
        user.description = form.description.data
        user.group = form.group.data
        user.update()
        flash(_('info update'), 'info')
        return redirect(url_for('user_view', id_=id_))
    form.username.data = user.username
    form.group.data = user.group
    form.real_name.data = user.real_name
    form.active.data = user.active
    form.email.data = user.email
    form.description.data = user.description
    if user.id == current_user.id:
        del form.active
    return render_template('user/update.html', form=form, user=user)


@app.route('/admin/user/insert', methods=['POST', 'GET'])
@required_group('manager')
def user_insert():
    form = UserForm()
    form.group.choices = get_groups()
    if form.validate_on_submit():
        user_id = UserMapper.insert(form)
        flash(_('user created'), 'info')
        if form.send_info.data and session['settings']['mail']:  # pragma: no cover
            subject = _(
                'Your account information for %(sitename)s',
                sitename=session['settings']['site_name'])
            body = _('Account information for %(username)s', username=form.username.data) + ' '
            body += _('at') + ' ' + request.scheme + '://' + request.headers['Host'] + '\n\n'
            body += uc_first(_('username')) + ': ' + form.username.data + '\n'
            body += uc_first(_('password')) + ': ' + form.password.data + '\n'
            if send_mail(subject, body, form.email.data, False):
                flash(
                    _('Sent account information mail to %(email)s.', email=form.email.data), 'info')
            else:
                flash(
                    _('Failed to send account details to %(email)s.',
                      email=form.email.data),
                    'error')
            return redirect(url_for('user_index'))
        if form.continue_.data == 'yes':
            return redirect(url_for('user_insert'))
        return redirect(url_for('user_view', id_=user_id))
    return render_template('user/insert.html', form=form)


def get_groups():
    """
        Returns groups, hardcoded because order is relevant (weakest permissions to strongest)
    """
    choices = [('readonly', 'readonly'), ('editor', 'editor'), ('manager', 'manager')]
    if is_authorized('admin'):
        choices.append(('admin', 'admin'))  # admin group is only available for admins
    return choices


@app.route('/admin/user/delete/<int:id_>')
@required_group('manager')
def user_delete(id_):
    user = UserMapper.get_by_id(id_)
    if (user.group == 'admin' and current_user.group != 'admin') and user.id != current_user.id:
        abort(403)
    UserMapper.delete(id_)
    flash(_('user deleted'), 'info')
    return redirect(url_for('user_index'))
