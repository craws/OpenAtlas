import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import sys
import schemathesis
from schemathesis.cli import schemathesis as schemathesis_cli

from openatlas import app
from openatlas.api.api_v1.routes.files import check_file_access
from openatlas.display.image_processing import check_iiif_file_exist
from openatlas.models.entity import Entity

_place_uuid = None
_case_study_id = None
_image_id = None

def get_place_uuid() -> str:
    global _place_uuid
    if _place_uuid is not None:
        return _place_uuid

    try:
        with app.test_request_context():
            app.preprocess_request()
            places = Entity.get_by_class('place')
            if places:
                _place_uuid = str(places[0].uuid)
                return _place_uuid
    except Exception:
        pass

    _place_uuid = "00000000-0000-0000-0000-000000000001"
    return _place_uuid


def get_case_study_id() -> int:
    global _case_study_id
    if _case_study_id is not None:
        return _case_study_id

    try:
        with app.test_request_context():
            app.preprocess_request()
            case_study_hierarchy = Entity.get_hierarchy('Case study')
            if case_study_hierarchy and case_study_hierarchy.subs:
                _case_study_id = case_study_hierarchy.subs[0]
                return _case_study_id
    except Exception:
        pass

    _case_study_id = 1
    return _case_study_id


def get_image_id() -> int:
    global _image_id
    if _image_id is not None:
        return _image_id

    try:
        with app.test_request_context():
            app.preprocess_request()
            files = Entity.get_by_class('file')
            for f in files:
                if check_file_access(f.id) and check_iiif_file_exist(f.id):
                    _image_id = f.id
                    return _image_id
            if files:
                _image_id = files[0].id
                return _image_id
    except Exception:
        pass

    _image_id = 1
    return _image_id

@schemathesis.hook
def before_generate_path_parameters(context, strategy):
    path = context.operation.path

    def inject_valid_ids(params: dict) -> dict:
        if "id" in params:
            if path.startswith("/api/1/files/"):
                params["id"] = get_image_id()
            elif path.startswith("/api/1/case-studies/"):
                params["id"] = get_case_study_id()
            elif "/entity/" in path:
                params["id"] = get_place_uuid()
        return params

    return strategy.map(inject_valid_ids)

if __name__ == "__main__":
    sys.argv = [
        "schemathesis",
        "run",
        "http://localhost:5000/api/1/docs/openapi.json",
        "--url", "http://localhost:5000",
        # "--phases", "examples",
        "--phases", "examples,coverage,fuzzing"]
    
    try:
        schemathesis_cli()
    except SystemExit as e:
        sys.exit(e.code)
