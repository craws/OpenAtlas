from subprocess import call
from typing import Any

from flask import g
from werkzeug.utils import secure_filename

from openatlas import app
from openatlas.display.image_processing import resize_image
from openatlas.display.util import check_iiif_activation, convert_image_to_iiif
from openatlas.models.dates import Dates, form_to_datetime64
from openatlas.models.entity import Entity


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
    from openatlas.forms.entity_form import process_form_data
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
