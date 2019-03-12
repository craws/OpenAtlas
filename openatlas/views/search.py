# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (BooleanField, IntegerField, SelectMultipleField, StringField, SubmitField,
                     widgets)
from wtforms.validators import InputRequired, NoneOf, NumberRange, Optional

from openatlas import app
from openatlas.models.date import DateMapper
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, required_group, truncate_string, uc_first


class SearchForm(Form):
    term = StringField(_('search'), [InputRequired()],
                       render_kw={'placeholder': _('search term'), 'autofocus': True})
    own = BooleanField(_('Only entities edited by me'))
    desc = BooleanField(_('Also search in description'))
    classes = SelectMultipleField(_('classes'), [InputRequired()], choices=(),
                                  option_widget=widgets.CheckboxInput(),
                                  widget=widgets.ListWidget(prefix_label=False))
    search = SubmitField(_('search'))

    # Date fields
    validator_day = [Optional(), NumberRange(min=1, max=31)]
    validator_month = [Optional(), NumberRange(min=1, max=12)]
    validator_year = [Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])]
    begin_year = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    begin_month = IntegerField(render_kw={'placeholder': 1}, validators=validator_month)
    begin_day = IntegerField(render_kw={'placeholder': 1}, validators=validator_day)
    end_year = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    end_month = IntegerField(render_kw={'placeholder': 12}, validators=validator_month)
    end_day = IntegerField(render_kw={'placeholder': 31}, validators=validator_day)
    include_dateless = BooleanField(_('Include dateless entities'))

    def validate(self, extra_validators=None):
        valid = Form.validate(self)
        from_date = None
        to_date = None
        if self.begin_year.data:
            if not self.end_month.data or not self.end_day.data:
                self.end_month.data = 1
                self.end_day.data = 1
            from_date = DateMapper.form_to_datetime64(self.begin_year.data, self.begin_month.data,
                                                      self.begin_day.data)
        if self.end_year.data:
            if not self.end_month.data or not self.end_day.data:
                self.end_month.data = 12
                self.end_day.data = 31
            to_date = DateMapper.form_to_datetime64(self.end_year.data, self.end_month.data,
                                                    self.end_day.data)
        if from_date and to_date and from_date > to_date:
            self.begin_year.errors.append(_('Begin dates cannot start after end dates.'))
            valid = False
        return valid


@app.route('/overview/search', methods=['POST', 'GET'])
@required_group('readonly')
def search_index():
    choices = ['source', 'event', 'actor', 'place', 'feature', 'stratigraphic unit', 'find',
               'reference', 'file']
    form = SearchForm()
    form.classes.choices = [(x, uc_first(_(x))) for x in choices]
    form.classes.default = choices
    form.classes.process(request.form)
    table = {'data': []}
    if request.method == 'POST' and 'global-term' in request.form:
        # Coming from global search
        form.term.data = request.form['global-term']
        form.classes.data = choices
        table = build_search_table(form)
    elif form.validate_on_submit():
        table = build_search_table(form)
    return render_template('search/index.html', form=form, table=table)


def build_search_table(form):
    table = {'id': 'search', 'data': [], 'sort': 'sortList: [[0, 0]]',
             'header': ['name', 'class', 'first', 'last', 'description']}
    for entity in EntityMapper.search(form):
        table['data'].append([link(entity),
                              entity.class_.name,
                              entity.first,
                              entity.last,
                              truncate_string(entity.description)])
    return table
