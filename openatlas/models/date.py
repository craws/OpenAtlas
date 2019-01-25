# Created by Alexander Watzinger and others. Please see README.md for licensing information
import numpy
from datetime import datetime


class DateMapper:

    @staticmethod
    def current_date_for_filename():
        today = datetime.today()
        return '{year}-{month}-{day}_{hour}{minute}'.format(
            year=today.year,
            month=str(today.month).zfill(2),
            day=str(today.day).zfill(2),
            hour=str(today.hour).zfill(2),
            minute=str(today.minute).zfill(2))

    @staticmethod
    def timestamp_to_datetime64(string):
        """ Converts a timestamp string to a numpy.datetime64
        :param string: PostgreSQL timestamp
        :return: numpy.datetime64
        """
        if not string:
            return None
        if 'BC' in string:
            parts = string.split(' ')[0].split('-')
            string = '-' + str(int(parts[0]) - 1) + '-' + parts[1] + '-' + parts[2]
        return numpy.datetime64(string.split(' ')[0])

    @staticmethod
    def datetime64_to_timestamp(date):
        """ Converts a numpy.datetime64 to a timestamp string
        :param date: numpy.datetime64
        :return: PostgreSQL timestamp
        """
        if not date:
            return None
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
        """ Converts form fields (year, month, day) to a numpy.datetime64
        :param year: -4713 to 9999
        :param month: 1 to 12
        :param day: 1 to 31
        :return: numpy.datetime64
        """
        if not year:
            return None
        year = format(year, '03d') if year > 0 else format(year + 1, '04d')
        month = format(month, '02d') if month else '01'
        day = format(day, '02d') if day else '01'
        string = str(year) + '-' + str(month) + '-' + str(day)
        try:
            datetime_ = numpy.datetime64(string)
        except ValueError:
            return None
        return datetime_

    @staticmethod
    def get_invalid_dates():
        """ Search for entities with invalid date combinations, e.g. begin after end"""
        return []

    @staticmethod
    def get_invalid_link_dates():
        """ Search for links with invalid date combinations, e.g. begin after end"""
        return []
