import locale
from typing import Any, Optional

from flask import Flask, Response, g, request, session
from flask_babel import Babel
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect
from psycopg2 import extras

from openatlas.api.resources.error import AccessDeniedError
from openatlas.database.connect import close_connection, open_connection

app: Flask = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)  # Make sure all forms are CSRF protected
app.config.from_object('config.default')
app.config.from_object('config.api')
app.config.from_pyfile('production.py')
app.config['WTF_CSRF_TIME_LIMIT'] = None  # Set CSRF token valid for session

locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
babel = Babel(app)

# pylint: disable=cyclic-import, import-outside-toplevel, wrong-import-position
from openatlas.models.logger import Logger
from openatlas.api import api
from openatlas.views import (
    admin, ajax, annotation, arche, changelog, entity, entity_index, error,
    export, file, hierarchy, index, imports, link, login, model, note, overlay,
    profile, search, sql, tools, type as type_, user, vocabs)


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
def before_request() -> None:
    from openatlas.models.openatlas_class import (
        OpenatlasClass, view_class_mapping)
    from openatlas.models.cidoc_property import CidocProperty
    from openatlas.models.cidoc_class import CidocClass
    from openatlas.models.type import Type
    from openatlas.models.settings import Settings
    from openatlas.models.reference_system import ReferenceSystem

    if request.path.startswith('/static'):
        return  # Avoid files overhead if not using Apache with static alias

    g.logger = Logger()
    g.db = open_connection(app.config)
    g.db.autocommit = True
    g.cursor = g.db.cursor(cursor_factory=extras.DictCursor)
    g.settings = Settings.get_settings()
    session['language'] = get_locale()
    g.cidoc_classes = CidocClass.get_all(session['language'])
    g.properties = CidocProperty.get_all(session['language'])
    g.classes = OpenatlasClass.get_all()
    with_count = False
    if (request.path.startswith(('/type', '/api/type_tree/', '/admin/orphans'))
            or (request.path.startswith('/entity/') and
                request.path.split('/entity/')[1].isdigit())):
        with_count = True
    g.types = Type.get_all(with_count)
    g.radiocarbon_type = Type.get_hierarchy('Radiocarbon')
    g.sex_type = Type.get_hierarchy('Features for sexing')
    g.reference_match_type = Type.get_hierarchy('External reference match')
    g.reference_systems = ReferenceSystem.get_all()
    g.view_class_mapping = view_class_mapping
    g.class_view_mapping = OpenatlasClass.get_class_view_mapping()
    g.table_headers = OpenatlasClass.get_table_headers()
    g.writable_paths = [
        app.config['EXPORT_PATH'],
        app.config['RESIZED_IMAGES'],
        app.config['UPLOAD_PATH'],
        app.config['TMP_PATH']]
    setup_files()
    setup_api()


def setup_files() -> None:
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


def setup_api() -> None:
    from openatlas.api.resources.openapi_util import write_openapi_instance
    if request.path.startswith('/swagger'):
        write_openapi_instance()
    elif request.path.startswith('/api/'):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not current_user.is_authenticated \
                and not g.settings['api_public'] \
                and ip not in app.config['ALLOWED_IPS']:
            raise AccessDeniedError


@app.after_request
def apply_caching(response: Response) -> Response:
    response.headers['Strict-Transport-Security'] = \
        'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.teardown_request
def teardown_request(_exception: Optional[Any]) -> None:
    close_connection()
