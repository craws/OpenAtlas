from openatlas.api.v02.resources.error import EntityDoesNotExistError
from openatlas.models.entity import Entity


def get_entity_by_id(id_: int) -> Entity:
    try:
        entity = Entity.get_by_id(id_, nodes=True, aliases=True)
    except Exception:
        raise EntityDoesNotExistError
    return entity
