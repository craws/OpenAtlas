# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask_babel import gettext, lazy_gettext as _
from flask import abort, flash, render_template, url_for
from flask_login import current_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, TextAreaField, HiddenField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email

from openatlas import app
from openatlas.util.util import uc_first, format_date, link, required_group
from openatlas.models.user import UserMapper, User


class UserForm(Form):
    user_id = None
    active = BooleanField(uc_first(_('active')), default=True)
    username = StringField(uc_first(_('username')), validators=[InputRequired()])
    password = PasswordField(uc_first(_('password')), validators=[InputRequired()])
    password2 = PasswordField(uc_first(_('repeat password')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('info')))
    real_name = StringField(uc_first(_('name')))
    email = StringField(uc_first(_('email')), validators=[InputRequired(), Email()])
    send_info = BooleanField(_('send account information'))
    group = SelectField(uc_first(_('group')), choices=UserMapper.get_groups(), default='readonly')
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

        password = getattr(self, 'password', None)
        if password:
            if password.data != self.password2.data:
                password.errors.append(str(_('error passwords must match')))
                valid = False
            # if len(password.data) < app.config['PASSWORD_MINIMUM_LENGTH']:
            #     password.errors.append(str(_('error password length')))
            #    form_validity = False
            # if app.config['PASSWORD_REQUIRE_CHARACTER_MIX']:
            #    lowercase_letters = sum(1 for c in password.data if c.islower())
            #    uppercase_letters = sum(1 for c in password.data if c.isupper())
            #    digits = sum(1 for c in password.data if c.isdigit())
            #    if lowercase_letters < 1 or uppercase_letters < 1 or digits < 1:
            #        password.errors.append(str(_('error password complexity')))
            #        form_validity = False
        return valid


@app.route('/user/view/<int:user_id>')
@required_group('manager')
def user_view(user_id):
    user = UserMapper.get_by_id(user_id)
    data = {'info': [
        (_('username'), link(user)),
        (_('group'), user.group),
        (_('name'), user.real_name),
        (_('email'), user.email),
        (_('language'), 'To do'),
        (_('last login'), 'To do'),
        (_('failed logins'), 'To do')
    ]}
    return render_template('user/view.html', user=user, data=data)


@app.route('/user')
@required_group('manager')
def user_index():
    tables = {'user': {
        'name': 'user',
        'sort': 'sortList: [[3, 1]]',
        'header': [_('username'), _('group'), _('email'), _('newsletter'), _('created'), _('last login')],
        'data': []}}
    for user in UserMapper.get_all():
        tables['user']['data'].append([
            link(user),
            user.group,
            user.email,
            '',  # user.newsletter
            format_date(user.created),
            format_date(user.login_last_success)
        ])
    return render_template('user/index.html', tables=tables)


@app.route('/user/update/<int:user_id>', methods=['POST', 'GET'])
@required_group('manager')
def user_update(user_id):
    user = UserMapper.get_by_id(user_id)
    if user.group == 'admin' and current_user.group != 'admin':
        abort(403)
    form = UserForm()
    form.user_id = user_id
    del form.password
    del form.password2
    del form.send_info
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
        flash(gettext('user updated'), 'info')
        return redirect(url_for('user_view', user_id=user_id))
    form.username.data = user.username
    form.group.data = user.group
    form.real_name.data = user.real_name
    form.active.data = user.active
    form.email.data = user.email
    form.description.data = user.description
    return render_template('user/update.html', form=form, user=user)


@app.route('/user/insert', methods=['POST', 'GET'])
@required_group('manager')
def user_insert():
    form = UserForm()
    if form.validate_on_submit():
        user_id = UserMapper.insert(form)
        flash(gettext('user created'), 'info')
        if form.continue_.data == 'yes':
            return redirect(url_for('user_insert'))
        return redirect(url_for('user_view', user_id=user_id))
    return render_template('user/insert.html', form=form)


@app.route('/admin/user/delete/<int:user_id>')
@required_group('manager')
def user_delete(user_id):
    user = UserMapper.get_by_id(user_id)
    if (user.group == 'admin' and current_user.group != 'admin') and user.id != current_user.id:
        flash(gettext('error user deleted'), 'info')
        return redirect(url_for('user_index'))
    UserMapper.delete(user_id)
    flash(gettext('user deleted'), 'info')
    return redirect(url_for('user_index'))
