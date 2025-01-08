import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/usr/local/openatlas')  # Todo: remove hardcoded path

os.environ['INSTANCE_PATH'] = f'{os.path.dirname(os.path.abspath(__file__))}/'

from openatlas import app as application
