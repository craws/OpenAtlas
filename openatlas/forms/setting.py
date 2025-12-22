from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, FieldList, IntegerField, SelectField, StringField)
from wtforms.validators import Email, InputRequired, Optional, Regexp, URL

from openatlas import app
from openatlas.forms.field import RemovableListField, SubmitField


class ContentForm(FlaskForm):
    pass


class ModulesForm(FlaskForm):
    module_map_overlay = BooleanField(str(_('map overlay')))
    module_time = BooleanField(str(_('time')))
    save = SubmitField(str(_('save')))


class GeneralForm(FlaskForm):
    site_name = StringField(str(_('site name')), [InputRequired()])
    default_language = SelectField(
        str(_('default language')),
        choices=list(app.config['LANGUAGES'].items()))
    table_rows = SelectField(
        str(_('default table rows')),
        coerce=int,
        choices=list(app.config['TABLE_ROWS'].items()))
    log_level = SelectField(
        str(_('log level')),
        coerce=int,
        choices=list(app.config['LOG_LEVELS'].items()))
    random_password_length = IntegerField(str(_('random password length')))
    minimum_password_length = IntegerField(str(_('minimum password length')))
    reset_confirm_hours = IntegerField(str(_('reset confirm hours')))
    failed_login_tries = IntegerField(str(_('failed login tries')))
    failed_login_forget_minutes = IntegerField(
        str(_('failed login forget minutes')))
    minimum_jstree_search = IntegerField(str(_('minimum jstree search')))
    image_processing = BooleanField(str(_('image processing')))
    save = SubmitField(str(_('save')))


class TestMailForm(FlaskForm):
    receiver = StringField(
        str(_('test mail receiver')),
        [InputRequired(), Email()])
    save = SubmitField(str(_('send test mail')))


class MailForm(FlaskForm):
    mail = BooleanField(str(_('mail')))
    mail_transport_username = StringField(str(_('mail transport username')))
    mail_transport_host = StringField(str(_('mail transport host')))
    mail_transport_port = StringField(str(_('mail transport port')))
    mail_from_email = StringField(str(_('mail from email')), [Email()])
    mail_from_name = StringField(str(_('mail from name')))
    mail_recipients_feedback = FieldList(
        RemovableListField(render_kw={'class': 'email'}))
    save = SubmitField(str(_('save')))


class IiifForm(FlaskForm):
    iiif = BooleanField(
        str('IIIF'),
        description=str(_('tooltip IIIF enabled')))
    iiif_url = StringField(
        str(_('URL')),
        validators=[
            URL(require_tld=False),
            Regexp(r'^(.*)\/$', message=str(_('URL need a trailing /')))],
        description=str(_('tooltip IIIF URL')))
    iiif_version = SelectField(
        str(_('version')),
        choices=((2, '2'),),
        coerce=int,
        description=str(_('tooltip IIIF version')))
    iiif_conversion = SelectField(
        str(_('conversion')),
        choices=(('', 'none'), ('deflate', 'deflate'), ('jpeg', 'jpeg')),
        description=str(_('tooltip IIIF conversion')))
    iiif_path = StringField(
        str(_('path')),
        description=str(_('tooltip IIIF path')))
    iiif_convert_on_upload = BooleanField(
        str(_('convert on upload')),
        description=str(_('tooltip IIIF convert on upload')))
    save = SubmitField(str(_('apply')))


class LogForm(FlaskForm):
    limit = SelectField(
        str(_('limit')),
        choices=((0, str(_('all'))), (100, 100), (500, 500)),  # type: ignore
        default=100)
    priority = SelectField(
        str(_('priority')),
        choices=(list(app.config['LOG_LEVELS'].items())),
        default=6)
    user = SelectField(
        str(_('user')),
        choices=([(0, str(_('all')))]),
        default=0)
    save = SubmitField(str(_('apply')))


class MapForm(FlaskForm):
    map_zoom_default = IntegerField(
        str(_('default map zoom')),
        [InputRequired()])
    map_zoom_max = IntegerField(str(_('max map zoom')), [InputRequired()])
    map_cluster_disable_at_zoom = IntegerField(
        str(_('disable clustering at zoom')))
    map_cluster_max_radius = IntegerField(str(_('max cluster radius')))
    geonames_username = StringField('GeoNames ' + str(_('username')))
    save = SubmitField(str(_('save')))


class FrontendForm(FlaskForm):
    frontend_website_url = StringField(
        str(_('website url')),
        [Optional(), URL()])
    frontend_resolver_url = StringField(
        str(_('resolver url')),
        [Optional(), URL()])
    save = SubmitField(str(_('save')))


class ApiForm(FlaskForm):
    api_public = BooleanField('public')
    save = SubmitField(str(_('save')))


class FileForm(FlaskForm):
    file_upload_max_size = IntegerField(str(_('maximum file size in MB')))
    profile_image_width = IntegerField(str(_('profile image width in pixel')))
    file_upload_allowed_extension = FieldList(RemovableListField())
    save = SubmitField(str(_('save')))


class SimilarForm(FlaskForm):
    classes = SelectField(str(_('class')), choices=[])
    ratio = IntegerField(default=100)
    save = SubmitField(str(_('search')))


class ProfileForm(FlaskForm):
    name = StringField(
        str(_('full name')),
        description=str(_('tooltip full name')))
    email = StringField(
        str(_('email')),
        [InputRequired(), Email()],
        description=str(_('tooltip email')))
    show_email = BooleanField(
        str(_('show email')),
        description=str(_('tooltip show email')))
    newsletter = BooleanField(
        str(_('newsletter')),
        description=str(_('tooltip newsletter')))
    save = SubmitField(str(_('save')))


class DisplayForm(FlaskForm):
    language = SelectField(
        str(_('language')),
        choices=list(app.config['LANGUAGES'].items()))
    table_rows = SelectField(
        str(_('table rows')),
        description=str(_('tooltip table rows')),
        choices=list(app.config['TABLE_ROWS'].items()),
        coerce=int)
    table_show_aliases = BooleanField(str(_('show aliases in tables')))
    entity_show_dates = BooleanField(
        str(_('show created and modified information')))
    entity_show_import = BooleanField(str(_('show import information')))
    entity_show_class = BooleanField(str(_('show CIDOC class')))
    map_zoom_default = IntegerField(
        str(_('default map zoom')),
        [InputRequired()])
    map_zoom_max = IntegerField(str(_('max map zoom')), [InputRequired()])
    save = SubmitField(str(_('save')))
