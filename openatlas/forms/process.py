import ast
from typing import Any

from flask import g

from openatlas.display.util2 import sanitize
from openatlas.models.dates import Dates, form_to_datetime64
from openatlas.models.entity import Entity
from openatlas.models.reference_system import ReferenceSystem


def process_standard_fields(manager: Any) -> None:
    for key, value in manager.form.data.items():
        field_type = getattr(manager.form, key).type
        if field_type in [
                'TreeField',
                'TreeMultiField',
                'TableField',
                'TableMultiField']:
            if value:
                ids = ast.literal_eval(value)
                value = ids if isinstance(ids, list) else [int(ids)]
            else:
                value = []
        if key == 'name':
            name = manager.form.data['name']
            if hasattr(manager.form, 'name_inverse'):
                name = manager.form.name.data.replace(
                    '(', '').replace(')', '').strip()
                if manager.form.name_inverse.data.strip():
                    inverse = manager.form.name_inverse.data. \
                        replace('(', ''). \
                        replace(')', '').strip()
                    name += f' ({inverse})'
            if isinstance(manager.entity, ReferenceSystem) \
                    and manager.entity.system:
                name = manager.entity.name  # Prevent changing a system name
            manager.data['attributes']['name'] = name
        elif field_type == 'ValueTypeField':
            if value is not None:  # Allow the number zero
                manager.add_link('P2', g.types[int(key)], value)
        elif key == 'public':
            manager.data['file_info'] = {
                'public': bool(manager.form.public.data),
                'creator': sanitize(manager.form.creator.data),
                'license_holder': sanitize(manager.form.license_holder.data)}


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

# Todo: This will be where Bernhard and Alex will start again next time
def process_files(entity: Entity, form: Any) -> str:
    pass
#     filenames = []
#     try:
#         # Transaction.begin()
#         entity_name = form.name.data.strip()
#         for count, file in enumerate(form.file.data):
#             entity = insert('file', file.filename)
#             # Add 'a' to prevent emtpy temporary filename, has no side effects
#             filename = secure_filename(f'a{file.filename}')
#             name = f"{manager.entity.id}.{filename.rsplit('.', 1)[1].lower()}"
#             ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
#             path = app.config['UPLOAD_PATH'] / name
#             file.save(str(path))
#             if f'.{ext}' in g.display_file_ext:
#                 call(f'exiftran -ai {path}', shell=True)  # Fix rotation
#             filenames.append(name)
#             if g.settings['image_processing']:
#                 resize_image(name)
#             if (g.settings['iiif_conversion']
#                     and check_iiif_activation()
#                     and g.settings['iiif_convert_on_upload']):
#                 convert_image_to_iiif(manager.entity.id, path)
#             if len(manager.form.file.data) > 1:
#                 manager.form.name.data = \
#                     f'{entity_name}_{str(count + 1).zfill(2)}'
#             manager.process_form()
#             manager.update_entity()
#             g.logger.log_user(manager.entity.id, 'insert')
#         # Transaction.commit()
#         url = redirect_url_insert(manager)
#         flash(_('entity created'), 'info')
#     except Exception as e:  # pragma: no cover
#         # Transaction.rollback()
#         for filename in filenames:
#             (app.config['UPLOAD_PATH'] / filename).unlink()
#         g.logger.log('error', 'database', 'transaction failed', e)
#         flash(_('error transaction'), 'error')
#         url = url_for('index', group=g.classes['file'].group['name'])
#     return url
