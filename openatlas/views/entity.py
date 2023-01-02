from typing import Union

from flask import flash, g, render_template, request, url_for
from flask_babel import lazy_gettext as _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

from openatlas import app
from openatlas.display import display
from openatlas.forms.form import get_table_form
from openatlas.models.entity import Entity
from openatlas.util.util import display_form, required_group, uc_first
from openatlas.views.link import AddReferenceForm


@app.route('/entity/<int:id_>')
@required_group('readonly')
def view(id_: int) -> Union[str, Response]:
    if id_ in g.types:  # Types have their own view
        entity = g.types[id_]
        if not entity.root:
            return redirect(
                f"{url_for('type_index')}"
                f"#menu-tab-{entity.category}_collapse-{id_}")
    elif id_ in g.reference_systems:
        entity = g.reference_systems[id_]
    else:
        entity = Entity.get_by_id(id_, types=True, aliases=True)
        if not entity.class_.view:
            flash(_("This entity can't be viewed directly."), 'error')
            abort(400)
    class_name = \
        f"{''.join(i.capitalize() for i in entity.class_.name.split('_'))}"
    manager = getattr(display, f'{class_name}Display')(entity)
    return render_template(
        'tabs.html',
        tabs=manager.tabs,
        entity=entity,
        gis_data=manager.gis_data,
        crumbs=manager.crumbs)


@app.route('/entity/add/file/<int:id_>', methods=['GET', 'POST'])
@required_group('contributor')
def entity_add_file(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'], inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-file")
    return render_template(
        'content.html',
        content=get_table_form(
            'file',
            entity.get_linked_entities('P67', inverse=True)),
        entity=entity,
        title=entity.name,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('file')}"])


@app.route('/entity/add/source/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_source(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    if request.method == 'POST':
        if request.form['checkbox_values']:
            entity.link_string(
                'P67',
                request.form['checkbox_values'],
                inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-source")
    return render_template(
        'content.html',
        content=get_table_form(
            'source',
            entity.get_linked_entities('P67', inverse=True)),
        title=entity.name,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('source')}"])


@app.route('/entity/add/reference/<int:id_>', methods=['POST', 'GET'])
@required_group('contributor')
def entity_add_reference(id_: int) -> Union[str, Response]:
    entity = Entity.get_by_id(id_)
    form = AddReferenceForm()
    if form.validate_on_submit():
        entity.link_string(
            'P67',
            form.reference.data,
            description=form.page.data,
            inverse=True)
        return redirect(f"{url_for('view', id_=id_)}#tab-reference")
    form.page.label.text = uc_first(_('page / link text'))
    return render_template(
        'content.html',
        content=display_form(form),
        entity=entity,
        crumbs=[
            [_(entity.class_.view), url_for('index', view=entity.class_.view)],
            entity,
            f"{_('link')} {_('reference')}"])

