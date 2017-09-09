# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import configparser
import locale
import psycopg2.extras
import os
import time
from collections import OrderedDict

from flask import Flask, request, session
from flask_babel import Babel

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    instance_relative_config=True)

settings = []


def connect(config_name='production'):
    config = configparser.ConfigParser()
    config.read_file(open(os.path.dirname(__file__) + '/db.conf'))
    db_name = config.get(config_name, 'database_name')
    db_user = config.get(config_name, 'database_user')
    db_port = config.get(config_name, 'database_port')
    db_pass = config.get(config_name, 'database_pass')
    db_host = config.get(config_name, 'database_host')
    try:
        connection_ = psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host)
        connection_.autocommit = True
        return connection_
    except Exception as e:  # pragma: no cover
        print("Database connection error.")
        raise Exception(e)


def get_cursor():
    return connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)


try:  # To do: better way to use different configs (e.g production and testing)
    import mod_wsgi
    connection = connect('production')  # pragma: no cover
except ImportError:
    connection = connect('testing')

app.config.from_object('config.default')  # load config/default.py
app.config.from_pyfile('config.py')  # load instance/config.py
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')

babel = Babel(app)

# To do: store these values somewhere else, config?
default_table_rows = OrderedDict()
default_table_rows['10'] = '10'
default_table_rows['20'] = '20'
default_table_rows['50'] = '50'
default_table_rows['100'] = '100'

log_levels = OrderedDict()
log_levels[0] = 'emergency'
log_levels[1] = 'alert'
log_levels[2] = 'critical'
log_levels[3] = 'error'
log_levels[4] = 'warn'
log_levels[5] = 'notice'
log_levels[6] = 'info'
log_levels[7] = 'debug'


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

# get id of property 'has type' because its needed in EntityMapper
cursor = get_cursor()
cursor.execute("SELECT id FROM model.property WHERE name = 'has type';")
has_type_id = cursor.fetchone()[0]

import openatlas
from openatlas.models.node import NodeMapper
from openatlas.models.property import PropertyMapper
from openatlas.models.settings import SettingsMapper
from openatlas.util import filters

debug_model['current'] = time.time()
classes = openatlas.models.classObject.ClassMapper.get_all()
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

from openatlas.views import actor, ajax, content, index, settings, model, source, event, place, reference, node
from openatlas.views import user, login, profile

app.register_blueprint(filters.blueprint)
app.add_template_global(debug_model, 'debug_model')
app.debug = True


@app.context_processor
def inject_debug():
    return dict(debug=app.debug)

if __name__ == "__main__":  # pragma: no cover
    app.run()

    # below is a try to debug with pycharm
    # import argparse
    #
    # parser = argparse.ArgumentParser(description='Development Server Help')
    # parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
    #                     help="run in debug mode (for use with PyCharm)", default=False)
    # parser.add_argument("-p", "--port", dest="port", help="port of server (default:%(default)s)", type=int,
    #                     default=5000)
    #
    # cmd_args = parser.parse_args()
    # app_options = {"port": cmd_args.port}
    #
    # if cmd_args.debug_mode:
    #     app_options["debug"] = True
    #     app_options["use_debugger"] = False
    #     app_options["use_reloader"] = False
    #
    # app.run(**app_options)
