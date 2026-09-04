import sys
from functools import cache
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import schemathesis
from schemathesis.cli import schemathesis as schemathesis_cli

from openatlas import app
from openatlas.api.api_v1.util.files import check_file_access
from openatlas.display.image_processing import check_iiif_file_exist
from openatlas.models.entity import Entity

DEFAULT_IMAGE_ID = 1
DEFAULT_CASE_STUDY_ID = 1
DEFAULT_PLACE_UUID = "00000000-0000-0000-0000-000000000001"
SCHEMATHESIS_ARGUMENTS = (
    "run",
    "http://localhost:5000/api/1/docs/openapi.json",
    "--url",
    "http://localhost:5000",
    "--phases",
    "examples,coverage,fuzzing",
)


@cache
def get_place_uuid() -> str:
    try:
        with app.test_request_context():
            app.preprocess_request()
            places = Entity.get_by_class('place')
            if places:
                return str(places[0].uuid)
    except Exception:
        return DEFAULT_PLACE_UUID

    return DEFAULT_PLACE_UUID


@cache
def get_case_study_id() -> int:
    try:
        with app.test_request_context():
            app.preprocess_request()
            case_study_hierarchy = Entity.get_hierarchy('Case study')
            if case_study_hierarchy and case_study_hierarchy.subs:
                return case_study_hierarchy.subs[0]
    except Exception:
        return DEFAULT_CASE_STUDY_ID

    return DEFAULT_CASE_STUDY_ID


@cache
def get_image_id() -> int:
    try:
        with app.test_request_context():
            app.preprocess_request()
            files = Entity.get_by_class('file')
            for file_ in files:
                if (check_file_access(file_.id)
                        and check_iiif_file_exist(file_.id)):
                    return file_.id
            if files:
                return files[0].id
    except Exception:
        return DEFAULT_IMAGE_ID

    return DEFAULT_IMAGE_ID


@schemathesis.hook
def before_generate_path_parameters(
        context: Any, strategy: Any) -> Any:
    path = context.operation.path

    def inject_valid_ids(params: dict[str, Any]) -> dict[str, Any]:
        if "id" in params:
            if path.startswith("/api/1/files/"):
                params["id"] = get_image_id()
            elif path.startswith("/api/1/case-studies/"):
                params["id"] = get_case_study_id()
            elif "/entity/" in path:
                params["id"] = get_place_uuid()
        return params

    return strategy.map(inject_valid_ids)


def main() -> None:
    schemathesis_cli.main(
        args=SCHEMATHESIS_ARGUMENTS,
        prog_name="schemathesis")


if __name__ == "__main__":
    main()
