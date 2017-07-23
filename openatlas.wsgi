import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openatlas import app
from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(app, evalex=True)
