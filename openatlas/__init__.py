import locale
import os
import sys
from typing import Optional

from flask import Flask, Response, g, request, session
from flask_babel import Babel
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect

from openatlas.api.v02.resources.error import AccessDeniedError
from openatlas.database.connect import close_connection, open_connection

app: Flask = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)  # Make sure all forms are CSRF protected

# Use test database if running tests
instance_name = 'production' \
    if 'test_runner.py' not in sys.argv[0] else 'testing'

app.config.from_object('config')
app.config.from_pyfile(instance_name + '.py')
app.config['WTF_CSRF_TIME_LIMIT'] = None  # Set CSRF token valid for session

if os.name == "posix":
    locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
babel = Babel(app)

from openatlas.models.logger import Logger

logger = Logger()

from openatlas.api import api  # New routes
from openatlas.util import processor
from openatlas.util.util import get_file_stats
from openatlas.views import (
    admin, ajax, entity, entity_index, entity_form, export, file, hierarchy,
    index, involvement, imports, link, login, member, model, note, overlay,
    profile, reference, relation, reference_system, search, sql, type, user)


@babel.localeselector
def get_locale() -> str:
    if 'language' in session:
        return session['language']
    best_match = request.accept_languages.best_match(
        app.config['LANGUAGES'].keys())
    return best_match if best_match else session['settings']['default_language']


@app.before_request
def before_request() -> None:
    from openatlas.models.openatlas_class import (
        OpenatlasClass, view_class_mapping)
    from openatlas.models.cidoc_property import CidocProperty
    from openatlas.models.cidoc_class import CidocClass
    from openatlas.models.type import Type
    from openatlas.models.settings import Settings
    from openatlas.models.reference_system import ReferenceSystem

    if request.path.startswith('/static'):  # pragma: no cover
        return  # Avoid overhead for files if not using Apache with static alias
    open_connection(app.config)
    session['settings'] = Settings.get_settings()
    session['language'] = get_locale()
    g.cidoc_classes = CidocClass.get_all()
    g.properties = CidocProperty.get_all()
    g.classes = OpenatlasClass.get_all()
    g.types = Type.get_all()
    g.reference_systems = ReferenceSystem.get_all()
    g.view_class_mapping = view_class_mapping
    g.class_view_mapping = OpenatlasClass.get_class_view_mapping()
    g.table_headers = OpenatlasClass.get_table_headers()
    g.file_stats = get_file_stats()

    # Set max file upload in MB
    app.config['MAX_CONTENT_LENGTH'] = \
        session['settings']['file_upload_max_size'] * 1024 * 1024

    if request.path.startswith('/api/'):
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not current_user.is_authenticated \
                and not session['settings']['api_public'] \
                and ip not in app.config['ALLOWED_IPS']:
            raise AccessDeniedError  # pragma: no cover


@app.after_request
def apply_caching(response: Response) -> Response:
    response.headers['Strict-Transport-Security'] = \
        'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


@app.teardown_request
def teardown_request(_exception: Optional[Exception]) -> None:
    close_connection()


if __name__ == "__main__":  # pragma: no cover
    app.run()
