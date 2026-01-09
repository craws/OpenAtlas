from typing import Any, Optional

from flask import flash, g, render_template, request, url_for
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from werkzeug.wrappers import Response
from wtforms import (
    BooleanField, SelectField, SelectMultipleField, StringField, widgets)
from wtforms.validators import InputRequired, URL

from openatlas import app
from openatlas.api.import_scripts.vocabs import (
    fetch_top_concept_details, fetch_top_group_details,
    fetch_vocabulary_details, get_vocabularies, import_vocabs_data)
from openatlas.display.tab import Tab
from openatlas.display.table import Table
from openatlas.display.util import button, display_info, link, required_group
from openatlas.display.util2 import is_authorized, manual
from openatlas.forms.display import display_form
from openatlas.forms.field import SubmitField
from openatlas.models.entity import Entity
from openatlas.models.settings import update_settings


@app.route('/vocabs')
@required_group('manager')
def vocabs_index() -> str:
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'info',
                content=display_info({
                    _('base URL'): g.settings['vocabs_base_url'],
                    _('endpoint'): g.settings['vocabs_endpoint'],
                    _('user'): g.settings['vocabs_user']}),
                buttons=[
                    manual('admin/vocabs'),
                    button(_('edit'), url_for('vocabs_update'))
                    if is_authorized('manager') else '',
                    button(
                        _('show vocabularies'),
                        url_for('show_vocabularies'))])},
        crumbs=[[_('admin'), f'{url_for('admin_index')}#tab-data'], 'VOCABS'])


def vocabs_form() -> Any:
    class Form(FlaskForm):
        base_url = StringField(
            _('base URL'),
            validators=[InputRequired(), URL()])
        endpoint = StringField(_('endpoint'), validators=[InputRequired()])
        vocabs_user = StringField(_('user'))
        save = SubmitField(_('save'))

    return Form()


@app.route('/vocabs/update', methods=['GET', 'POST'])
@required_group('manager')
def vocabs_update() -> str | Response:
    form = vocabs_form()
    if form.validate_on_submit():
        update_settings({
            'vocabs_base_url': form.base_url.data,
            'vocabs_endpoint': form.endpoint.data,
            'vocabs_user': form.vocabs_user.data})
        flash(_('info update'))
        return redirect(url_for('vocabs_index'))
    if request.method != 'POST':
        form.base_url.data = g.settings['vocabs_base_url']
        form.endpoint.data = g.settings['vocabs_endpoint']
        form.vocabs_user.data = g.settings['vocabs_user']
    return render_template(
        'content.html',
        title='VOCABS',
        buttons=[manual('admin/vocabs')],
        content=display_form(form),
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            ['VOCABS', url_for('vocabs_index')],
            _('edit')])


@app.route('/vocabs/vocabularies')
@required_group('manager')
def show_vocabularies() -> str:
    table = Table([
        _('name'),
        'ID',
        _('default language'),
        _('languages'),
        _('import'),
        _('import')])
    for entry in get_vocabularies():
        table.rows.append([
            link(entry['title'], entry['conceptUri'], external=True),
            entry['id'],
            entry['defaultLanguage'],
            ' '.join(entry['languages']),
            vocabulary_detail(
                'hierarchy',
                url_for(
                    'vocabulary_import_view',
                    category="hierarchy",
                    id_=entry['id'])),
            vocabulary_detail(
                'groups',
                url_for(
                    'vocabulary_import_view',
                    category="groups",
                    id_=entry['id']))])
    return render_template(
        'tabs.html',
        tabs={
            'vocabularies': Tab(
                _('vocabularies'),
                table=table,
                buttons=[manual('admin/vocabs')])},
        buttons=[manual('admin/vocabs')],
        title='VOCABS',
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            ['VOCABS', url_for('vocabs_index')],
            _('vocabularies')])


def vocabulary_detail(category: str, url: str) -> Optional[str]:
    return link(_(category), url) if is_authorized('manager') else None


@app.route('/vocabs/import/<category>/<id_>', methods=['GET', 'POST'])
@required_group('manager')
def vocabulary_import_view(category: str, id_: str) -> str | Response:
    details = fetch_vocabulary_details(id_)

    class ImportVocabsHierarchyForm(FlaskForm):
        # noinspection PyTypeChecker
        concepts = SelectMultipleField(
            _('top concepts') if category == 'hierarchy' else _('groups'),
            choices=fetch_top_concept_details(id_) if category == 'hierarchy'
            else fetch_top_group_details(id_),
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False))
        # noinspection PyTypeChecker
        classes = SelectMultipleField(
            _('classes'),
            description=_('tooltip hierarchy forms'),
            choices=Entity.get_class_choices(),
            option_widget=widgets.CheckboxInput(),
            widget=widgets.ListWidget(prefix_label=False))
        multiple = BooleanField(
            _('multiple'),
            description=_('tooltip hierarchy multiple'))
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
            'choices': form.concepts.choices,
            'top_concepts': form.concepts.data,
            'classes': form.classes.data,
            'multiple': form.multiple.data,
            'language': form.language.data}
        try:
            results = import_vocabs_data(id_, form_data, details, category)
            count = len(results[0])
            g.logger.log('info', 'import', f'import: {count} top concepts')
            import_str = f'{_('import of')}: {count} {_('top concepts')}'
            if results[1]:
                import_str += f'. {_("Check log for not imported concepts")}'
                for duplicate in results[1]:
                    g.logger.log(
                        'info',
                        'import',
                        f'Did not import "{duplicate}", duplicate.')
            flash(import_str)
        except Exception as e:  # pragma: no cover
            g.logger.log('error', 'import', 'import failed', e)
            flash(_('error transaction'), 'error')
        return redirect(f"{url_for('index', group='type')}#menu-tab-custom")
    return render_template(
        'tabs.html',
        tabs={
            'info': Tab(
                'info',
                content=_('You are about to import following hierarchy') +
                ': ' +
                link(details['title'], details['conceptUri'], external=True),
                form=form,
                buttons=[manual('admin/vocabs')])},
        title=id_,
        crumbs=[
            [_('admin'), f'{url_for('admin_index')}#tab-data'],
            ['VOCABS', url_for('vocabs_index')],
            [_('vocabularies'), url_for('show_vocabularies')],
            details['title']])
