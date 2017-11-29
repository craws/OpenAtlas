# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information

import datetime
from dateutil.relativedelta import relativedelta

import openatlas
from openatlas.models.linkProperty import LinkPropertyMapper
from .link import LinkMapper


class DateMapper(object):

    @staticmethod
    def get_dates(entity):
        sql = """
            SELECT e2.value_timestamp, e2.description, e2.system_type, l.property_code
            FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id
                AND l.property_code IN ('OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6')
            JOIN model.entity e2 ON l.range_id = e2.id
            WHERE e.id = %(id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity.id})
        dates = {}
        for row in cursor.fetchall():
            if row.property_code not in dates:
                dates[row.property_code] = {}
            dates[row.property_code][row.system_type] = {
                'timestamp': row.value_timestamp,
                'info': row.description if row.description else ''}
        openatlas.debug_model['div sql'] += 1
        return dates

    @staticmethod
    def get_link_dates(link):
        sql = """
            SELECT e.value_timestamp, e.description, e.system_type, p.code
            FROM model.link_property lp
            JOIN model.link l ON lp.domain_id = l.id
            JOIN model.entity e ON lp.range_id = e.id
            JOIN model.property p ON lp.property_id = p.id AND p.code in ('OA5', 'OA6')
            WHERE l.id = %(id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': link.id})
        dates = {}
        for row in cursor.fetchall():
            if row.code not in dates:
                dates[row.code] = {}
            dates[row.code][row.system_type] = {
                'timestamp': row.value_timestamp,
                'info': row.description if row.description else ''}
        openatlas.debug_model['div sql'] += 1
        return dates

    @staticmethod
    def save_dates(entity, form):
        # Todo: refactor to not delete/save dates if not changed
        if entity.dates:
            DateMapper.delete_dates(entity)
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
        DateMapper.save_date(entity.id, form, 'begin', code_begin, LinkMapper)
        DateMapper.save_date(entity.id, form, 'end', code_end, LinkMapper)

    @staticmethod
    def save_link_dates(link_id, form):
        DateMapper.save_date(link_id, form, 'begin', 'OA5', LinkPropertyMapper)
        DateMapper.save_date(link_id, form, 'end', 'OA6', LinkPropertyMapper)

    @staticmethod
    def delete_dates(entity):
        sql = """
            DELETE FROM model.entity WHERE id in (
                SELECT e.id FROM model.entity e
                JOIN model.link l ON e.id = l.range_id AND l.domain_id = %(entity_id)s
                    AND l.property_code IN ('OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6'));"""
        openatlas.get_cursor().execute(sql, {'entity_id': entity.id})
        openatlas.debug_model['div sql'] += 1
        return

    @staticmethod
    def save_date(id_, form, name, code, link_mapper):
        from openatlas.models.entity import EntityMapper
        from openatlas.util.util import create_date_from_form

        if not getattr(form, 'date_' + name + '_year').data:
            return
        description = getattr(form, 'date_' + name + '_info').data

        date = {}  # put date form values in a dictionary
        for item in ['year', 'month', 'day', 'year2', 'month2', 'day2']:
            value = getattr(form, 'date_' + name + '_' + item).data
            date[item] = int(value) if value else ''

        if not date['year2'] and date['month'] and date['year']:  # exact date
            date_from = create_date_from_form(date)
            exact_date = EntityMapper.insert('E61', '', 'exact date value', description, date_from)
            link_mapper.insert(id_, code, exact_date)
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

        date_from = EntityMapper.insert('E61', '', 'from date value', description, date_from)
        link_mapper.insert(id_, code, date_from)
        date_to = EntityMapper.insert('E61', '', 'to date value', None, date_to)
        link_mapper.insert(id_, code, date_to)
