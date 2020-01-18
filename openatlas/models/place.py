from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, List, Optional

from openatlas.models.entity import Entity


def get_structure(object_: Optional[Entity]) -> Dict[str, Any]:
    place = None
    feature = None
    stratigraphic_unit = None
    siblings: List[Entity] = []
    if not object_:
        pass
    elif object_.system_type == 'find':
        stratigraphic_unit = object_.get_linked_entity_safe('P46', inverse=True)
        feature = stratigraphic_unit.get_linked_entity_safe('P46', inverse=True)
        place = feature.get_linked_entity_safe('P46', inverse=True)
        siblings = stratigraphic_unit.get_linked_entities('P46')  # Add finds of same stratigraphic
    elif object_.system_type == 'stratigraphic unit':
        feature = object_.get_linked_entity_safe('P46', inverse=True)
        place = feature.get_linked_entity_safe('P46', inverse=True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity_safe('P46', inverse=True)
    return {'place': place,
            'feature': feature,
            'stratigraphic_unit': stratigraphic_unit,
            'subunits': object_.get_linked_entities('P46', nodes=True) if object_ else [],
            'siblings': siblings}
