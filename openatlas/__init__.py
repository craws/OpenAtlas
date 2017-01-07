import locale
import sys
from flask import Flask, request, session
from flask.ext.babel import Babel, gettext
from openatlas.util import filters

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)

from openatlas.views import index, content

app.config.from_object('config.default')  # load config/default.py
app.config.from_pyfile('config.py')  # load instance/config.py
app.config.from_envvar('APP_CONFIG_FILE')
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')


babel = Babel(app)
app.register_blueprint(filters.blueprint)

@babel.localeselector
def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

if __name__ == "__main__":  # pragma: no cover
    app.run()
