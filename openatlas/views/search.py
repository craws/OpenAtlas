# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import (BooleanField, IntegerField, SelectMultipleField, StringField, SubmitField,
                     widgets)
from wtforms.validators import InputRequired, NoneOf, NumberRange, Optional

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, required_group, truncate_string, uc_first


class SearchForm(Form):
    validator_day = [Optional(), NumberRange(min=1, max=31)]
    validator_month = [Optional(), NumberRange(min=1, max=12)]
    validator_year = [Optional(), NumberRange(min=-4713, max=9999), NoneOf([0])]

    begin_year = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    begin_month = IntegerField(render_kw={'placeholder': _('1')}, validators=validator_month)
    begin_day = IntegerField(render_kw={'placeholder': _('1')}, validators=validator_day)
    end_year = IntegerField(render_kw={'placeholder': _('YYYY')}, validators=validator_year)
    end_month = IntegerField(render_kw={'placeholder': _('12')}, validators=validator_month)
    end_day = IntegerField(render_kw={'placeholder': _('31')}, validators=validator_day)

    term = StringField(_('search'), [InputRequired()],
                       render_kw={'placeholder': _('search term'), 'autofocus': True})
    own = BooleanField(_('Only entities edited by me'))
    desc = BooleanField(_('Also search in description'))
    classes = SelectMultipleField(_('classes'), [InputRequired()], choices=(),
                                  option_widget=widgets.CheckboxInput(),
                                  widget=widgets.ListWidget(prefix_label=False))
    search = SubmitField(_('search'))


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
        table['data'].append([link(entity), entity.class_.name, entity.first, entity.last,
                              truncate_string(entity.description)])
    return table
