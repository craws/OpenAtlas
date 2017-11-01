# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import locale
import psycopg2.extras
import sys
import time
from collections import OrderedDict
from flask import Flask, request, session
from flask_babel import Babel

try:
    import mod_wsgi
except ImportError:
    mod_wsgi = None

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config=True)

instance_name = 'production' if '--cover-tests' not in sys.argv else 'testing'
app.config.from_object('config.default')  # load config/INSTANCE_NAME.py
app.config.from_pyfile(instance_name + '.py')  # load instance/INSTANCE_NAME.py


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


def get_cursor():
    return connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)


connection = connect()
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')
babel = Babel(app)


import openatlas
from openatlas.models.classObject import ClassMapper
from openatlas.models.entity import Entity, EntityMapper
from openatlas.models.node import NodeMapper
from openatlas.models.property import PropertyMapper
from openatlas.models.settings import SettingsMapper
from openatlas.util import filters
from openatlas.views import (actor, admin, ajax, content, event, hierarchy, index, login, node,
                             model, place, profile, reference, settings, source, translation, user)


@babel.localeselector
def get_locale():
    if 'language' in session:
        return session['language']
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'].keys())
    # check if best_match is set (in tests it isn't)
    return best_match if best_match else session['settings']['default_language']


debug_model = OrderedDict()
debug_model['current'] = time.time()
debug_model['by id'] = 0
debug_model['by ids'] = 0
debug_model['by codes'] = 0
debug_model['linked'] = 0
debug_model['user'] = 0
debug_model['current'] = time.time()

classes = ClassMapper.get_all()
properties = PropertyMapper.get_all()

debug_model['model'] = time.time() - debug_model['current']
debug_model['current'] = time.time()

nodes = {}


@app.before_request
def before_request():
    session['settings'] = SettingsMapper.get_settings()
    session['language'] = get_locale()
    openatlas.nodes = NodeMapper.get_all_nodes()
    NodeMapper.populate_subs()
    debug_model['current'] = time.time()
    debug_model['by id'] = 0
    debug_model['by ids'] = 0
    debug_model['linked'] = 0
    debug_model['user'] = 0
    debug_model['div sql'] = 0


app.register_blueprint(filters.blueprint)
app.add_template_global(debug_model, 'debug_model')


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)


if __name__ == "__main__":  # pragma: no cover
    app.run()
