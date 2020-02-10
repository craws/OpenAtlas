from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, List, Optional

from openatlas.models.entity import Entity


def get_structure(object_: Optional[Entity] = None,
                  super_: Optional[Entity] = None) -> Optional[Dict[str, Any]]:
    super_id = None
    place = None
    feature = None
    stratigraphic_unit = None
    siblings: List[Entity] = []
    subunits: List[Entity] = []

    if super_:
        super_id = super_.id
        if super_.system_type == 'stratigraphic unit':
            feature = super_.get_linked_entity_safe('P46', inverse=True)
            place = feature.get_linked_entity_safe('P46', inverse=True)
        elif super_.system_type == 'feature':
            place = super_.get_linked_entity_safe('P46', inverse=True)
        elif super_.system_type == 'place':
            place = super_
    elif not object_:
        return None
    elif object_.system_type in ['find', 'human remains']:
        stratigraphic_unit = object_.get_linked_entity_safe('P46', inverse=True)
        super_id = stratigraphic_unit.id
        feature = stratigraphic_unit.get_linked_entity_safe('P46', inverse=True)
        place = feature.get_linked_entity_safe('P46', inverse=True)
    elif object_.system_type == 'stratigraphic unit':
        feature = object_.get_linked_entity_safe('P46', inverse=True)
        super_id = feature.id
        place = feature.get_linked_entity_safe('P46', inverse=True)
    elif object_.system_type == 'feature':
        place = object_.get_linked_entity_safe('P46', inverse=True)
        super_id = place.id
    if object_:
        if object_.system_type not in ['find', 'human remains']:
            subunits = object_.get_linked_entities('P46', nodes=True)
    if super_:
        siblings = super_.get_linked_entities('P46')
    else:
        if object_.system_type == 'feature':
            siblings = place.get_linked_entities('P46')
        if object_.system_type == 'stratigraphic unit':
            siblings = feature.get_linked_entities('P46')
        if object_.system_type in ['find', 'human remains']:
            siblings = stratigraphic_unit.get_linked_entities('P46')
    return {'place': place,
            'feature': feature,
            'stratigraphic_unit': stratigraphic_unit,
            'super_id': super_id,
            'subunits': subunits,
            'siblings': siblings}
