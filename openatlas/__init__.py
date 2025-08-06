import datetime
import locale
from typing import Any, Optional

from flask import Flask, g, redirect, request, session, url_for
from flask_babel import Babel
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect
from psycopg2 import extras
from werkzeug.wrappers import Response

from config.model.class_groups import class_groups
from openatlas.api.resources.error import AccessDeniedError
from openatlas.database.checks import check_type_count_needed
from openatlas.database.connect import close_connection, open_connection
from openatlas.database.token import check_token_revoked
from openatlas.database.user import admins_available
from openatlas.models.openatlas_class import (
    get_class_view_mapping, get_classes)

app: Flask = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)  # Make sure all forms are CSRF protected
app.config.from_object('config.default')
app.config.from_object('config.api')
app.config.from_pyfile('production.py')
app.config['WTF_CSRF_TIME_LIMIT'] = None  # Set CSRF token valid for session
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
babel = Babel(app)
jwt = JWTManager(app)

# pylint: disable=cyclic-import, import-outside-toplevel, wrong-import-position
from openatlas.models.logger import Logger
from openatlas.api import api
from openatlas.views import (
    admin, ajax, annotation, arche, changelog, entity, entity_index, error,
    export, file, hierarchy, index, imports, link, login, model, note, overlay,
    profile, search, token, tools, type as type_, user, vocabs)


@babel.localeselector
def get_locale() -> str:
    if request.path.startswith('/api/') \
            and request.args.get('locale') in app.config['LANGUAGES']:
        return str(request.args.get('locale'))
    if 'language' in session:
        return session['language']
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    return best_match or g.settings['default_language']


@app.before_request
def before_request() -> Response | None:
    from openatlas.models.cidoc_property import CidocProperty
    from openatlas.models.cidoc_class import CidocClass
    from openatlas.models.entity import Entity
    from openatlas.models.settings import Settings
    from openatlas.models.reference_system import ReferenceSystem

    if request.path.startswith('/static'):
        return None  # Avoid overheads if not using Apache with static alias
    g.logger = Logger()
    g.db = open_connection(app.config)
    g.db.autocommit = True
    g.cursor = g.db.cursor(cursor_factory=extras.DictCursor)
    g.settings = Settings.get_settings()

    if request.path.startswith('/display'):
        return None  # Avoid overheads for file display

    session['language'] = get_locale()
    g.admins_available = admins_available()
    if not g.admins_available \
            and request.endpoint not in ['first_admin', 'set_locale']:
        return redirect(url_for('first_admin'))
    g.cidoc_classes = CidocClass.get_all(
        session['language'],
        (request.path.startswith('/overview/model/cidoc_class_index')))
    g.properties = CidocProperty.get_all(
        session['language'],
        (request.path.startswith('/overview/model/property')))
    g.classes = get_classes()
    g.types = Entity.get_all_types(count_type())
    g.radiocarbon_type = Entity.get_hierarchy('Radiocarbon')
    g.sex_type = Entity.get_hierarchy('Features for sexing')
    g.reference_match_type = Entity.get_hierarchy('External reference match')
    g.reference_systems = ReferenceSystem.get_all()
    g.class_groups = class_groups
    g.writable_paths = [
        app.config['EXPORT_PATH'],
        app.config['RESIZED_IMAGES'],
        app.config['UPLOAD_PATH'],
        app.config['TMP_PATH']]
    setup_files()
    setup_api()
    return None


def setup_files() -> None:
    from openatlas.models.entity import Entity
    g.files = {}
    for file_ in app.config['UPLOAD_PATH'].iterdir():
        if file_.stem.isdigit():
            g.files[int(file_.stem)] = file_
    app.config['MAX_CONTENT_LENGTH'] = \
        g.settings['file_upload_max_size'] * 1024 * 1024  # Max upload in MB
    g.display_file_ext = app.config['DISPLAY_FILE_EXT']
    if g.settings['image_processing']:
        g.display_file_ext += app.config['PROCESSABLE_EXT']
    if g.settings['iiif'] and g.settings['iiif_path']:
        g.writable_paths.append(g.settings['iiif_path'])
    g.file_info = Entity.get_file_info()


def setup_api() -> None:
    from openatlas.api.resources.openapi_util import write_openapi_instance
    if request.path.startswith('/swagger'):
        write_openapi_instance()
    elif request.path.startswith('/api/'):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not current_user.is_authenticated \
                and not g.settings['api_public'] \
                and ip not in app.config['ALLOWED_IPS'] \
                and not verify_jwt_in_request(
                    optional=True,
                    locations='headers'):
            raise AccessDeniedError


def count_type() -> bool:
    if request.path.startswith(('/type', '/api/type_tree/', '/admin/orphans')):
        return True
    if request.path.startswith('/entity/') and \
            request.path.split('/entity/')[1].isdigit():
        return check_type_count_needed(int(request.path.split('/entity/')[1]))
    return False


@app.after_request
def apply_caching(response: Response) -> Response:
    response.headers['Strict-Transport-Security'] = \
        'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = app.config['CSP_HEADER']
    return response


@app.teardown_request
def teardown_request(_exception: Optional[Any]) -> None:
    close_connection()


@jwt.token_in_blocklist_loader
def check_incoming_tokens(
        jwt_header: dict[str, Any],
        jwt_payload: dict[str, Any]) -> bool:
    if not jwt_header['typ'] == 'JWT':
        return True
    token_ = check_token_revoked(jwt_payload["jti"])
    if token_['revoked'] \
            or not token_['active'] \
            or token_['valid_until'] < datetime.datetime.now():
        return True
    return False
