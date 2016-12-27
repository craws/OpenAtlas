import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# To do: try to get rid of hardcoded path below (needed to find packages with Apache)
sys.path.insert(0, "/var/www/org/openatlas")
# To do: try to get rid of hardcoded path below (ideally set in Apache config)
os.environ['APP_CONFIG_FILE'] = '/home/alex/projects/www/org/openatlas/config/development.py'

from openatlas import app
from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, evalex=True)
