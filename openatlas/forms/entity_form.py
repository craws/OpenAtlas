import time
from collections import OrderedDict
from typing import Any, Optional

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import FieldList, HiddenField, StringField, TextAreaField
from wtforms.validators import InputRequired

from openatlas.display.util2 import is_authorized
from openatlas.forms.add_fields import add_value_type_fields
from openatlas.forms.field import (
    RemovableListField, SubmitAnnotationField, SubmitField, TableField,
    TableMultiField, TextAnnotationField, TreeField, TreeMultiField,
    ValueTypeRootField)
from openatlas.forms.util import convert
from openatlas.forms.validation import validate
from openatlas.models.entity import Entity, insert
from openatlas.models.openatlas_class import OpenatlasClass


def get_entity_form(entity: Entity, origin: Optional[Entity] = None) -> Any:
    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    add_name_fields(Form, entity)
    add_types(Form, entity.class_)
    add_relations(Form, entity, origin)
    add_description(Form, entity)
    add_buttons(Form, entity)
    form: Any = Form(obj=entity)
    if request.method == 'GET' and entity.id:
        populate_update(form, entity)
    # elif request.method == 'GET' and entity.id:
    #    populate_insert(form, entity, origin, date)
    return form


def add_name_fields(form: Any, entity: Entity) -> None:
    if 'name' in entity.class_.attributes:
        setattr(
            form,
            'name',
            StringField(
                _('name'),
                validators=[InputRequired()],
                render_kw={'autofocus': True}))
    if 'alias' in entity.class_.attributes:
        setattr(form, 'alias', FieldList(RemovableListField()))


def add_buttons(form: Any, entity: Entity) -> None:
    field = SubmitField
    if 'description' in entity.class_.attributes \
            and 'annotated' in entity.class_.attributes['description']:
        field = SubmitAnnotationField
    setattr(form, 'save', field(_('save') if entity.id else _('insert')))
    if not entity.id and entity.class_.display['form']['insert_and_continue']:
        setattr(form, 'insert_and_continue', field(_('insert and continue')))
        setattr(form, 'continue_', HiddenField())


def add_description(form: Any, entity: Entity) -> None:
    if 'description' not in entity.class_.attributes:
        return
    if 'annotated' not in entity.class_.attributes['description']:
        setattr(
            form,
            'description',
            TextAreaField(_('description'), render_kw={'rows': 8}))
        return
    text = ''
    linked_entities = []
    if entity.id:
        text = entity.get_annotated_text()
        for e in entity.get_linked_entities('P67'):
            linked_entities.append({'id': e.id, 'name': e.name})
    setattr(
            form,
            'annotation',
            TextAnnotationField(
                label=entity.class_.attributes['description']['label'],
                source_text=text,
                linked_entities=linked_entities))
    setattr(form, 'description', HiddenField())


def add_types(form: Any, class_: OpenatlasClass) -> None:
    if class_.hierarchies:
        types = OrderedDict({id_: g.types[id_] for id_ in class_.hierarchies})
        if class_.standard_type_id in types:
            types.move_to_end(class_.standard_type_id, last=False)
        for type_ in types.values():
            class AddDynamicType(FlaskForm):
                pass

            setattr(AddDynamicType, 'name-dynamic', StringField(_('name')))
            setattr(
                AddDynamicType,
                f'{type_.id}-dynamic',
                TreeField(str(type_.id), type_id=str(type_.id)))
            setattr(
                AddDynamicType,
                'description-dynamic',
                TextAreaField(_('description')))
            add_form = AddDynamicType() if is_authorized('editor') else None
            if add_form:
                getattr(add_form, f'{type_.id}-dynamic').label.text = 'super'
            validators = [InputRequired()] if type_.required else []
            if type_.category == 'value':
                setattr(
                    form,
                    str(type_.id),
                    ValueTypeRootField(type_.name, type_.id))
                add_value_type_fields(form, type_.subs)
            elif type_.multiple:
                setattr(
                    form,
                    str(type_.id),
                    TreeMultiField(str(type_.id), validators, form=add_form))
            else:
                setattr(
                    form,
                    str(type_.id),
                    TreeField(str(type_.id), validators, form=add_form))


