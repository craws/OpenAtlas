from subprocess import call
from typing import Any, Optional

from flask import g, request
from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import (
    BooleanField, HiddenField, SelectMultipleField, StringField, widgets)

from openatlas import app
from openatlas.database.connect import Transaction
from openatlas.display.image_processing import resize_image
from openatlas.display.util import check_iiif_activation, convert_image_to_iiif
from openatlas.display.util2 import uc_first
from openatlas.forms.add_fields import (
    add_buttons, add_class_types, add_date_fields, add_description,
    add_name_fields, add_reference_systems, add_relations, get_validators)
from openatlas.forms.field import DragNDropField
from openatlas.forms.populate import populate_insert, populate_update
from openatlas.forms.util import convert
from openatlas.forms.validation import file, validate
from openatlas.models.dates import Dates, form_to_datetime64
from openatlas.models.entity import Entity, insert
from openatlas.models.gis import InvalidGeomException
from openatlas.models.openatlas_class import get_reverse_relation


def get_entity_form(
        entity: Entity,
        origin: Optional[Entity] = None,
        relation: Optional[str] = None) -> Any:

    class Form(FlaskForm):
        opened = HiddenField()
        validate = validate

    add_name_fields(Form, entity)
    add_class_types(Form, entity.class_)
    add_relations(Form, entity, origin)
    add_reference_systems(Form, entity.class_)
    for key, value in entity.class_.attributes.items():
        match key:
            case 'creator' | 'example_id' | 'license_holder' | \
                 'resolver_url' | 'website_url':
                setattr(
                    Form,
                    key,
                    StringField(
                        value['label'],
                        validators=get_validators(value)))
            case 'dates':
                add_date_fields(Form, entity)
            case 'description':
                add_description(Form, entity, origin)
            case 'file':
                if not entity.id:
                    setattr(
                        Form,
                        'file',
                        DragNDropField(
                            value['label'],
                            validators=get_validators(value)))
                    setattr(Form, 'validate_file', file)
            case 'location':
                for shape in ['points', 'polygons', 'lines']:
                    setattr(Form, f'gis_{shape}', HiddenField(default='[]'))
            case 'public':
                setattr(
                    Form,
                    'public',
                    BooleanField(
                        value['label'],
                        validators=get_validators(value)))
            case 'reference_system_classes':
                if choices := get_reference_system_class_choices(entity):
                    setattr(
                        Form,
                        'reference_system_classes',
                        SelectMultipleField(
                            _('classes'),
                            choices=choices,  # type: ignore
                            option_widget=widgets.CheckboxInput(),
                            widget=widgets.ListWidget(prefix_label=False)))

    add_buttons(
        Form,
        entity,
        origin.class_.relations[relation] if origin and relation else {})
    form: Any = Form(obj=entity)
    if request.method == 'GET':
        if entity.id:
            populate_update(form, entity)
        else:
            populate_insert(form, entity, origin)
    return form


def get_reference_system_class_choices(entity: Entity) -> list[tuple]:
    choices = []
    for class_ in g.classes.values():
        if 'reference_system' in class_.extra \
                and class_.name not in entity.classes \
                and not (
                    entity.name == 'GeoNames'
                    and class_.name not in g.class_groups['place']['classes']):
            choices.append((
                class_.name,
                uc_first(g.classes[class_.name].label)))
    return choices


