# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import NoneOf, NumberRange, Optional

from openatlas.models.date import DateMapper


class DateForm(Form):

    @staticmethod
    def format_date(date, part):
        """If it's a negative year, add one year

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
        if part == 'year':
            return '-' + str(int(parts[0]) + 1) if bc else parts[0]
        if part == 'month':
            return parts[1]
        return parts[2]

    def populate_dates(self, param):
        """Populates the date form fields with date values of an entity or link

        :param param: an entity or a link
        """
        for code, types in param.dates.items():
            if code in ['OA1', 'OA3', 'OA5']:
                for type_, date in types.items():
                    if type_ in ['exact date value', 'from date value']:
                        self.date_begin_year.data = DateForm.format_date(date['date'], 'year')
                        self.date_begin_month.data = DateForm.format_date(date['date'], 'month')
                        self.date_begin_day.data = DateForm.format_date(date['date'], 'day')
                        self.date_begin_info.data = date['info']
                    else:
                        self.date_begin_year2.data = DateForm.format_date(date['date'], 'year')
                        self.date_begin_month2.data = DateForm.format_date(date['date'], 'month')
                        self.date_begin_day2.data = DateForm.format_date(date['date'], 'day')
            else:
                for type_, date in types.items():
                    if type_ in ['exact date value', 'from date value']:
                        self.date_end_year.data = DateForm.format_date(date['date'], 'year')
                        self.date_end_month.data = DateForm.format_date(date['date'], 'month')
                        self.date_end_day.data = DateForm.format_date(date['date'], 'day')
                        self.date_end_info.data = date['info']
                    else:
                        self.date_end_year2.data = DateForm.format_date(date['date'], 'year')
                        self.date_end_month2.data = DateForm.format_date(date['date'], 'month')
                        self.date_end_day2.data = DateForm.format_date(date['date'], 'day')
            if code == 'OA3':
                self.date_birth.data = True
            if code == 'OA4':
                self.date_death.data = True

    date_birth = BooleanField(_('birth'))
    date_death = BooleanField(_('death'))

    date_begin_year = IntegerField(
        _('begin'),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])])
    date_begin_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)])
    date_begin_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)])
    date_begin_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])])
    date_begin_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)])
    date_begin_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)])
    date_begin_info = StringField(render_kw={'placeholder': _('comment')},)
    date_end_year = IntegerField(
        _('end'),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])])
    date_end_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)])
    date_end_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)])
    date_end_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])])
    date_end_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)])
    date_end_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)])
    date_end_info = StringField(render_kw={'placeholder': _('comment')})

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        fields = {}  # put date form values in a dictionary
        for name in ['begin', 'end']:
            for item in ['year', 'month', 'day', 'year2', 'month2', 'day2']:
                value = getattr(self, 'date_' + name + '_' + item).data
                fields[name + '_' + item] = int(value) if value else ''

        # check if dates have a valid format
        dates = {}
        for name in ['begin', 'end']:
            for postfix in ['', '2']:
                if fields[name + '_' + 'year' + postfix]:
                    date = DateMapper.form_to_datetime64(
                        fields[name + '_' + 'year' + postfix],
                        fields[name + '_' + 'month' + postfix],
                        fields[name + '_' + 'day' + postfix]
                    )
                    if not date:
                        field = getattr(self, 'date_' + name + '_' + 'day' + postfix)
                        field.errors.append(_('not a valid date'))
                        valid = False
                    else:
                        dates[name + postfix] = date  # put dates into a dictionary

        # check if date spans are in itself valid
        if valid:
            for name in ['begin', 'end']:
                if name in dates and name + '2' in dates:
                    if dates[name] > dates[name + '2']:
                        field = getattr(self, 'date_' + name + '_day')
                        field.errors.append(_('First date cannot be after second.'))
                        valid = False

        # check if begin dates are before ends dates
        if valid and 'begin' in dates and 'end' in dates:
            field = getattr(self, 'date_begin_day')
            if len(dates) == 4:  # all dates are used
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
