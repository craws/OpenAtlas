import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.insert(0, "/var/www/org/openatlas")

from openatlas import app
from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, evalex=True)
