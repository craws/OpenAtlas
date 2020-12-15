from typing import List, Tuple, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity


class ReferenceSystem:
    # Tools for reference systems like Wikidata or GeoNames

    @staticmethod
    def add_forms_to_system(entity: Entity, form: FlaskForm) -> None:
        for form_id in form.forms.data:
            sql = """
                INSERT INTO web.reference_system_form (reference_system_id, form_id)
                VALUES (%(entity_id)s, %(form_id)s);"""
            g.execute(sql, {'entity_id': entity.id, 'form_id': form_id})

    @staticmethod
    def get_form_choices(origin: Union[Entity, None]) -> List[Tuple[int, str]]:
        g.execute("SELECT f.id, f.name FROM web.form f WHERE f.name IN %(forms)s ORDER BY name ASC",
                  {'forms': tuple(['Event', 'Feature', 'Find', 'Group', 'Human_Remains',
                                   'Legal Body', 'Person', 'Place', 'Stratigraphic Unit'])})
        return [
            (r.id, r.name) for r in g.cursor.fetchall() if not origin or r.id not in origin.forms]

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
    def update(entity: Entity, form: FlaskForm):
        entity.update()
        sql = '''
            UPDATE web.reference_system SET (name, website_url, resolver_url) =
            (%(name)s, %(website_url)s, %(resolver_url)s) WHERE entity_id = %(entity_id)s;'''
        g.execute(sql, {'entity_id': entity.id,
                        'name': entity.name,
                        'website_url': form.website_url.data if form.website_url.data else None,
                        'resolver_url': form.resolver_url.data if form.resolver_url.data else None})

    @staticmethod
    def get_by_id(id_: int) -> Entity:
        entity = Entity.get_by_id(id_)
        sql = '''
            SELECT rs.name, rs.website_url, rs.resolver_url, rs.locked,
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
        return entity

    @staticmethod
    def get_all():
        reference_systems = []
        for entity in Entity.get_by_class_code('E32'):
            reference_systems.append(ReferenceSystem.get_by_id(entity.id))
        return reference_systems
