# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information

import datetime
from dateutil.relativedelta import relativedelta

import openatlas
from .link import LinkMapper


class DateMapper(object):

    @staticmethod
    def get_dates(entity):
        sql = '''
            SELECT e2.value_timestamp, e2.description, p.code, e3.name AS type_name
            FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id
            JOIN model.entity e2 ON l.range_id = e2.id
            JOIN model.link l2 ON l.range_id = l2.domain_id
            JOIN model.entity e3 ON l2.range_id = e3.id
            JOIN model.property p ON l.property_id = p.id AND p.code in ('OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6')
            WHERE e.id = %(id)s;'''
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity.id})
        dates = {}
        for row in cursor.fetchall():
            if row.code not in dates:
                dates[row.code] = {}
            dates[row.code][row.type_name] = {'timestamp': row.value_timestamp, 'info': row.description}
        openatlas.debug_model['div sql'] += 1
        return dates

    @staticmethod
    def save_dates(entity, form):
        code_begin = 'OA1'
        code_end = 'OA2'
        if entity.class_.name in ['Activity', 'Destruction', 'Acquisition', 'Production']:
            code_begin = 'OA5'
            code_end = 'OA6'
        if entity.class_.name == 'Person':
            if form.date_birth.data:
                code_begin = 'OA3'
            if form.date_death.data:
                code_end = 'OA4'
        DateMapper.save_date(entity, form, 'begin', code_begin)
        DateMapper.save_date(entity, form, 'end', code_end)

    @staticmethod
    def delete_dates(entity):
        sql = '''
            DELETE FROM model.entity WHERE id in (
                SELECT e.id FROM model.entity e
                JOIN model.link l ON e.id = l.range_id AND l.domain_id = %(entity_id)s
                JOIN model.class c ON e.class_id = c.id AND c.code = 'E61');'''
        openatlas.get_cursor().execute(sql, {'entity_id': entity.id})
        openatlas.debug_model['div sql'] += 1
        return

    @staticmethod
    def save_date(entity, form, name, code):
        from openatlas.models.entity import EntityMapper
        from openatlas.models.node import NodeMapper
        from openatlas.util.util import create_date_from_form

        if not getattr(form, 'date_' + name + '_year').data:
            return

        description = getattr(form, 'date_' + name + '_info').data
        nodes = {}  # get date types for later use
        for node_id in NodeMapper.get_hierarchy_by_name('Date value type').subs:
            nodes[openatlas.nodes[node_id].name] = node_id
        date = {}  # put date form values in a dictionary
        for item in ['year', 'month', 'day', 'year2', 'month2', 'day2']:
            value = getattr(form, 'date_' + name + '_' + item).data
            date[item] = int(value) if value else ''

        if not date['year2'] and date['month'] and date['year']:  # exact date
            date_from = create_date_from_form(date)
            exact_date_id = EntityMapper.insert('E61', '', description, date_from)
            LinkMapper.insert(exact_date_id, 'P2', nodes['Exact date value'])
            LinkMapper.insert(entity.id, code, exact_date_id)
            return

        if date['year2']:
            date_from = create_date_from_form(date)
            date_to = create_date_from_form(date, '2')
        else:  # try to guess time spans from incomplete "from date"
            if date['month'] and not date['day']:
                date_from = create_date_from_form(date)
                date_to = (date_from + relativedelta(months=1)) - datetime.timedelta(days=1)
            else:
                date_from = create_date_from_form(date)
                date_to = (date_from + relativedelta(years=1)) - datetime.timedelta(days=1)

        date_from_id = EntityMapper.insert('E61', '', description, date_from)
        LinkMapper.insert(date_from_id, 'P2', nodes['From date value'])
        LinkMapper.insert(entity.id, code, date_from_id)
        date_to_id = EntityMapper.insert('E61', '', '', date_to)
        LinkMapper.insert(date_to_id, 'P2', nodes['To date value'])
        LinkMapper.insert(entity.id, code, date_to_id)
