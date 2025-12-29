from typing import Any

from flask import g, render_template, request
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, IntegerField, SelectMultipleField, StringField, widgets)
from wtforms.validators import InputRequired, NoneOf, NumberRange, Optional

from openatlas import app
from openatlas.display.table import Table, entity_table
from openatlas.display.util import required_group
from openatlas.display.util2 import uc_first
from openatlas.forms.field import SubmitField
from openatlas.models.dates import form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.search import search


class SearchForm(FlaskForm):
    term = StringField(
        'search',
        [InputRequired()],
        render_kw={'autofocus': True})
    own = BooleanField(_('Only entities edited by me'))
    desc = BooleanField(_('Also search in description'))
    # noinspection PyTypeChecker
    classes = SelectMultipleField(
        _('classes'),
        [InputRequired()],
        choices=(),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
    search = SubmitField(_('search'))
    validator_day = [Optional(), NumberRange(min=1, max=31)]
    validator_month = [Optional(), NumberRange(min=1, max=12)]
    validator_year = [
        Optional(),
        NumberRange(min=-4713, max=9999),
        NoneOf([0])]
    begin_year = IntegerField(
        render_kw={'placeholder': _('YYYY')},
        validators=validator_year)
    begin_month = IntegerField(
        render_kw={'placeholder': 1},
        validators=validator_month)
    begin_day = IntegerField(
        render_kw={'placeholder': 1},
        validators=validator_day)
    end_year = IntegerField(
        render_kw={'placeholder': _('YYYY')},
        validators=validator_year)
    end_month = IntegerField(
        render_kw={'placeholder': 12},
        validators=validator_month)
    end_day = IntegerField(
        render_kw={'placeholder': 31},
        validators=validator_day)
    include_dateless = BooleanField(_('Include dateless entities'))

    def validate(self, extra_validators: Any = None) -> bool:
        valid = FlaskForm.validate(self)
        from_date = form_to_datetime64(
            self.begin_year.data,
            self.begin_month.data,
            self.begin_day.data)
        to_date = form_to_datetime64(
            self.end_year.data,
            self.end_month.data,
            self.end_day.data,
            to_date=True)
        if from_date and to_date and from_date > to_date:
            self.begin_year.errors.append(  # type: ignore
                _('Begin dates cannot start after end dates.'))
            valid = False
        return valid


@app.route('/overview/search', methods=['GET', 'POST'])
@required_group('readonly')
def search_index() -> str:
    classes = [
        name for name, count in Entity.get_overview_counts().items()
        if count and g.classes[name].group]
    form = SearchForm()
    getattr(form, 'search').label.text = uc_first(_('search'))
    form.classes.choices = [(name, g.classes[name].label) for name in classes]
    form.classes.default = classes
    form.classes.process(request.form)
    table = Table()
    if request.method == 'POST' and 'global-term' in request.form:
        form.term.data = request.form['global-term']
        form.classes.data = classes
        table = results_table(form)
    elif form.validate_on_submit():
        table = results_table(form)
    return render_template(
        'search.html',
        form=form,
        table=table,
        title=_('search'),
        crumbs=[_('search')])


def results_table(form: Any) -> Table:
    entities = search({
        'term': form.term.data,
        'classes': form.classes.data,
        'desc': form.desc.data,
        'own': form.own.data,
        'include_dateless': form.include_dateless.data,
        'from_date': form_to_datetime64(
            form.begin_year.data,
            form.begin_month.data,
            form.begin_day.data),
        'to_date': form_to_datetime64(
            form.end_year.data,
            form.end_month.data,
            form.end_day.data,
            to_date=True)})
    return entity_table(
        entities,
        columns=['name', 'class', 'begin', 'end', 'description'])
