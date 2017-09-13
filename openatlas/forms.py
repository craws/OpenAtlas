# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import NumberRange, Optional

from openatlas.util.util import uc_first


class DateForm(Form):

    def populate_dates(self, entity):
        for code, types in entity.dates.items():
            if code in ['OA1', 'OA3', 'OA5']:
                for type_, date in types.items():
                    if type_ in ['Exact date value', 'From date value']:
                        self.date_begin_year.data = date['timestamp'].year
                        self.date_begin_month.data = date['timestamp'].month
                        self.date_begin_day.data = date['timestamp'].day
                        self.date_begin_info.data = date['info']
                    else:
                        self.date_begin_year2.data = date['timestamp'].year
                        self.date_begin_month2.data = date['timestamp'].month
                        self.date_begin_day2.data = date['timestamp'].day
            else:
                for type_, date in types.items():
                    if type_ in ['Exact date value', 'From date value']:
                        self.date_end_year.data = date['timestamp'].year
                        self.date_end_month.data = date['timestamp'].month
                        self.date_end_day.data = date['timestamp'].day
                        self.date_end_info.data = date['info']
                    else:
                        self.date_end_year2.data = date['timestamp'].year
                        self.date_end_month2.data = date['timestamp'].month
                        self.date_end_day2.data = date['timestamp'].day

    date_begin_year = IntegerField(
        uc_first(_('begin')),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_begin_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_begin_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_begin_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_begin_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_begin_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_begin_info = StringField(render_kw={'placeholder': _('comment')},)
    date_end_year = IntegerField(
        uc_first(_('end')),
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_end_month = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_end_day = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_end_year2 = IntegerField(
        render_kw={'placeholder': _('yyyy')},
        validators=[Optional(), NumberRange(min=-4713)]
    )
    date_end_month2 = IntegerField(
        render_kw={'placeholder': _('mm')},
        validators=[Optional(), NumberRange(min=1, max=12)]
    )
    date_end_day2 = IntegerField(
        render_kw={'placeholder': _('dd')},
        validators=[Optional(), NumberRange(min=1, max=31)]
    )
    date_end_info = StringField(render_kw={'placeholder': _('comment')})


