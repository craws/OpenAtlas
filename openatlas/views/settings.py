# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import flash, render_template, session, url_for, request, g
from flask_babel import lazy_gettext as _
from flask_login import current_user
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, BooleanField, SelectField, SubmitField
from wtforms.validators import Email, InputRequired

import openatlas
from openatlas import SettingsMapper
from openatlas import app
from openatlas.util.util import uc_first, required_group, send_mail


class TestMail(Form):
    receiver = StringField(_('test mail receiver'), [InputRequired(), Email()])
    send = SubmitField(_('send test mail'))


class SettingsForm(Form):

    # General
    site_name = StringField(uc_first(_('site name')))
    default_language = SelectField(uc_first(
        _('default language')),
        choices=app.config['LANGUAGES'].items())
    default_table_rows = SelectField(
        uc_first(_('default table rows')),
        choices=app.config['DEFAULT_TABLE_ROWS'].items(),
        coerce=int)
    log_level = SelectField(
        uc_first(_('log level')),
        choices=app.config['LOG_LEVELS'].items(),
        coerce=int)
    debug_mode = BooleanField(uc_first(_('debug mode')))

    # Mail
    mail = BooleanField(uc_first(_('mail')))
    mail_transport_username = StringField(uc_first(_('mail transport username')))
    mail_transport_host = StringField(uc_first(_('mail transport host')))
    mail_transport_port = StringField(uc_first(_('mail transport port')))
    mail_from_email = StringField(uc_first(_('mail from email')))
    mail_from_name = StringField(uc_first(_('mail from name')))
    mail_recipients_login = StringField(uc_first(_('mail recipients login')))
    mail_recipients_feedback = StringField(uc_first(_('mail recipients feedback')))

    # Authentication
    random_password_length = StringField(uc_first(_('random password length')))
    minimum_password_length = StringField(uc_first(_('minimum password length')))
    reset_confirm_hours = StringField(uc_first(_('reset confirm hours')))
    failed_login_tries = StringField(uc_first(_('failed login tries')))
    failed_login_forget_minutes = StringField(uc_first(_('failed login forget minutes')))


@app.route('/admin/settings', methods=["GET", "POST"])
@required_group('admin')
def settings_index():
    form = TestMail()
    if form.validate_on_submit() and session['settings']['mail']:  # pragma: no cover
        user = current_user
        subject = _('Test mail from %(site_name)s', sitename=session['settings']['site_name'])
        body = _('This test mail was sent by %(username)s', username=user.username)
        body += ' ' + _('at') + ' ' + request.headers['Host']
        if send_mail(subject, body, form.receiver.data):
            flash(_('A test mail was sent to %(email)s.', email=form.receiver.data))
    else:
        form.receiver.data = current_user.email

    settings = session['settings']
    groups = OrderedDict([
        ('general', OrderedDict([
            (_('site name'), settings['site_name']),
            (_('default language'), app.config['LANGUAGES'][settings['default_language']]),
            (_('default table rows'), settings['default_table_rows']),
            (_('log level'), app.config['LOG_LEVELS'][int(settings['log_level'])]),
            (_('debug mode'), uc_first(_('on')) if settings['debug_mode'] else uc_first(_('off')))
        ])),
        ('mail', OrderedDict([
            (_('mail'), uc_first(_('on')) if settings['mail'] else uc_first(_('off'))),
            (_('mail transport username'), settings['mail_transport_username']),
            (_('mail transport host'), settings['mail_transport_host']),
            (_('mail transport port'), settings['mail_transport_port']),
            (_('mail from email'), settings['mail_from_email']),
            (_('mail from name'), settings['mail_from_name']),
            (_('mail recipients login'), ', '.join(settings['mail_recipients_login'])),
            (_('mail recipients feedback'), ', '.join(settings['mail_recipients_feedback']))])),
        ('authentication', OrderedDict([
            (_('random password length'), settings['random_password_length']),
            (_('minimum password length'), settings['minimum_password_length']),
            (_('reset confirm hours'), settings['reset_confirm_hours']),
            (_('failed login tries'), settings['failed_login_tries']),
            (_('failed login forget minutes'), settings['failed_login_forget_minutes'])]))])
    return render_template('settings/index.html', groups=groups, settings=settings, form=form)


@app.route('/admin/settings/update', methods=["GET", "POST"])
@required_group('admin')
def settings_update():
    form = SettingsForm()
    if form.validate_on_submit():
        g.cursor.execute('BEGIN')
        try:
            SettingsMapper.update(form)
            openatlas.logger.log('info', 'settings', 'Settings updated')
            g.cursor.execute('COMMIT')
            flash(_('info update'), 'info')
        except Exception as e:  # pragma: no cover
            g.cursor.execute('ROLLBACK')
            openatlas.logger.log('error', 'database', 'transaction failed', e)
            flash(_('error transaction'), 'error')
        return redirect(url_for('settings_index'))
    for field in SettingsMapper.fields:
        if field in ['mail_recipients_login', 'mail_recipients_feedback']:
            getattr(form, field).data = ', '.join(session['settings'][field])
        elif field in ['default_table_rows', 'log_level']:
            getattr(form, field).data = int(session['settings'][field])
        else:
            getattr(form, field).data = session['settings'][field]
    return render_template('settings/update.html', form=form, settings=session['settings'])
