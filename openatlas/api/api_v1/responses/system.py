from http import HTTPStatus

from openatlas.api.api_v1.models.system import (
    EntityCountResponse, SystemClassesResponse, SystemInfoResponse,
    SystemPropertiesResponse)

system_info_response = {HTTPStatus.OK: SystemInfoResponse}
entity_count_response = {HTTPStatus.OK: EntityCountResponse}
system_classes_response = {HTTPStatus.OK: SystemClassesResponse}
system_properties_response = {HTTPStatus.OK: SystemPropertiesResponse}
