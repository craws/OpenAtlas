import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from openatlas import open_connection
from config.default import (
    DATABASE_PASS, VERSION, DATABASE_VERSION, DATABASE_NAME, DATABASE_USER,
    DATABASE_HOST, DATABASE_PORT)
from instance import production

config = {
    'DATABASE_NAME': DATABASE_NAME,
    'DATABASE_USER': DATABASE_USER,
    'DATABASE_PASS': DATABASE_PASS,
    'DATABASE_PORT': DATABASE_PORT,
    'DATABASE_HOST': DATABASE_HOST}

for item in config:
    try:
        config[item] = vars(production)[item]
    except:
        pass


print(f"{VERSION} OpenAtlas version")
print(f"{DATABASE_VERSION} Database version required")

db = open_connection(config)

# print(f"Installed database version: {g.settings['database_version']}")
