from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


# Refactor with new recursive
def get_place(entity: Entity) -> Optional[Entity]:
    if entity := entity.get_linked_entity('P46', inverse=True):  # type: ignore
        if entity.class_.name == 'place':
            return entity  # pragma: no cover
        if entity := entity.get_linked_entity(
                'P46',
                inverse=True):  # type: ignore
            if entity.class_.name == 'place':
                return entity  # pragma: no cover
            if entity := entity.get_linked_entity(
                    'P46',
                    inverse=True):  # type: ignore
                if entity.class_.name == 'place':
                    return entity
    return None  # pragma: no cover


def get_structure(
        object_: Optional[Entity] = None,
        super_: Optional[Entity] = None) -> Optional[dict[str, list[Entity]]]:
    siblings: list[Entity] = []
    subunits: list[Entity] = []
    if super_:
        supers = \
            super_.get_linked_entities_recursive('P46', inverse=True) \
            + [super_]
        siblings = super_.get_linked_entities('P46')
    elif not object_:
        return None
    else:
        supers = object_.get_linked_entities_recursive('P46', inverse=True)
        subunits = object_.get_linked_entities('P46', types=True)
        if supers:
            siblings = supers[-1].get_linked_entities('P46')
    return {
        'supers': supers,
        'subunits': subunits,
        'siblings': siblings}
