from typing import Any

import requests

from openatlas import app


def fetch_only_files() -> dict[int, Any]:
    collections = {}
    for id_ in app.config['ARCHE_COLLECTION_IDS']:
        req = requests.get(
            f"{app.config['ARCHE_BASE_URL']}"
            f"/api/{id_}/metadata?format=application/json")
        collections[id_] = req.json()
    return collections


