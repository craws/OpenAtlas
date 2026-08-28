from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiIndexResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    version: str
    openapi_schema: str
    documentation: str
    manual: str
