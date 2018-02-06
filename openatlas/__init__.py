# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import locale
import sys
import time
from collections import OrderedDict

import psycopg2.extras
from flask import Flask, request, session, g
from flask_babel import Babel, lazy_gettext as _
from flask_wtf import Form
from wtforms import StringField, SubmitField

try:
    import mod_wsgi
except ImportError:
    mod_wsgi = None

app = Flask(__name__, instance_relative_config=True)

# use the test database if running tests
instance_name = 'production' if 'test_runner.py' not in sys.argv[0] else 'testing'
debug_model = OrderedDict()
app.config.from_object('config.default')  # load config/INSTANCE_NAME.py
app.config.from_pyfile(instance_name + '.py')  # load instance/INSTANCE_NAME.py
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
babel = Babel(app)

import openatlas
from openatlas.models.classObject import ClassMapper
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.models.property import PropertyMapper
from openatlas.models.settings import SettingsMapper
from openatlas.util import filters
from openatlas.views import (actor, admin, ajax, content, event, hierarchy, index, login, types,
                             model, place, profile, reference, settings, source, translation, user,
                             involvement, relation, member, search)

from openatlas.models.logger import DBHandler
logger = DBHandler()


@babel.localeselector
def get_locale():
    if 'language' in session:
        return session['language']
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
    # check if best_match is set (in tests it isn't)
    return best_match if best_match else session['settings']['default_language']


def connect():
    try:
        connection_ = psycopg2.connect(
            database=app.config['DATABASE_NAME'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASS'],
            port=app.config['DATABASE_PORT'],
            host=app.config['DATABASE_HOST'])
        connection_.autocommit = True
        return connection_
    except Exception as e:  # pragma: no cover
        print("Database connection error.")
        raise Exception(e)


@app.before_request
def before_request():
    if request.path.startswith('/static'):  # pragma: no cover
        return  # only needed if not running with apache and static alias
    debug_model['current'] = time.time()
    g.db = connect()
    g.cursor = g.db.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    g.classes = ClassMapper.get_all()
    g.properties = PropertyMapper.get_all()
    g.nodes = NodeMapper.get_all_nodes()
    session['settings'] = SettingsMapper.get_settings()
    session['language'] = get_locale()
    debug_model['by codes'] = 0
    debug_model['by id'] = 0
    debug_model['by ids'] = 0
    debug_model['linked'] = 0
    debug_model['user'] = 0
    debug_model['div sql'] = 0
    debug_model['model'] = time.time() - debug_model['current']
    debug_model['current'] = time.time()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


class GlobalSearchForm(Form):
    term = StringField('', render_kw={"placeholder": _('search term')})
    search = SubmitField(_('search'))


@app.context_processor
def inject_search_form():
    return dict(search_form=GlobalSearchForm(prefix="global"))


app.register_blueprint(filters.blueprint)
app.add_template_global(debug_model, 'debug_model')


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


if __name__ == "__main__":  # pragma: no cover
    app.run()
