from flask import g
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity


class ReferenceSystem:
    # Tools for reference systems like Wikidata or GeoNames

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
            SELECT name, website_url, resolver_url, locked
            FROM web.reference_system
            WHERE entity_id = %(entity_id)s;'''
        g.execute(sql, {'entity_id': id_})
        row = g.cursor.fetchone()
        entity.website_url = row.website_url
        entity.resolver_url = row.resolver_url
        return entity

    @staticmethod
    def get_all():
        reference_systems = []
        for entity in Entity.get_by_class_code('E32'):
            reference_systems.append(ReferenceSystem.get_by_id(entity.id))
        return reference_systems
