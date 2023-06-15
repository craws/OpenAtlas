from typing import Optional

from flask import render_template, url_for, g, flash, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import BooleanField, SelectMultipleField, widgets, SelectField
from wtforms.validators import InputRequired

from openatlas.api.import_scripts.vocabs import (
    import_vocabs_data, get_vocabularies, fetch_vocabulary_details)
from openatlas.database.connect import Transaction
from openatlas import app
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import (
    button, display_info, is_authorized, required_group, display_form, link)
from openatlas.forms.field import SubmitField
from openatlas.forms.form import get_vocabs_form
from openatlas.models.settings import Settings
from openatlas.models.type import Type


@app.route('/vocabs')
@required_group('readonly')
def vocabs_index() -> str:
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            display_info({
                _('base url'): g.settings['vocabs_base_url'],
                _('endpoint'): g.settings['vocabs_endpoint'],
                _('user'): g.settings['vocabs_user']}),
            buttons=[
                button(_('edit'), url_for('vocabs_update'))
                if is_authorized('manager') else '',
                button(_('show vocabularies'), url_for('show_vocabularies'))
            ])},
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            'VOCABS'])


@app.route('/vocabs/update', methods=['GET', 'POST'])
@required_group('manager')
def vocabs_update() -> str:
    form = get_vocabs_form()
    if form.validate_on_submit():
        Settings.update({
            'vocabs_base_url': form.base_url.data,
            'vocabs_endpoint': form.endpoint.data,
            'vocabs_user': form.vocabs_user.data})
        flash(_('info update'), 'info')
        return redirect(url_for('vocabs_index'))
    if request.method != 'POST':
        form.base_url.data = g.settings['vocabs_base_url']
        form.endpoint.data = g.settings['vocabs_endpoint']
        form.vocabs_user.data = g.settings['vocabs_user']
    return render_template(
        'content.html',
        title='VOCABS',
        content=display_form(form),
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            _('edit')])


@app.route('/vocabs/vocabularies')
@required_group('manager')
def show_vocabularies() -> str:
    vocabularies = get_vocabularies()
    table = Table(
        header=[_('name'), 'ID', _('default language'), _('languages')])
    for entry in vocabularies:
        table.rows.append([
            link(entry['title'], entry['conceptUri'], external=True),
            entry['id'],
            entry['defaultLanguage'],
            ' '.join(entry['languages']),
            vocabulary_detail(
                url_for('vocabulary_import_view', id_=entry['id']))])
    tabs = {'vocabularies': Tab(_('vocabularies'), table=table)}
    return render_template(
        'tabs.html',
        tabs=tabs,
        title='VOCABS',
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            _('vocabularies')])


def vocabulary_detail(url: str) -> Optional[str]:
    return link(_('import'), url) if is_authorized('manager') else None


@app.route('/vocabs/import/<id_>', methods=['GET', 'POST'])
@required_group('manager')
def vocabulary_import_view(id_: str) -> str:

    details = fetch_vocabulary_details(id_)

    class ImportVocabsHierarchyForm(FlaskForm):
        multiple = BooleanField(
            _('multiple'),
            description=_('tooltip hierarchy multiple'))
        classes = SelectMultipleField(
                _('classes'),
                render_kw={'disabled': True},
                description=_('tooltip hierarchy forms'),
                choices=Type.get_class_choices(),
                option_widget=widgets.CheckboxInput(),
                widget=widgets.ListWidget(prefix_label=False))
        language = SelectField(
            _('language'),
            choices=[(lang, lang) for lang in details['languages']],
            default=details['defaultLanguage'])
        confirm_import = BooleanField(
            _("I'm sure to import this hierarchy"),
            default=False,
            validators=[InputRequired()])
        save = SubmitField(_('import hierarchy'))

    form = ImportVocabsHierarchyForm()

    if form.validate_on_submit() and form.confirm_import.data:
        form_data = {
            'classes': form.classes.data,
            'multiple': form.multiple.data,
            'language': form.language.data}
        try:
            count = import_vocabs_data(id_, form_data, details)
            Transaction.commit()
            g.logger.log('info', 'import', f'import: {count} top concepts')
            flash(f"{_('import of')}: {count} {_('top concepts')}", 'info')
        except Exception as e:
            print(e)
            Transaction.rollback()
            g.logger.log('error', 'import', 'import failed', e)
            flash(_('error transaction'), 'error')
        return redirect(f"{url_for('type_index')}#menu-tab-custom")
    return render_template(
        'tabs.html',
        tabs={'info': Tab(
            'info',
            _('You are about to import following hierarchy: ') +
            link(details['title'], details['conceptUri'], external=True),
            form=form)},
        title=id_,
        crumbs=[
            [_('admin'), f"{url_for('admin_index')}#tab-data"],
            ['VOCABS', f"{url_for('vocabs_index')}"],
            [_('vocabularies'), f"{url_for('show_vocabularies')}"],
            details['title']])
