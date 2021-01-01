from typing import List, Tuple, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.node import Node


class ReferenceSystem:
    # Functions for external reference systems like Wikidata or GeoNames

    @staticmethod
    def add_forms(entity: Entity, form: FlaskForm) -> None:
        for form_id in form.forms.data:
            sql = """
                INSERT INTO web.reference_system_form (reference_system_id, form_id)
                VALUES (%(entity_id)s, %(form_id)s);"""
            g.execute(sql, {'entity_id': entity.id, 'form_id': form_id})

    @staticmethod
    def remove_form(entity_id: int, form_id: int) -> None:
        sql = """
            DELETE FROM web.reference_system_form
            WHERE reference_system_id = %(reference_system_id)s AND form_id = %(form_id)s;"""
        g.execute(sql, {'reference_system_id': entity_id, 'form_id': form_id})

    @staticmethod
    def get_forms(entity_id: int):
        sql = """
            SELECT f.id, f.name FROM web.form f
            JOIN web.reference_system_form rsf ON f.id = rsf.form_id
                AND rsf.reference_system_id = %(id)s;"""
        g.execute(sql, {'id': entity_id})
        return {row.id: {'name': row.name} for row in g.cursor.fetchall()}

    @staticmethod
    def get_form_choices(entity: Union[Entity, None]) -> List[Tuple[int, str]]:
        g.execute("SELECT f.id, f.name FROM web.form f WHERE f.name IN %(forms)s ORDER BY name ASC",
                  {'forms': tuple(app.config['EXTERNAL_REFERENCES_FORMS'])})
        return [
            (r.id, r.name) for r in g.cursor.fetchall() if not entity or r.id not in entity.forms]

    @staticmethod
    def insert(form: FlaskForm) -> Entity:
        entity = Entity.insert('E32', form.name.data, description=form.description.data)
        sql = '''
            INSERT INTO web.reference_system (entity_id, name, website_url, resolver_url)
            VALUES (%(entity_id)s, %(name)s, %(website_url)s, %(resolver_url)s);'''
        g.execute(sql, {'entity_id': entity.id,
                        'name': entity.name,
                        'website_url': form.website_url.data if form.website_url.data else None,
                        'resolver_url': form.resolver_url.data if form.resolver_url.data else None})
        return ReferenceSystem.get_by_id(entity.id)

    @staticmethod
    def update(entity: Entity, form: FlaskForm) -> None:
        entity.update(form)
        precision_default_id = None
        entity_with_updated_nodes = Entity.get_by_id(entity.id, nodes=True)
        if entity_with_updated_nodes.nodes:
            precision_default_id = list(entity_with_updated_nodes.nodes.keys())[0].id
        sql = '''
            UPDATE web.reference_system SET (name, website_url, resolver_url, identifier_example,
                precision_default_id)
            = (%(name)s, %(website_url)s, %(resolver_url)s, %(identifier_example)s,
                %(precision_default_id)s)
            WHERE entity_id = %(entity_id)s;'''
        g.execute(sql, {'entity_id': entity.id,
                        'name': entity.name,
                        'website_url': entity.website_url,
                        'resolver_url': entity.resolver_url,
                        'identifier_example': entity.placeholder,
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
    def get_by_id(id_: int) -> Entity:
        entity = Entity.get_by_id(id_, nodes=True)
        sql = '''
            SELECT rs.name, rs.website_url, rs.resolver_url, rs.identifier_example, rs.locked,
                rs.precision_default_id,
            (SELECT ARRAY(
                SELECT f.id FROM web.form f JOIN web.reference_system_form rfs ON f.id = rfs.form_id
                AND rfs.reference_system_id = rs.entity_id)) AS form_ids
            FROM web.reference_system AS rs
            WHERE rs.entity_id = %(entity_id)s;'''
        g.execute(sql, {'entity_id': id_})
        row = g.cursor.fetchone()
        entity.website_url = row.website_url
        entity.resolver_url = row.resolver_url
        entity.forms = row.form_ids
        entity.placeholder = row.identifier_example
        entity.precision_default_id = row.precision_default_id
        return entity

    @staticmethod
    def get_all():
        reference_systems = []
        for entity in Entity.get_by_class_code('E32'):
            reference_systems.append(ReferenceSystem.get_by_id(entity.id))
        return reference_systems
