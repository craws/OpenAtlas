import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.default import VERSION, DATABASE_VERSION

# execfile("/home/el/foo2/mylib.py")

from openatlas.models.settings import Settings

print(f"{VERSION} OpenAtlas version")
print(f"{DATABASE_VERSION} Database version required")

#settings = Settings.get_settings()
#print(settings)
# print(f"Installed database version: {g.settings['database_version']}")
