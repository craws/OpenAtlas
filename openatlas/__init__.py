import locale
import sys
from flask import Flask

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = 'come, get some'
app.config.from_pyfile('production.py')
locale.setlocale(locale.LC_ALL, 'en_US.utf-8')

from openatlas.views import overview

if __name__ == "__main__":  # pragma: no cover
    app.run()
