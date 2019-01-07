# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import render_template, request
from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import BooleanField, SelectMultipleField, StringField, SubmitField, widgets
from wtforms.validators import InputRequired

from openatlas import app
from openatlas.models.entity import EntityMapper
from openatlas.util.util import link, required_group, truncate_string, uc_first


class SearchForm(Form):
    term = StringField(_('search'), [InputRequired()],
                       render_kw={'placeholder': uc_first(_('search term')), 'autofocus': True})
    own = BooleanField(_('Only entities edited by me'))
    desc = BooleanField(_('Also search in description'))
    classes = SelectMultipleField(_('classes'), [InputRequired()], choices=(),
                                  option_widget=widgets.CheckboxInput(),
                                  widget=widgets.ListWidget(prefix_label=False))
    search = SubmitField(_('search'))


@app.route('/overview/search', methods=['POST', 'GET'])
@required_group('readonly')
def search_index():
    choices = ['source', 'event', 'actor', 'place', 'reference', 'file']
    form = SearchForm()
    form.classes.choices = [(x, uc_first(_(x))) for x in choices]
    form.classes.default = choices
    form.classes.process(request.form)
    table = {'data': []}
    if request.method == 'POST' and 'global-term' in request.form and request.form['global-term']:
        # Coming from global search
        form.term.data = request.form['global-term']
        form.classes.data = choices
        table = build_search_table(form)
    if form.validate_on_submit():
        table = build_search_table(form)
    return render_template('search/index.html', form=form, table=table)


def build_search_table(form):
    table = {'id': 'search', 'data': [],
             'header': ['name', 'class', 'first', 'last', 'description']}
    for entity in EntityMapper.search(form):
        table['data'].append([link(entity), entity.class_.name, entity.first, entity.last,
                              truncate_string(entity.description)])
    return table