def process_form_data(
        entity: Entity,
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> Entity:
    data = {
        'name': entity.name,
        'openatlas_class_name': entity.class_.name,
        'description': entity.description,
        'begin_from': entity.dates.begin_from,
        'begin_to': entity.dates.begin_to,
        'begin_comment': entity.dates.begin_comment,
        'end_from': entity.dates.end_from,
        'end_to': entity.dates.end_to,
        'end_comment': entity.dates.end_comment}
    for attr in entity.class_.attributes:
        match attr:
            case 'dates':
                data.update(process_dates(form))
            case 'location':
                data['gis'] = {
                    shape: getattr(form, f'gis_{shape}s').data
                    for shape in ['point', 'line', 'polygon']}
            case 'name' if entity.system:
                pass  # Prevent name change of system entities
            case 'name' if hasattr(form, 'name_inverse'):
                data[attr] = form.name.data.replace('(', '') \
                    .replace(')', '').strip()
                if form.name_inverse.data.strip():
                    inverse = form.name_inverse.data \
                        .replace('(', '').replace(')', '').strip()
                    data[attr] += f' ({inverse})'
            case _ if hasattr(form, attr) and (
                    getattr(form, attr).data or getattr(form, attr).data == 0):
                value = getattr(form, attr).data
                data[attr] = value.strip() if isinstance(value, str) else value
            case _:
                data[attr] = None
    try:
        Transaction.begin()
        if entity.id:
            delete_links(entity)
            entity.update(data)
        else:
            entity = insert(data)
        if entity.class_.hierarchies:
            process_types(entity, form)
        process_relations(entity, form, origin, relation_name)
        process_reference_systems(entity, form)
        Transaction.commit()
    except InvalidGeomException as e:
        Transaction.rollback()
        g.logger.log('error', 'database', 'invalid geom', e)
        raise e from None
    except Exception as e:
        Transaction.rollback()
        g.logger.log('error', 'database', 'transaction failed', e)
        raise e from None
    return entity


def process_reference_systems(entity: Entity, form: Any):
    entity.delete_links('P67', ['reference_system'], inverse=True)
    for system in g.reference_systems.values():
        if entity.class_.name not in system.classes:
            continue
        data = getattr(form, f'reference_system_id_{system.id}').data
        if data['value']:
            entity.link(
                'P67',
                system,
                data['value'],
                inverse=True,
                type_id=data['precision'])


def process_types(entity: Entity, form: Any) -> None:
    for type_ in [g.types[id_] for id_ in entity.class_.hierarchies]:
        if data := convert(getattr(form, str(type_.id)).data):
            if type_.class_.name == 'administrative_unit':
                entity.location.link('P89', [g.types[id_] for id_ in data])
            else:
                entity.link('P2', [g.types[id_] for id_ in data])


def process_relations(
        entity: Entity,
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> None:
    for name, relation in entity.class_.relations.items():
        if relation['mode'] != 'direct':
            continue
        ids = convert(getattr(form, name).data)
        if entity.class_.group['name'] == 'type' \
                and relation['name'] == 'super' \
                and not ids:
            ids = [entity.root[0] if entity.root else origin.id]
        if hasattr(form, name) and ids:
            entities = Entity.get_by_ids(ids)
            if 'object_location' in relation['classes']:
                locations = []
                for place in entities:
                    locations.append(place.get_linked_entity_safe('P53'))
                entities = locations
            entity.link(
                relation['property'],
                entities,
                inverse=relation['inverse'])

    if origin and relation_name:
        origin_relation = origin.class_.relations[relation_name]
        if not origin.class_.relations[relation_name]['additional_fields']:
            reverse_relation = get_reverse_relation(
                origin.class_,
                origin_relation,
                entity.class_)
            if not reverse_relation or reverse_relation['mode'] != 'direct':
                origin.link(
                    origin_relation['property'],
                    entity,
                    inverse=origin_relation['inverse'])


def delete_links(entity: Entity) -> None:
    if entity.class_.hierarchies:
        entity.delete_links('P2', ['type'])
        if entity.location:
            entity.location.delete_links('P89', ['administrative_unit'])
    for relation in entity.class_.relations.values():
        if relation['mode'] == 'direct':
            entity.delete_links(
                relation['property'],
                relation['classes'],
                relation['inverse'])


def process_dates(form: Any) -> dict[str, Any]:
    dates = Dates({})
    if hasattr(form, 'begin_year_from') and form.begin_year_from.data:
        dates.begin_comment = form.begin_comment.data
        dates.begin_from = form_to_datetime64(
            form.begin_year_from.data,
            form.begin_month_from.data,
            form.begin_day_from.data,
            form.begin_hour_from.data if 'begin_hour_from' in form else None,
            form.begin_minute_from.data if 'begin_hour_from' in form else None,
            form.begin_second_from.data if 'begin_hour_from' in form else None)
        dates.begin_to = form_to_datetime64(
            form.begin_year_to.data or (
                form.begin_year_from.data if not
                form.begin_day_from.data else None),
            form.begin_month_to.data or (
                form.begin_month_from.data if not
                form.begin_day_from.data else None),
            form.begin_day_to.data,
            form.begin_hour_to.data if 'begin_hour_from' in form else None,
            form.begin_minute_to.data if 'begin_hour_from' in form else None,
            form.begin_second_to.data if 'begin_hour_from' in form else None,
            to_date=True)
    if hasattr(form, 'end_year_from') and form.end_year_from.data:
        dates.end_comment = form.end_comment.data
        dates.end_from = form_to_datetime64(
            form.end_year_from.data,
            form.end_month_from.data,
            form.end_day_from.data,
            form.end_hour_from.data if 'end_hour_from' in form else None,
            form.end_minute_from.data if 'end_hour_from' in form else None,
            form.end_second_from.data if 'end_hour_from' in form else None)
        dates.end_to = form_to_datetime64(
            form.end_year_to.data or
            (form.end_year_from.data if not form.end_day_from.data else None),
            form.end_month_to.data or
            (form.end_month_from.data if not form.end_day_from.data else None),
            form.end_day_to.data,
            form.end_hour_to.data if 'end_hour_from' in form else None,
            form.end_minute_to.data if 'end_hour_from' in form else None,
            form.end_second_to.data if 'end_hour_from' in form else None,
            to_date=True)
    return dates.to_timestamp()


def process_files(
        form: Any,
        origin: Entity | None,
        relation_name: str | None) -> Entity:
    filenames = []
    entity = None
    try:
        entity_name = form.name.data.strip()
        for count, file in enumerate(form.file.data):
            if len(form.file.data) > 1:
                form.name.data = f'{entity_name}_{str(count + 1).zfill(2)}'
            entity = process_form_data(
                Entity({'openatlas_class_name': 'file'}),
                form,
                origin,
                relation_name)

            # Add 'a' to prevent emtpy temporary filename, has no side effects
            filename = secure_filename(f'a{file.filename}')
            ext = filename.rsplit('.', 1)[1].lower()
            name = f"{entity.id}.{ext}"
            path = app.config['UPLOAD_PATH'] / name
            file.save(str(path))

            if f'.{ext}' in g.display_file_ext:
                call(f'exiftran -ai {path}', shell=True)  # Fix rotation
            filenames.append(name)
            if g.settings['image_processing']:
                resize_image(name)
            if g.settings['iiif_conversion'] \
                    and check_iiif_activation() \
                    and g.settings['iiif_convert_on_upload']:
                convert_image_to_iiif(entity.id, path)
    except Exception as e:
        g.logger.log('error', 'database', 'file upload failed', e)
        raise e from None
    return entity
