from typing import Any

from flask import g
from flask_login import current_user

from openatlas.database import entity as db
from openatlas.models.entity import Entity


def search(data: dict[str, Any]) -> list[Entity]:
    if not data['term']:
        return []
    for class_ in data['classes']:
        if g.classes[class_].attributes.get('alias'):
            data['classes'].append('appellation')
            break
    entities = []
    for row in db.search(
            data['term'],
            data['classes'],
            data['desc'],
            data['own'],
            current_user.id):
        if row['openatlas_class_name'] == 'appellation':
            entity = Entity.get_linked_entity_safe_static(
                row['id'],
                'P1',
                inverse=True)
            if entity.class_.name not in data['classes']:
                continue
        else:
            entity = Entity(row)
        if entity and check_dates(entity, data):
            entities.append(entity)
    return list({d.id: d for d in entities}.values())  # Remove duplicates


def check_dates(entity: Entity, data: dict[str, Any]) -> bool:
    if not data['from_date'] and not data['to_date']:
        return True
    if not entity.dates.begin_from \
            and not entity.dates.begin_to \
            and not entity.dates.end_from \
            and not entity.dates.end_to:
        return bool(data['include_dateless'])
    dates = [
        entity.dates.begin_from,
        entity.dates.begin_to,
        entity.dates.end_from,
        entity.dates.end_to]
    begin_ok = False
    if not data['from_date']:
        begin_ok = True
    else:
        for date in dates:
            if date and date >= data['from_date']:
                begin_ok = True
    end_ok = False
    if not data['to_date']:
        end_ok = True
    else:
        for date in dates:
            if date and date <= data['to_date']:
                end_ok = True
    return bool(begin_ok and end_ok)
