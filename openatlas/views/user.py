# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask_babel import lazy_gettext as _
from flask import render_template
from flask_wtf import Form
from wtforms import StringField, TextAreaField, HiddenField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email
from openatlas import app
from openatlas.util.util import uc_first, format_date
from openatlas.models.user import UserMapper


class UserForm(Form):
    active = BooleanField(uc_first(_('active')))
    username = StringField(uc_first(_('username')), validators=[InputRequired()])
    password = PasswordField(uc_first(_('password')), validators=[InputRequired()])
    password2 = PasswordField(uc_first(_('repeat password')), validators=[InputRequired()])
    description = TextAreaField(uc_first(_('info')))
    name = StringField(uc_first(_('name')))
    email = StringField(uc_first(_('email')), validators=[InputRequired(), Email()])
    send_info = BooleanField(_('send account information'))
    continue_ = HiddenField()


@app.route('/user')
def user_index():
    tables = {'user': {
        'name': 'user',
        'sort': 'sortList: [[3, 1]]',
        'header': [_('username'), _('group'), _('email'), _('newsletter'), _('created'), _('last login')],
        'data': []}}
    for user in UserMapper.get_all():
        tables['user']['data'].append([
            user.username,
            user.group,
            user.email,
            '',  # user.newsletter
            format_date(user.created),
            format_date(user.login_last_success)
        ])
    return render_template('user/index.html', tables=tables)


@app.route('/user/insert', methods=['POST', 'GET'])
def user_insert():
    form = UserForm()
    return render_template('user/insert.html', form=form)
