# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask_babel import lazy_gettext as _
from flask import render_template
from openatlas import app
from openatlas.util.util import format_date
from openatlas.models.user import UserMapper


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
