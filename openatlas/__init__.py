# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import ConfigParser
import locale
import psycopg2.extras
import os
import sys
from collections import OrderedDict

from flask import Flask, request, session
from flask_babel import Babel

from openatlas.models.property import PropertyMapper
from openatlas.models.classObject import ClassMapper
from openatlas.models.settings import SettingsMapper
from openatlas.util import filters

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)
settings = []


def connect(config_name='production'):
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.dirname(__file__) + '/db.conf'))
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


try:  # To do: elegant way to use different configs (e.g production and testing)
    import mod_wsgi
    connection = connect('production')  # pragma: no cover
except ImportError:
    connection = connect('testing')

app.config.from_object('config.default')  # load config/default.py
app.config.from_pyfile('config.py')  # load instance/config.py
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')

from openatlas.views import content, index, settings, model, source, event, actor, place, reference, hierarchy

babel = Babel(app)
app.register_blueprint(filters.blueprint)

classes = ClassMapper.get_all()
properties = PropertyMapper.get_all()

# To do: store these values somewhere else, config?

default_table_rows = OrderedDict()
default_table_rows[10] = '10'
default_table_rows[20] = '20'
default_table_rows[50] = '50'
default_table_rows[100] = '100'

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
    return best_match if best_match else session['settings']['default_language']  # check if best_match is set (in tests it isn't)


@app.before_request
def before_request():
    session['settings'] = SettingsMapper.get_settings()
    session['language'] = get_locale()

if __name__ == "__main__":  # pragma: no cover
    app.run()
