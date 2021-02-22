from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Dict, List, Tuple, Union

from flask import g
from flask_wtf import FlaskForm
from psycopg2.extras import NamedTupleCursor

from openatlas import app
from openatlas.models.entity import Entity


class ReferenceSystem(Entity):
    # Class for external reference systems like Wikidata or GeoNames
    website_url = None
    resolver_url = None
    placeholder = None
    system = False

    def __init__(self, row: NamedTupleCursor.Record) -> None:

        super().__init__(row)
        self.website_url = row.website_url
        self.resolver_url = row.resolver_url
        self.forms = row.form_ids
        self.placeholder = row.identifier_example
        self.precision_default_id = row.precision_default_id
        self.count = row.count
        self.system = row.system

    @staticmethod
    def get_all() -> Dict[int, ReferenceSystem]:
        sql = """
            SELECT
                e.id, e.name, e.class_code, e.description, e.system_class, e.created, e.modified,
                rs.website_url, rs.resolver_url, rs.identifier_example, rs.system,
                rs.precision_default_id, COUNT(l.id) AS count,
                (SELECT ARRAY(
                    SELECT f.id FROM web.form f
                    JOIN web.reference_system_form rfs ON f.id = rfs.form_id
                        AND rfs.reference_system_id = rs.entity_id)) AS form_ids,
                array_to_json(
                    array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
                ) AS nodes
            FROM model.entity e
            JOIN web.reference_system rs ON e.id = rs.entity_id
            LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code = 'P67'
            LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code = 'P2'
            GROUP BY
                e.id, e.name, e.class_code, e.description, e.system_class, e.created,
                e.modified, rs.website_url, rs.resolver_url, rs.identifier_example, rs.system,
                rs.precision_default_id, rs.entity_id;"""
        g.execute(sql)
        return {row.id: ReferenceSystem(row) for row in g.cursor.fetchall()}

    @staticmethod
    def get_by_name(name: str) -> ReferenceSystem:
        for system in g.reference_systems.values():
            if system.name == name:
                return system

    def add_forms(self, form: FlaskForm) -> None:
        for form_id in form.forms.data:
            sql = """
                INSERT INTO web.reference_system_form (reference_system_id, form_id)
                VALUES (%(entity_id)s, %(form_id)s);"""
            g.execute(sql, {'entity_id': self.id, 'form_id': form_id})

    def remove_form(self, form_id: int) -> None:
        sql = """
            DELETE FROM web.reference_system_form
            WHERE reference_system_id = %(reference_system_id)s AND form_id = %(form_id)s;"""
        g.execute(sql, {'reference_system_id': self.id, 'form_id': form_id})

    def get_forms(self) -> Dict[int, Dict[str, str]]:
        sql = """
            SELECT f.id, f.name FROM web.form f
            JOIN web.reference_system_form rsf ON f.id = rsf.form_id
                AND rsf.reference_system_id = %(id)s;"""
        g.execute(sql, {'id': self.id})
        return {row.id: {'name': row.name} for row in g.cursor.fetchall()}

    def update_system(self, form: FlaskForm) -> None:
        self.update(form)
        precision_default_id = None
        entity_with_updated_nodes = Entity.get_by_id(self.id, nodes=True)
        if entity_with_updated_nodes.nodes:  # Get default precision id if it was set
            precision_default_id = list(entity_with_updated_nodes.nodes.keys())[0].id
        sql = '''
            UPDATE web.reference_system SET (name, website_url, resolver_url, identifier_example,
                precision_default_id)
            = (%(name)s, %(website_url)s, %(resolver_url)s, %(identifier_example)s,
                %(precision_default_id)s)
            WHERE entity_id = %(entity_id)s;'''
        g.execute(sql, {'entity_id': self.id,
                        'name': self.name,
                        'website_url': self.website_url,
                        'resolver_url': self.resolver_url,
                        'identifier_example': self.placeholder,
                        'precision_default_id': precision_default_id})

    @staticmethod
    def update_links(form: FlaskForm, entity: Entity) -> None:
        for field in form:
            if field.id.startswith('reference_system_id_'):  # Delete and recreate link
                system = Entity.get_by_id(int(field.id.replace('reference_system_id_', '')))
                precision_field = getattr(form, field.id.replace('id_', 'precision_'))
                sql = """
                    DELETE FROM model.link WHERE property_code = 'P67'
                    AND domain_id = %(system_id)s AND range_id = %(entity_id)s;"""
                g.execute(sql, {'system_id': system.id, 'entity_id': entity.id})
                if field.data:
                    system.link('P67', entity, field.data, type_id=precision_field.data)

    @staticmethod
    def get_form_choices(entity: Union[ReferenceSystem, None]) -> List[Tuple[int, str]]:
        g.execute("SELECT f.id, f.name FROM web.form f WHERE f.name IN %(forms)s ORDER BY name ASC",
                  {'forms': tuple(app.config['EXTERNAL_REFERENCES_FORMS'])})
        choices = []
        for row in g.cursor.fetchall():
            if not entity or row.id not in entity.forms:
                if entity and entity.name == 'GeoNames' and row.name != 'Place':
                    continue
                choices.append((row.id, row.name))
        return choices

    @staticmethod
    def insert_system(form: FlaskForm) -> Entity:
        entity = Entity.insert('E32', form.name.data, description=form.description.data)
        sql = '''
            INSERT INTO web.reference_system (entity_id, name, website_url, resolver_url)
            VALUES (%(entity_id)s, %(name)s, %(website_url)s, %(resolver_url)s);'''
        g.execute(sql, {'entity_id': entity.id,
                        'name': entity.name,
                        'website_url': form.website_url.data if form.website_url.data else None,
                        'resolver_url': form.resolver_url.data if form.resolver_url.data else None})
        return ReferenceSystem.get_all()[entity.id]
