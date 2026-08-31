import os
import sys

from application_path import OPENATLAS_INSTALLATION

sys.path.insert(0, OPENATLAS_INSTALLATION)
os.environ['INSTANCE_PATH'] = f'{os.path.dirname(os.path.abspath(__file__))}/'

# pylint: disable=wrong-import-position
from install.upgrade import database_upgrade
database_upgrade.database_upgrade()
