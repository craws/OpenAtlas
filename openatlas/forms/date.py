# Created by Alexander Watzinger and others. Please see README.md for licensing information
import numpy
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import NoneOf, NumberRange, Optional

from openatlas.models.date import DateMapper


class DateForm(FlaskForm):

    validator_day = [Optional(), NumberRange(min=1, max=31)]
    validator_month = [Optional(), NumberRange(min=1, max=12)]
    validator_year = [Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])]

    begin_year_from = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    begin_month_from = IntegerField(render_kw={'placeholder': _('MM')}, validators=validator_month)
    begin_day_from = IntegerField(render_kw={'placeholder': _('DD')}, validators=validator_day)
    begin_year_to = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    begin_month_to = IntegerField(render_kw={'placeholder': _('MM')}, validators=validator_month)
    begin_day_to = IntegerField(render_kw={'placeholder': _('DD')}, validators=validator_day)
    begin_comment = StringField(render_kw={'placeholder': _('comment')})
    end_year_from = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    end_month_from = IntegerField(render_kw={'placeholder': _('MM')}, validators=validator_month)
    end_day_from = IntegerField(render_kw={'placeholder': _('DD')}, validators=validator_day)
    end_year_to = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    end_month_to = IntegerField(render_kw={'placeholder': _('MM')}, validators=validator_month)
    end_day_to = IntegerField(render_kw={'placeholder': _('DD')}, validators=validator_day)
    end_comment = StringField(render_kw={'placeholder': _('comment')})

    @staticmethod
    def format_date(date: numpy.datetime64, part: str) -> str:
        string = str(date).split(' ')[0]
        bc = False
        if string.startswith('-') or string.startswith('0000'):
            bc = True
            string = string[1:]
        parts = string.split('-')
        if part == 'year':  # If it's a negative year, add one year
            return '-' + str(int(parts[0]) + 1) if bc else str(int(parts[0]))
        if part == 'month':
            return parts[1]
        return parts[2]

    def populate_dates(self, item) -> None:
        """ Populates date form fields with date values of an entity or link."""
        if item.begin_from:
            self.begin_year_from.data = DateForm.format_date(item.begin_from, 'year')
            self.begin_month_from.data = DateForm.format_date(item.begin_from, 'month')
            self.begin_day_from.data = DateForm.format_date(item.begin_from, 'day')
            self.begin_comment.data = item.begin_comment
            if item.begin_to:
                self.begin_year_to.data = DateForm.format_date(item.begin_to, 'year')
                self.begin_month_to.data = DateForm.format_date(item.begin_to, 'month')
                self.begin_day_to.data = DateForm.format_date(item.begin_to, 'day')
        if item.end_from:
            self.end_year_from.data = DateForm.format_date(item.end_from, 'year')
            self.end_month_from.data = DateForm.format_date(item.end_from, 'month')
            self.end_day_from.data = DateForm.format_date(item.end_from, 'day')
            self.end_comment.data = item.end_comment
            if item.end_to:
                self.end_year_to.data = DateForm.format_date(item.end_to, 'year')
                self.end_month_to.data = DateForm.format_date(item.end_to, 'month')
                self.end_day_to.data = DateForm.format_date(item.end_to, 'day')

    def validate(self) -> bool:
        valid = FlaskForm.validate(self)

        # Check date format, if valid put dates into a list called "dates"
        dates = {}
        for prefix in ['begin_', 'end_']:
            for postfix in ['_from', '_to']:
                if getattr(self, prefix + 'year' + postfix).data:
                    date = DateMapper.form_to_datetime64(
                        getattr(self, prefix + 'year' + postfix).data,
                        getattr(self, prefix + 'month' + postfix).data,
                        getattr(self, prefix + 'day' + postfix).data)
                    if not date:
                        getattr(self, prefix + 'day' + postfix).errors.append(_('not a valid date'))
                        valid = False
                    else:
                        dates[prefix + postfix.replace('_', '')] = date

        # Check for valid date combination e.g. begin not after end
        if valid:
            for prefix in ['begin', 'end']:
                if prefix + '_from' in dates and prefix + '_to' in dates:
                    if dates[prefix + '_from'] > dates[prefix + '_to']:
                        field = getattr(self,  prefix + '_day_from')
                        field.errors.append(_('First date cannot be after second.'))
                        valid = False
        if valid and 'begin_from' in dates and 'end_from' in dates:
            field = getattr(self, 'begin_day_from')
            if len(dates) == 4:  # All dates are used
                if dates['begin_from'] > dates['end_from'] or dates['begin_to'] > dates['end_to']:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False
            else:
                first = dates['begin_to'] if 'begin_to' in dates else dates['begin_from']
                second = dates['end_from'] if 'end_from' in dates else dates['end_to']
                if first > second:
                    field.errors.append(_('Begin dates cannot start after end dates.'))
                    valid = False
        return valid
