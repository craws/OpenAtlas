# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
import ConfigParser
import locale
import psycopg2.extras
import os
import sys

from flask import Flask, request, session
from flask_babel import Babel
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
    app.config['WTF_CSRF_ENABLED'] = False
    connection = connect('testing')

app.config.from_object('config.default')  # load config/default.py
app.config.from_pyfile('config.py')  # load instance/config.py
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')

from openatlas.views import content, index, settings

babel = Babel(app)
app.register_blueprint(filters.blueprint)


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
