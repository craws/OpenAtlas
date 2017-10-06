# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas


class Link(object):

    def __init__(self, row):
        self.id = row.id
        self.property = openatlas.properties[row.property_id]
        self.domain = openatlas.EntityMapper.get_by_id(row.domain_id)
        self.range = openatlas.EntityMapper.get_by_id(row.range_id)

    # def delete(self):
    #    LinkMapper.delete(self)


class LinkMapper(object):

    @staticmethod
    def insert(domain, property_code, range_):
        if not domain or not range_:
            return
        range_ = range_ if isinstance(range_, list) else [range_]
        for range_param in range_:
            if not range_param:
                continue
            domain_id = domain.id if type(domain) is openatlas.Entity else int(domain)
            range_id = range_param.id if type(range_param) is openatlas.Entity else int(range_param)
            sql = """
                INSERT INTO model.link (property_id, domain_id, range_id)
                VALUES ((
                    SELECT id FROM model.property
                    WHERE code = %(property_code)s), %(domain_id)s, %(range_id)s);"""
            # Todo: build only sql and get execution out of loop
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {
                'property_code': property_code,
                'domain_id': domain_id,
                'range_id': range_id})
            openatlas.debug_model['div sql'] += 1

    # @staticmethod
    # def get_linked_entity(entity, property_name, inverse=False):
    #     sql = """
    #         SELECT range_id AS result_id
    #         FROM model.link
    #         WHERE domain_id = %(entity_id)s AND property_id = %(property_id)s;"""
    #     if inverse:
    #         sql = """
    #             SELECT domain_id AS result_id
    #             FROM model.link
    #             WHERE range_id = %(entity_id)s AND property_id = %(property_id)s;"""
    #     cursor = openatlas.get_cursor()
    #     cursor.execute(sql, {
    #         'entity_id': entity.id,
    #         'property_id': openatlas.PropertyMapper.get_id_by_name(property_name)})
    #     row = cursor.fetchone()
    #     openatlas.debug['linked entity'] += 1
    #     if row:
    #         return openatlas.EntityMapper.get_by_id(row.result_id)
    #     return
    #
    # @staticmethod
    # def get_linked_entities(entity, property_names, inverse=False):
    #     property_names = property_names if isinstance(property_names, list) else [property_names]
    #     cursor = openatlas.get_cursor()
    #     sql = """
    #         SELECT range_id AS result_id
    #         FROM model.link
    #         WHERE domain_id = %(entity_id)s AND property_id IN %(property_ids)s;"""
    #     if inverse:
    #         sql = """
    #             SELECT domain_id AS result_id
    #             FROM model.link
    #             WHERE range_id = %(entity_id)s AND property_id IN %(property_ids)s;"""
    #     cursor.execute(sql, {
    #         'entity_id': entity.id,
    #         'property_ids': tuple(openatlas.PropertyMapper.get_ids_by_names(property_names))})
    #     rows = cursor.fetchall()
    #     ids = []  # To do: get ids in one go instead with for loop, transform result somehow
    #     for row in rows:
    #         ids.append(row.result_id)
    #     openatlas.debug['linked entities'] += 1
    #     return openatlas.EntityMapper.get_by_ids(rows)
    #
    # @staticmethod
    # def get_link(entity, property_name):
    #     links = LinkMapper.get_links(entity, property_name)
    #     if len(links) == 0:
    #         return  # pragma: no cover
    #     if len(links) == 1:
    #         return links[0]
    #     return 'link.get_link() returned more than one for: ' + property_name  # pragma: no cover
    #
    # @staticmethod
    # def get_links(entity, property_names, inverse=False):
    #     links = []
    #     property_names = property_names if isinstance(property_names, list) else [property_names]
    #     sql = """
    #         SELECT l.id, l.property_id, l.domain_id, l.range_id FROM model.link l
    #         JOIN model.entity e ON l.domain_id = e.id AND l.domain_id = %(entity_id)s
    #         WHERE l.property_id IN %(property_ids)s
    #         ORDER BY e.name;"""
    #     if inverse:
    #         sql = """
    #         SELECT l.id, l.property_id, l.domain_id, l.range_id FROM model.link l
    #         JOIN model.entity e ON l.range_id = e.id AND l.range_id = %(entity_id)s
    #         WHERE l.property_id IN %(property_ids)s
    #         ORDER BY e.name;"""
    #     cursor = openatlas.get_cursor()
    #     cursor.execute(sql, {
    #         'entity_id': entity.id,
    #         'property_ids': tuple(openatlas.PropertyMapper.get_ids_by_names(property_names))})
    #     for row in cursor.fetchall():
    #         links.append(Link(row))
    #     return links
    #
    # @staticmethod
    # def delete(links):
    #     if not links:
    #         return
    #     links = links if type(links) is list else [links]
    #     link_ids = []
    #     for link in links:
    #         link_ids.append(link.id)
    #     cursor = openatlas.get_cursor()
    #     cursor.execute("DELETE FROM model.link WHERE id IN %(ids)s;", {'ids': tuple(link_ids)})
