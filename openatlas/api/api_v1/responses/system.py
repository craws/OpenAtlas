from openatlas.api.api_v1.models.system import (
    EntityCountResponse, SystemClassesResponse,
    SystemInfoResponse, SystemPropertiesResponse)

system_info_response = {200: SystemInfoResponse}
entity_count_response = {200: EntityCountResponse}
system_classes_response = {200: SystemClassesResponse}
system_properties_response = {200: SystemPropertiesResponse}
