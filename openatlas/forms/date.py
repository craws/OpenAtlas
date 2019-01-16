# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import NoneOf, NumberRange, Optional

from openatlas.models.date import DateMapper


class DateForm(Form):

    @staticmethod
    def format_date(date, part):
        """
        :param date: a date string
        :param part: year, month or day
        :return: string presentation of the date part for the form
        """
        string = str(date).split(' ')[0]
        bc = False
        if string.startswith('-') or string.startswith('0000'):
            bc = True
            string = string[1:]
        parts = string.split('-')
        if part == 'year':  # If it's a negative year, add one year
            return '-' + str(int(parts[0]) + 1) if bc else parts[0]
        if part == 'month':
            return parts[1]
        return parts[2]

    def populate_dates(self, item):
        """ Populates date form fields with date values of an entity or link."""
        self.begin_year.data = DateForm.format_date(item.begin_from, 'year')
        self.begin_month.data = DateForm.format_date(item.begin_from, 'month')
        self.begin_day.data = DateForm.format_date(item.begin_from, 'day')
        self.begin_info.data = item.begin_from_comment

        self.begin_year2.data = DateForm.format_date(item.begin_to, 'year')
        self.begin_month2.data = DateForm.format_date(item.begin_to, 'month')
        self.begin_day2.data = DateForm.format_date(item.begin_to, 'day')

        self.end_year.data = DateForm.format_date(item.end_to, 'year')
        self.end_month.data = DateForm.format_date(item.end_to, 'month')
        self.end_day.data = DateForm.format_date(item.end_to, 'day')
        self.end_info.data = item.end_comment

        self.end_year2.data = DateForm.format_date(item.end_from, 'year')
        self.end_month2.data = DateForm.format_date(item.end_from, 'month')
        self.end_day2.data = DateForm.format_date(item.end_from, 'day')

    validator_day = [Optional(), NumberRange(min=1, max=31)]
    validator_month = [Optional(), NumberRange(min=1, max=12)]
    validator_year = [Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])]

    begin_year = IntegerField(_('begin'), render_kw={'placeholder': _('yyyy')},
                              validators=validator_year)
    begin_month = IntegerField(render_kw={'placeholder': _('mm')}, validators=validator_month)
    begin_day = IntegerField(render_kw={'placeholder': _('dd')}, validators=validator_day)
    begin_year2 = IntegerField(render_kw={'placeholder': _('yyyy')}, validators=validator_year)
    begin_month2 = IntegerField(render_kw={'placeholder': _('mm')}, validators=validator_month)
    begin_day2 = IntegerField(render_kw={'placeholder': _('dd')}, validators=validator_day)
    begin_info = StringField(render_kw={'placeholder': _('comment')},)
    end_year = IntegerField(_('end'), render_kw={'placeholder': _('yyyy')},
                            validators=validator_year)
    end_month = IntegerField(render_kw={'placeholder': _('mm')}, validators=validator_month)
    end_day = IntegerField(render_kw={'placeholder': _('dd')}, validators=validator_day)
    end_year2 = IntegerField(render_kw={'placeholder': _('yyyy')}, validators=validator_year)
    end_month2 = IntegerField(render_kw={'placeholder': _('mm')}, validators=validator_month)
    end_day2 = IntegerField(render_kw={'placeholder': _('dd')}, validators=validator_day)
    end_info = StringField(render_kw={'placeholder': _('comment')})

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        fields = {}  # put date form values in a dictionary
        for name in ['begin', 'end']:
            for item in ['year', 'month', 'day', 'year2', 'month2', 'day2']:
                value = getattr(self, name + '_' + item).data
                fields[name + '_' + item] = int(value) if value else ''

        # Check date format, if valid put dates into a dictionary
        dates = {}
        for name in ['begin', 'end']:
            for postfix in ['', '2']:
                if fields[name + '_' + 'year' + postfix]:
                    date = DateMapper.form_to_datetime64(
                        fields[name + '_' + 'year' + postfix],
                        fields[name + '_' + 'month' + postfix],
                        fields[name + '_' + 'day' + postfix])
                    if not date:
                        field = getattr(self, name + '_' + 'day' + postfix)
                        field.errors.append(_('not a valid date'))
                        valid = False
                    else:
                        dates[name + postfix] = date

        # Check for valid date combination e.g. begin not after end
        if valid:
            for name in ['begin', 'end']:
                if name in dates and name + '2' in dates:
                    if dates[name] > dates[name + '2']:
                        field = getattr(self, name + '_day')
                        field.errors.append(_('First date cannot be after second.'))
                        valid = False
        if valid and 'begin' in dates and 'end' in dates:
            field = getattr(self, 'begin_day')
            if len(dates) == 4:  # All dates are used
                if dates['begin'] > dates['end'] or dates['begin2'] > dates['end2']:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False
            else:
                first = dates['begin2'] if 'begin2' in dates else dates['begin']
                second = dates['end'] if 'end' in dates else dates['end2']
                if first > second:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False
        return valid