def add_relations(form: Any, entity: Entity, origin: Entity | None) -> None:
    entities = {}  # Collect entities per class to prevent multiple fetching
    for name, relation in entity.class_.relations.items():
        if relation['mode'] != 'direct':
            continue
        validators = [InputRequired()] if relation['required'] else None
        items = []
        for class_ in relation['class']:
            if class_ not in entities:
                entities[class_] = Entity.get_by_class(class_, True)
            items += entities[class_]
        if relation['multiple']:
            selection: Any = []
            if entity.id:
                selection = entity.get_linked_entities(
                    relation['property'],
                    relation['class'],
                    inverse=relation['inverse'])
            elif origin and origin.class_.name in relation['class']:
                selection = [origin]
            setattr(
                form,
                name,
                TableMultiField(
                    items,
                    selection,
                    description=relation['tooltip'],
                    label=relation['label'],
                    validators=validators))
        else:
            selection = None
            if entity.id:
                selection = entity.get_linked_entity(
                    relation['property'],
                    relation['class'],
                    relation['inverse'])
            elif origin and origin.class_.name in relation['class']:
                selection = origin
            setattr(
                form,
                name,
                TableField(
                    items,
                    selection,
                    description=relation['description'],
                    validators=validators))


def process_form_data(entity: Entity, form: Any) -> Entity:
    data = {
        'name': entity.class_.name,
        'openatlas_class_name': entity.class_.name,
        'cidoc_class_code': entity.class_.cidoc_class.code,
        'description': entity.description,
        'begin_from': entity.begin_from,
        'begin_to': entity.begin_to,
        'begin_comment': entity.begin_comment,
        'end_from': entity.end_from,
        'end_to': entity.end_to,
        'end_comment': entity.end_comment}
    for attr in entity.class_.attributes:
        data[attr] = None
        if getattr(form, attr).data or getattr(form, attr).data == 0:
            value = getattr(form, attr).data
            data[attr] = value.strip() if isinstance(value, str) else value
    if entity.id:
        update_entity(entity, form, data)
    else:
        entity = insert_entity(form, data)
    process_relations(entity, form)
    return entity


def process_relations(entity: Entity, form: Any) -> None:
    for name, relation in entity.class_.relations.items():
        if relation['mode'] == 'tab':
            continue
        #if hasattr(form, name) and (ids := convert(getattr(form, name).data)):
        #    entity.link(relation['property'], ids, relation['inverse'])


def insert_entity(form: Any, data: dict[str, Any]) -> Entity:
    entity = insert(data)
    #if hasattr(form, 'file'):
    #    file = request.files['file']
    #    ext = secure_filename(str(file.filename)).rsplit('.', 1)[1].lower()
    #    path = app.config['UPLOAD_DIR'] / f'{entity.id}.{ext}'
    #    file.save(str(path))
    #    if f'.{ext}' in app.config['IMAGE_EXTENSIONS']:
    #        call(f'exiftran -ai {path}', shell=True)  # Fix rotation
    return entity


def update_entity(entity: Entity, form: Any, data: dict[str, Any]) -> None:
    delete_links: dict[str, Any] = {'property': [], 'property_inverse': []}
    for i in entity.class_.relations.values():
        if i['mode'] != 'tab':
            if i['inverse']:
                delete_links['property_inverse'].append(i['property'])
            else:
                delete_links['property'].append(i['property'])
    if delete_links['property_inverse']:
        entity.delete_links(delete_links['property_inverse'], True)
    if delete_links['property']:
        entity.delete_links(delete_links['property'])
    if entity.class_.name in ['place', 'type']:
        new_super = g.types[entity.root[0]]
        if data1 := getattr(form, new_super.name).data:
            new_super = g.types[int(convert(data1)[0])]
        entity.link('has super', new_super.id)
    entity.update(data)


def populate_update(form: Any, entity: Entity) -> None:
    form.opened.data = time.time()
