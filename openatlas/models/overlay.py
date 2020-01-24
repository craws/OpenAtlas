from __future__ import annotations  # Needed for Python 4.0 type annotations

import os
from typing import Dict

from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.util.util import get_file_path


class Overlay:
    def __init__(self, row: NamedTupleCursor.Record) -> None:
        self.id = row.id
        self.name = row.name if hasattr(row, 'name') else ''
        self.image_id = row.image_id
        self.place_id = row.place_id
        self.bounding_box = row.bounding_box
        path = get_file_path(row.image_id)
        self.image_name = os.path.basename(path) if path else False

    @staticmethod
    def insert(form: FlaskForm, image_id: int, place_id: int, link_id: int) -> None:
        sql = """
            INSERT INTO web.map_overlay (image_id, place_id, link_id, bounding_box)
            VALUES (%(image_id)s, %(place_id)s, %(link_id)s, %(bounding_box)s);"""
        bounding_box = '[[{top_left_northing}, {top_left_easting}],' \
                       '[{bottom_right_northing}, {bottom_right_easting}]]'.format(
                        top_left_easting=form.top_left_easting.data,
                        top_left_northing=form.top_left_northing.data,
                        bottom_right_easting=form.bottom_right_easting.data,
                        bottom_right_northing=form.bottom_right_northing.data)
        g.execute(sql, {'image_id': image_id,
                        'place_id': place_id,
                        'link_id': link_id,
                        'bounding_box': bounding_box})

    @staticmethod
    def update(form: FlaskForm, image_id: int, place_id: int) -> None:
        sql = """
            UPDATE web.map_overlay SET bounding_box = %(bounding_box)s
            WHERE image_id = %(image_id)s AND place_id = %(place_id)s;"""
        bounding_box = '[[{top_left_northing}, {top_left_easting}],' \
                       '[{bottom_right_northing}, {bottom_right_easting}]]'.format(
                        top_left_easting=form.top_left_easting.data,
                        top_left_northing=form.top_left_northing.data,
                        bottom_right_easting=form.bottom_right_easting.data,
                        bottom_right_northing=form.bottom_right_northing.data)
        g.execute(sql, {'image_id': image_id, 'place_id': place_id, 'bounding_box': bounding_box})

    @staticmethod
    def get_by_object(object_: Entity) -> Dict[int, Overlay]:
        if not app.config['IS_UNIT_TEST'] and not current_user.settings['module_map_overlay']:
            return {}  # pragma: no cover - tests have no direct access to user settings

        ids = [object_.id]
        # Get overlays of parents
        if object_.system_type == 'find':
            stratigraphic_unit = object_.get_linked_entity_safe('P46', True)
            ids.append(stratigraphic_unit.id)
            feature = stratigraphic_unit.get_linked_entity_safe('P46', True)
            ids.append(feature.id)
            ids.append(feature.get_linked_entity_safe('P46', True).id)
        elif object_.system_type == 'stratigraphic unit':
            feature = object_.get_linked_entity_safe('P46', True)
            ids.append(feature.id)
            ids.append(feature.get_linked_entity_safe('P46', True).id)
        elif object_.system_type == 'feature':
            ids.append(object_.get_linked_entity_safe('P46', True).id)

        sql = """
            SELECT o.id, o.place_id, o.image_id, o.bounding_box, i.name
            FROM web.map_overlay o
            JOIN model.entity i ON o.image_id = i.id
            WHERE o.place_id IN %(place_ids)s;"""
        g.execute(sql, {'place_ids': tuple(ids)})
        return {row.image_id: Overlay(row) for row in g.cursor.fetchall()}

    @staticmethod
    def get_by_id(id_: int) -> Overlay:
        sql = 'SELECT id, place_id, image_id, bounding_box FROM web.map_overlay WHERE id = %(id)s;'
        g.execute(sql, {'id': id_})
        return Overlay(g.cursor.fetchone())

    @staticmethod
    def remove(id_: int) -> None:
        g.execute('DELETE FROM web.map_overlay WHERE id = %(id)s;', {'id': id_})
