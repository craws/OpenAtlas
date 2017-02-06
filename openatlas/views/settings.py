# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from collections import OrderedDict

import openatlas
from flask import flash, session, render_template
from flask_wtf import Form
from openatlas import app
from openatlas.models.settings import SettingsMapper
from openatlas.util import util
from werkzeug.utils import redirect
from wtforms import StringField, BooleanField

from openatlas.util.util import uc_first
from flask.ext.babel import lazy_gettext as _


class SettingsForm(Form):

    # General
    site_name = StringField(_('site name'))
    default_language = StringField(_('default language'))
    default_table_rows = StringField(_('default table rows'))
    log_level = StringField(_('log level'))
    maintenance = BooleanField(_('maintenance'))
    offline = BooleanField(_('offline'))

    # Mail
    mail = BooleanField(_('mail'))
    mail_transport_username = StringField(_('mail transport username'))
    mail_transport_host = StringField(_('mail transport host'))
    mail_transport_port = StringField(_('mail transport port'))
    mail_transport_type = StringField(_('mail transport type'))
    mail_transport_ssl = StringField(_('mail transport ssl'))
    mail_transport_auth = StringField(_('mail transport auth'))
    mail_from_email = StringField(_('mail from email'))
    mail_from_name = StringField(_('mail from name'))
    mail_recipients_login = StringField(_('mail recipients login'))
    mail_recipients_feedback = StringField(_('mail recipients feedback'))

    # Authentication
    random_password_length = StringField(_('random password length'))
    reset_confirm_hours = StringField(_('reset confirm hours'))
    failed_login_tries = StringField(_('failed login tries'))
    failed_login_forget_minutes = StringField(_('failed login forget minutes'))


@app.route('/settings')
def settings_index():
    settings = SettingsMapper.get_settings()
    log_array = {
        '0': 'Emergency',
        '1': 'Alert',
        '2': 'Critical',
        '3': 'Error',
        '4': 'Warn',
        '5': 'Notice',
        '6': 'Info',
        '7': 'Debug'
    }
    groups = OrderedDict([
        ('general', OrderedDict([
            (_('site name'), settings['site_name']),
            (_('default language'), settings['default_language']),
            (_('default table rows'), settings['default_table_rows']),
            (_('log level'), log_array[settings['log_level']]),
            (_('maintenance'), uc_first('on') if settings['maintenance'] else uc_first('off')),
            (_('offline'), uc_first('on') if settings['offline'] else uc_first('off')),
        ])),
        ('mail', OrderedDict([
            (_('mail'), uc_first('on') if settings['mail'] else uc_first('off')),
            (_('mail transport username'), settings['mail_transport_username']),
            (_('mail transport host'), settings['mail_transport_host']),
            (_('mail transport port'), settings['mail_transport_port']),
            (_('mail transport type'), settings['mail_transport_type']),
            (_('mail transport ssl'), settings['mail_transport_ssl']),
            (_('mail transport auth'), settings['mail_transport_auth']),
            (_('mail from email'), settings['mail_from_email']),
            (_('mail from name'), settings['mail_from_name']),
            (_('mail recipients login'), settings['mail_recipients_login']),
            (_('mail recipients feedback'), settings['mail_recipients_feedback']),
        ])),
        ('authentication', OrderedDict([
            (_('random password length'), settings['random_password_length']),
            (_('reset confirm hours'), settings['reset_confirm_hours']),
            (_('failed login tries'), settings['failed_login_tries']),
            (_('failed login forget minutes'), settings['failed_login_forget_minutes'])
        ]))
    ])
    return render_template('settings/index.html', groups=groups, settings=settings)


@app.route('/settings/update', methods=["GET", "POST"])
def settings_update():
    form = SettingsForm()
    return render_template('settings/update.html', form=form, settings=SettingsMapper.get_settings())
