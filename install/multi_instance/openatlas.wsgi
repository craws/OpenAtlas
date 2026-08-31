import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application_path import OPENATLAS_INSTALLATION

sys.path.insert(0, OPENATLAS_INSTALLATION)

os.environ['INSTANCE_PATH'] = f'{os.path.dirname(os.path.abspath(__file__))}/'

from openatlas import app as application
