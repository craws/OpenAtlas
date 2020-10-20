import locale
import os
import sys
import time
from typing import Any, Dict, Optional

import psycopg2.extras
from flask import Flask, Response, g, request, session
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect


app: Flask = Flask(__name__, instance_relative_config=True)
csrf = CSRFProtect(app)  # Make sure all forms are CSRF protected

# Use the test database if running tests
instance_name = 'production' if 'test_runner.py' not in sys.argv[0] else 'testing'

# Load config/default.py and instance/INSTANCE_NAME.py
app.config.from_object('config.default')  # type: ignore
app.config.from_pyfile(instance_name + '.py')  # type: ignore

if os.name == "posix":  # For other operating systems e.g. Windows, we would need adaptions here
    locale.setlocale(locale.LC_ALL, 'en_US.utf-8')  # pragma: no cover

babel = Babel(app)
debug_model: Dict[str, float] = {}


from openatlas.models.logger import Logger

logger = Logger()

from openatlas.util import filters, processor
from openatlas.views import (actor, admin, ajax, api, entity, event, export, file, hierarchy, index,
                             involvement, imports, link, login, member, model, note, object,
                             overlay, place, profile, reference, relation, search, source, sql,
                             translation, types, user)


@babel.localeselector
def get_locale() -> str:
    if 'language' in session:
        return session['language']
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
    # Check if best_match is set (in tests it isn't)
    return best_match if best_match else session['settings']['default_language']


def connect() -> psycopg2.connect:
    try:
        connection_ = psycopg2.connect(database=app.config['DATABASE_NAME'],
                                       user=app.config['DATABASE_USER'],
                                       password=app.config['DATABASE_PASS'],
                                       port=app.config['DATABASE_PORT'],
                                       host=app.config['DATABASE_HOST'])
        connection_.autocommit = True
        return connection_
    except Exception as e:  # pragma: no cover
        print("Database connection error.")
        raise Exception(e)


def execute(query: str, vars_: Optional[Dict[str, Any]] = None) -> None:
    debug_model['sql'] += 1
    return g.cursor.execute(query, vars_)


@app.before_request
def before_request() -> None:
    from openatlas.models.model import CidocClass, CidocProperty
    from openatlas.models.node import Node
    from openatlas.models.settings import Settings
    if request.path.startswith('/static'):  # pragma: no cover
        return  # Only needed if not running with Apache and static alias
    debug_model['sql'] = 0
    debug_model['current'] = time.time()
    g.db = connect()
    g.cursor = g.db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    g.execute = execute  # Add wrapper for g.cursor.execute to count SQL statements per request
    g.classes = CidocClass.get_all()
    g.properties = CidocProperty.get_all()
    g.nodes = Node.get_all_nodes()
    session['settings'] = Settings.get_settings()
    session['language'] = get_locale()
    g.external = app.config['EXTERNAL_REFERENCES']
    g.external['geonames']['url'] = session['settings']['geonames_url']
    debug_model['model'] = time.time() - debug_model['current']
    debug_model['current'] = time.time()

    # Set max file upload in MB
    app.config['MAX_CONTENT_LENGTH'] = session['settings']['file_upload_max_size'] * 1024 * 1024


@app.after_request
def apply_caching(response: Response) -> Response:
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Todo: activate Content-Security-Policy after removal of every inline CSS and JavaScript
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.teardown_request
def teardown_request(exception: Any) -> None:
    if hasattr(g, 'db'):
        g.db.close()


app.register_blueprint(filters.blueprint)
app.add_template_global(debug_model, 'debug_model')


if __name__ == "__main__":  # pragma: no cover
    app.run()
