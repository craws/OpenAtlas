from datetime import datetime

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, FieldList, IntegerField, SelectField, StringField)
from wtforms.fields.choices import RadioField
from wtforms.validators import Email, InputRequired, Optional, Regexp, URL

from openatlas import app
from openatlas.forms.field import RemovableListField, SubmitField


class ContentForm(FlaskForm):
    pass


class ModulesForm(FlaskForm):
    module_map_overlay = BooleanField(_('map overlay'))
    module_time = BooleanField(_('time'))
    save = SubmitField(_('save'))


class GeneralForm(FlaskForm):
    site_name = StringField(_('site name'), [InputRequired()])
    default_language = SelectField(
        _('default language'),
        choices=list(app.config['LANGUAGES'].items()))
    table_rows = SelectField(
        _('default table rows'),
        coerce=int,
        choices=list(app.config['TABLE_ROWS'].items()))
    log_level = SelectField(
        _('log level'),
        coerce=int,
        choices=list(app.config['LOG_LEVELS'].items()))
    random_password_length = IntegerField(_('random password length'))
    minimum_password_length = IntegerField(_('minimum password length'))
    reset_confirm_hours = IntegerField(_('reset confirm hours'))
    failed_login_tries = IntegerField(_('failed login tries'))
    failed_login_forget_minutes = IntegerField(
        _('failed login forget minutes'))
    minimum_jstree_search = IntegerField(_('minimum jstree search'))
    image_processing = BooleanField(_('image processing'))
    save = SubmitField(_('save'))


class TestMailForm(FlaskForm):
    receiver = StringField(_('test mail receiver'), [InputRequired(), Email()])
    save = SubmitField(_('send test mail'))


class MailForm(FlaskForm):
    mail = BooleanField(_('mail'))
    mail_transport_username = StringField(_('mail transport username'))
    mail_transport_host = StringField(_('mail transport host'))
    mail_transport_port = StringField(_('mail transport port'))
    mail_from_email = StringField(_('mail from email'), [Email()])
    mail_from_name = StringField(_('mail from name'))
    mail_recipients_feedback = FieldList(
        RemovableListField(render_kw={'class': 'email'}))
    save = SubmitField(_('save'))


class IiifForm(FlaskForm):
    iiif = BooleanField('IIIF', description=_('tooltip IIIF enabled'))
    iiif_url = StringField(
        _('URL'),
        validators=[
            URL(require_tld=False),
            Regexp(r'^(.*)\/$', message=_('URL need a trailing /'))],
        description=_('tooltip IIIF URL'))
    iiif_version = SelectField(
        _('version'),
        choices=((2, '2'),),
        coerce=int,
        description=_('tooltip IIIF version'))
    iiif_conversion = SelectField(
        _('conversion'),
        choices=(('', 'none'), ('deflate', 'deflate'), ('jpeg', 'jpeg')),
        description=_('tooltip IIIF conversion'))
    iiif_path = StringField(_('path'), description=_('tooltip IIIF path'))
    iiif_convert_on_upload = BooleanField(
        _('convert on upload'),
        description=_('tooltip IIIF convert on upload'))
    save = SubmitField(_('apply'))


class LogForm(FlaskForm):
    limit = SelectField(
        _('limit'),
        choices=((0, _('all')), (100, 100), (500, 500)), default=100)
    priority = SelectField(
        _('priority'),
        choices=(list(app.config['LOG_LEVELS'].items())),
        default=6)
    user = SelectField(_('user'), choices=([(0, _('all'))]), default=0)
    save = SubmitField(_('apply'))


class MapForm(FlaskForm):
    map_zoom_default = IntegerField(_('default map zoom'), [InputRequired()])
    map_zoom_max = IntegerField(_('max map zoom'), [InputRequired()])
    map_cluster_disable_at_zoom = IntegerField(_('disable clustering at zoom'))
    map_cluster_max_radius = IntegerField(_('max cluster radius'))
    geonames_username = StringField('GeoNames ' + _('username'))
    save = SubmitField(_('save'))


class FrontendForm(FlaskForm):
    frontend_website_url = StringField(_('website URL'), [Optional(), URL()])
    frontend_resolver_url = StringField(_('resolver URL'), [Optional(), URL()])
    save = SubmitField(_('save'))


class ApiForm(FlaskForm):
    api_public = BooleanField('public')
    save = SubmitField(_('save'))


class FileForm(FlaskForm):
    file_upload_max_size = IntegerField(_('maximum file size in MB'))
    profile_image_width = IntegerField(_('profile image width in pixel'))
    file_upload_allowed_extension = FieldList(RemovableListField())
    save = SubmitField(_('save'))


class SimilarForm(FlaskForm):
    classes = SelectField(_('class'), choices=[])
    ratio = IntegerField(default=100)
    save = SubmitField(_('search'))


class ProfileForm(FlaskForm):
    name = StringField(_('full name'), description=_('tooltip full name'))
    email = StringField(
        _('email'),
        [InputRequired(), Email()],
        description=_('tooltip email'))
    show_email = BooleanField(
        _('show email'),
        description=_('tooltip show email'))
    newsletter = BooleanField(
        _('newsletter'),
        description=_('tooltip newsletter'))
    save = SubmitField(_('save'))


class DisplayForm(FlaskForm):
    language = SelectField(
        _('language'),
        choices=list(app.config['LANGUAGES'].items()))
    table_rows = SelectField(
        _('table rows'),
        description=_('tooltip table rows'),
        choices=list(app.config['TABLE_ROWS'].items()),
        coerce=int)
    table_show_aliases = BooleanField(_('show aliases in tables'))
    table_show_icons = BooleanField(_('show icons in tables'))
    entity_show_dates = BooleanField(
        _('show created and modified information'))
    entity_show_import = BooleanField(_('show import information'))
    entity_show_class = BooleanField(_('show CIDOC class'))
    map_zoom_default = IntegerField(_('default map zoom'), [InputRequired()])
    map_zoom_max = IntegerField(_('max map zoom'), [InputRequired()])
    save = SubmitField(_('save'))


class TokenForm(FlaskForm):
    expiration = RadioField(
        _('expiration'),
        choices=[('0','One day'),('1','90 days'), ('2', 'no expiration date')],
        default='0')
    token_name = StringField(
        _('token name'),
        default=f"Token_{datetime.today().strftime('%Y-%m-%d')}")
    token_text = StringField(_('token'), render_kw={'readonly': True})
    save = SubmitField(_('generate'))
