# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from astropy.time import Time

import openatlas
from openatlas.models.linkProperty import LinkPropertyMapper
from .link import LinkMapper


class DateMapper(object):

    @staticmethod
    def get_dates(entity):
        sql = """
            SELECT
                COALESCE(to_char(e2.value_timestamp, 'yyyy-mm-dd bc'), '') AS value_timestamp,
                e2.description,
                e2.system_type,
                l.property_code
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
                'date': DateMapper.timestamp_to_astropy(row.value_timestamp),
                'info': row.description if row.description else ''}
        openatlas.debug_model['div sql'] += 1
        return dates

    @staticmethod
    def timestamp_to_astropy(string):
        """Converts a timestamp string to an astropy time

        :param string: with the format "yyyy-mm-dd bc"
        :return: astropy.Time
        """
        bc_prefix = '-' if 'bc' in string else '+'
        string = string.split(' ')[0]  # remove bc/ad and time from string
        string = bc_prefix + '0' + string  # transform to longdate format
        astropy_date = Time(string, format='fits', out_subfmt='longdate')
        astropy_date.format = 'iso'
        return astropy_date

    @staticmethod
    def astropy_to_timestamp(date):
        """Converts an astropy time to a timestamp string

        :param date: astropy.Time
        :return: string with the format "yyyy-mm-dd bc"
        """
        string = str(date).split(' ')[0]  # remove time and rest from string
        bc = ' BC' if string.startswith('-') else ''
        parts = string[1:].split('-')
        string = parts[0].zfill(4) + '-' + parts[1] + '-' + parts[2] + bc
        return string

    @staticmethod
    def form_to_astropy(year, month, day):
        """Converts form fields (year, month, day) to an astropy time

        :param year: -4713 to 9999
        :param month: 1 to 12
        :param day: 1 to 31
        :return: astropy.Time
        """
        year = '+' + format(year, '05d') if year > 0 else format(year, '06d')
        month = format(month, '02d') if month else '01'
        day = format(day, '02d') if day else '01'
        string = year + '-' + month + '-' + day
        try:
            astropy_date = Time(string, format='fits', out_subfmt='longdate')
        except ValueError:
            return None
        return astropy_date

    @staticmethod
    def get_link_dates(link):
        """Fetches dates associated with a link

        :param link:
        :return: a dictionary with a date and additional information
        """
        sql = """
            SELECT
                COALESCE(to_char(e.value_timestamp, 'yyyy-mm-dd bc'), '') AS value_timestamp,
                e.description,
                e.system_type,
                lp.property_code
            FROM model.link_property lp
            JOIN model.link l ON lp.domain_id = l.id AND lp.property_code IN ('OA5', 'OA6')
            JOIN model.entity e ON lp.range_id = e.id
            WHERE l.id = %(id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': link.id})
        dates = {}
        for row in cursor.fetchall():
            if row.property_code not in dates:
                dates[row.property_code] = {}
            dates[row.property_code][row.system_type] = {
                'date': DateMapper.timestamp_to_astropy(row.value_timestamp),
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
            date_from = DateMapper.form_to_astropy(date['year'], date['month'], date['day'])
            date_from = EntityMapper.insert('E61', '', 'from date value', description, date_from)
            link_mapper.insert(id_, code, date_from)
            date_to = DateMapper.form_to_astropy(date['year2'], date['month2'], date['day2'])
            date_to = EntityMapper.insert('E61', '', 'to date value', None, date_to)
            link_mapper.insert(id_, code, date_to)
        else:  # exact date
            date = DateMapper.form_to_astropy(date['year'], date['month'], date['day'])
            exact_date = EntityMapper.insert('E61', '', 'exact date value', description, date)
            link_mapper.insert(id_, code, exact_date)
