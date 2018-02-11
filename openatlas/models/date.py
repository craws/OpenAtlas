# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import numpy
from flask import g

import openatlas
from openatlas.models.linkProperty import LinkPropertyMapper
from .link import LinkMapper


class DateMapper:

    @staticmethod
    def get_dates(entity):
        sql = """
            SELECT
                COALESCE(to_char(e2.value_timestamp, 'yyyy-mm-dd BC'), '') AS value_timestamp,
                e2.description,
                e2.system_type,
                l.property_code
            FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id
                AND l.property_code IN ('OA1', 'OA2', 'OA3', 'OA4', 'OA5', 'OA6')
            JOIN model.entity e2 ON l.range_id = e2.id
            WHERE e.id = %(id)s;"""
        g.cursor.execute(sql, {'id': entity.id})
        dates = {}
        for row in g.cursor.fetchall():
            if row.property_code not in dates:
                dates[row.property_code] = {}
            dates[row.property_code][row.system_type] = {
                'date': DateMapper.timestamp_to_datetime64(row.value_timestamp),
                'info': row.description if row.description else ''}
        openatlas.debug_model['div sql'] += 1
        return dates

    @staticmethod
    def timestamp_to_datetime64(string):
        """Converts a timestamp string to a numpy.datetime64


        :param string: PostgreSQL timestamp
        :return: numpy.datetime64
        """
        if 'BC' in string:
            parts = string.split(' ')[0].split('-')
            string = '-' + str(int(parts[0]) - 1) + '-' + parts[1] + '-' + parts[2]
        datetime = numpy.datetime64(string.split(' ')[0])
        return datetime

    @staticmethod
    def datetime64_to_timestamp(date):
        """Converts a numpy.datetime64 to a timestamp string

        :param date: numpy.datetime64
        :return: PostgreSQL timestamp
        """
        string = str(date)
        postfix = ''
        if string.startswith('-') or string.startswith('0000'):
            string = string[1:]
            postfix = ' BC'
        parts = string.split('-')
        year = int(parts[0]) + 1 if postfix else int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        string = format(year, '04d') + '-' + format(month, '02d') + '-' + format(day, '02d')
        return string + postfix

    @staticmethod
    def form_to_datetime64(year, month, day):
        """Converts form fields (year, month, day) to a numpy.datetime64

        :param year: -4713 to 9999
        :param month: 1 to 12
        :param day: 1 to 31
        :return: numpy.datetime64
        """
        year = format(year, '03d') if year > 0 else format(year + 1, '04d')
        month = format(month, '02d') if month else '01'
        day = format(day, '02d') if day else '01'
        string = str(year) + '-' + str(month) + '-' + str(day)
        try:
            datetime = numpy.datetime64(string)
        except ValueError:
            return None
        return datetime

    @staticmethod
    def get_link_dates(link):
        """Fetches dates associated with a link

        :param link:
        :return: a dictionary with a date and additional information
        """
        sql = """
            SELECT
                COALESCE(to_char(e.value_timestamp, 'yyyy-mm-dd BC'), '') AS value_timestamp,
                e.description,
                e.system_type,
                lp.property_code
            FROM model.link_property lp
            JOIN model.link l ON lp.domain_id = l.id AND lp.property_code IN ('OA5', 'OA6')
            JOIN model.entity e ON lp.range_id = e.id
            WHERE l.id = %(id)s;"""
        g.cursor.execute(sql, {'id': link.id})
        dates = {}
        for row in g.cursor.fetchall():
            if row.property_code not in dates:
                dates[row.property_code] = {}
            dates[row.property_code][row.system_type] = {
                'date': DateMapper.timestamp_to_datetime64(row.value_timestamp),
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
        g.cursor.execute(sql, {'entity_id': entity.id})
        openatlas.debug_model['div sql'] += 1

    @staticmethod
    def save_date(id_, form, name, code, link_mapper):
        """Saves a date taken from a form and links it

        :param id_: id of an entity of link
        :param form: a form with date fields
        :param name: can be a string with the values "begin" or "end"
        :param code: an OpenAtlas shortcut code e.g. 'OA5'
        :param link_mapper: whether to use LinkMapper (for entity) or LinkPropertyMapper (for link)
        :return:
        """
        from openatlas.models.entity import EntityMapper

        if not getattr(form, 'date_' + name + '_year').data:
            return  # return because no year given
        description = getattr(form, 'date_' + name + '_info').data

        date = {}  # put date form values in a dictionary
        for item in ['year', 'month', 'day', 'year2', 'month2', 'day2']:
            value = getattr(form, 'date_' + name + '_' + item).data
            date[item] = int(value) if value else ''

        if date['year2']:  # time span
            date_from = DateMapper.form_to_datetime64(date['year'], date['month'], date['day'])
            date_from = EntityMapper.insert('E61', '', 'from date value', description, date_from)
            link_mapper.insert(id_, code, date_from)
            date_to = DateMapper.form_to_datetime64(date['year2'], date['month2'], date['day2'])
            date_to = EntityMapper.insert('E61', '', 'to date value', None, date_to)
            link_mapper.insert(id_, code, date_to)
        else:  # exact date
            date = DateMapper.form_to_datetime64(date['year'], date['month'], date['day'])
            exact_date = EntityMapper.insert('E61', '', 'exact date value', description, date)
            link_mapper.insert(id_, code, exact_date)
