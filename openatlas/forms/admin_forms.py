from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import Email, InputRequired

from openatlas import app
from openatlas.forms.forms import TableField
from openatlas.util.util import (uc_first)


class GeneralForm(FlaskForm):  # type: ignore
    site_name = StringField(uc_first(_('site name')))
    default_language = SelectField(uc_first(_('default language')),
                                   choices=list(app.config['LANGUAGES'].items()))
    default_table_rows = SelectField(uc_first(_('default table rows')),
                                     coerce=int,
                                     choices=list(app.config['DEFAULT_TABLE_ROWS'].items()))
    log_level = SelectField(uc_first(_('log level')),
                            coerce=int,
                            choices=list(app.config['LOG_LEVELS'].items()))
    debug_mode = BooleanField(uc_first(_('debug mode')))
    random_password_length = IntegerField(uc_first(_('random password length')))
    minimum_password_length = IntegerField(uc_first(_('minimum password length')))
    reset_confirm_hours = IntegerField(uc_first(_('reset confirm hours')))
    failed_login_tries = IntegerField(uc_first(_('failed login tries')))
    failed_login_forget_minutes = IntegerField(uc_first(_('failed login forget minutes')))
    minimum_jstree_search = IntegerField(uc_first(_('minimum jstree search')))
    minimum_tablesorter_search = IntegerField(uc_first(_('minimum tablesorter search')))
    save = SubmitField(uc_first(_('save')))


class TestMailForm(FlaskForm):  # type: ignore
    receiver = StringField(_('test mail receiver'), [InputRequired(), Email()])
    send = SubmitField(_('send test mail'))


class MailForm(FlaskForm):  # type: ignore
    mail = BooleanField(uc_first(_('mail')))
    mail_transport_username = StringField(uc_first(_('mail transport username')))
    mail_transport_host = StringField(uc_first(_('mail transport host')))
    mail_transport_port = StringField(uc_first(_('mail transport port')))
    mail_from_email = StringField(uc_first(_('mail from email')), [Email()])
    mail_from_name = StringField(uc_first(_('mail from name')))
    mail_recipients_feedback = StringField(uc_first(_('mail recipients feedback')))
    save = SubmitField(uc_first(_('save')))


class NewsLetterForm(FlaskForm):  # type: ignore
    subject = StringField('', [InputRequired()], render_kw={'placeholder': _('subject'),
                                                            'autofocus': True})
    body = TextAreaField('', [InputRequired()], render_kw={'placeholder': _('content')})
    send = SubmitField(uc_first(_('send')))


class LogForm(FlaskForm):  # type: ignore
    limit = SelectField(_('limit'), choices=((0, _('all')), (100, 100), (500, 500)), default=100)
    priority = SelectField(_('priority'),
                           choices=(list(app.config['LOG_LEVELS'].items())),
                           default=6)
    user = SelectField(_('user'), choices=([(0, _('all'))]), default=0)
    apply = SubmitField(_('apply'))


class MapForm(FlaskForm):  # type: ignore
    map_cluster_max_radius = IntegerField('maxClusterRadius')
    map_cluster_disable_at_zoom = IntegerField('disableClusteringAtZoom')
    save = SubmitField(uc_first(_('save')))


class ApiForm(FlaskForm):  # type: ignore
    api_public = BooleanField('public')
    save = SubmitField(uc_first(_('save')))


class FileForm(FlaskForm):  # type: ignore
    file_upload_max_size = IntegerField(_('max file size in MB'))
    file_upload_allowed_extension = StringField('allowed file extensions')
    profile_image_width = IntegerField(_('profile image width in pixel'))
    save = SubmitField(uc_first(_('save')))


class SimilarForm(FlaskForm):  # type: ignore
    classes = SelectField(_('class'), choices=[])
    ratio = IntegerField(default=100)
    apply = SubmitField(_('search'))


class LogoForm(FlaskForm):  # type: ignore
    file = TableField(_('file'), [InputRequired()])
    save = SubmitField(uc_first(_('change logo')))
