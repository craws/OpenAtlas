import locale
import sys
from flask import Flask

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')  # load config/default.py
app.config.from_pyfile('config.py')  # load instance/config.py
app.config.from_envvar('APP_CONFIG_FILE')
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')

from openatlas.views import overview

if __name__ == "__main__":  # pragma: no cover
    app.run()
