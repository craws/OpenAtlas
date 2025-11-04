from pathlib import Path

from flask import g
from wand.image import Image

from openatlas import app
from openatlas.models.entity import Entity


def resize_image(filename: str) -> None:
    file_format = '.' + filename.split('.', 1)[1].lower()
    if file_format in g.display_file_ext:
        for size in app.config['IMAGE_SIZE'].values():
            safe_resize_image(
                filename.rsplit('.', 1)[0].lower(),
                file_format, size)


def safe_resize_image(name: str, file_format: str, size: str) -> bool:
    try:
        if check_if_folder_exist(size, app.config['RESIZED_IMAGES']):
            return image_resizing(name, file_format, size)
        return False  # pragma: no cover
    except OSError as e:  # pragma: no cover
        g.logger.log(
            'info',
            'image processing',
            'failed to save resized image',
            e)
        return False


def image_resizing(name: str, format_: str, size: str) -> bool:
    filename = Path(app.config['UPLOAD_PATH']) / f"{name}{format_}[0]"
    with Image(filename=filename) as src:
        if format_ in app.config['PROCESSABLE_EXT']:
            format_ = app.config['PROCESSED_EXT']  # pragma: no cover
        with src.convert(format_.replace('.', '')) as img:
            img.transform(resize=f"{size}x{size}>")
            img.compression_quality = 75
            img.save(
                filename=Path(
                    app.config['RESIZED_IMAGES']) / size / f"{name}{format_}")
            return True


def check_processed_image(filename: str) -> bool:
    file_format = '.' + filename.split('.', 1)[1].lower()
    check = False
    try:
        if file_format in g.display_file_ext:
            check = loop_through_processed_folders(
                filename.rsplit('.', 1)[0].lower(),
                file_format)
    except OSError as e:  # pragma: no cover
        g.logger.log(
            'info',
            'image processing',
            'failed to validate file as image',
            e)
    return check


def loop_through_processed_folders(name: str, file_format: str) -> bool:
    ext = file_format
    if file_format in app.config['PROCESSABLE_EXT']:
        ext = app.config['PROCESSED_EXT']  # pragma: no cover
    for size in app.config['IMAGE_SIZE'].values():
        path = Path(app.config['RESIZED_IMAGES']) / size / f"{name}{ext}"
        if not path.is_file() \
                and not safe_resize_image(name, file_format, size):
            return False  # pragma: no cover
    return True


def check_if_folder_exist(folder: str, path: str) -> bool:
    folder_to_check = Path(path) / folder
    return True if folder_to_check.is_dir() else create_folder(folder_to_check)


def create_folder(folder: Path) -> bool:  # pragma: no cover
    try:
        folder.mkdir()
        return True
    except OSError as e:
        g.logger.log('info', 'image processing', 'failed to create folder', e)
        return False


def delete_orphaned_resized_images() -> None:
    for size in app.config['IMAGE_SIZE'].values():
        path = Path(app.config['RESIZED_IMAGES']) / size
        for file in path.glob('**/*'):
            file_name = file.name.rsplit('.', 1)[0].lower()
            if not file_name.isdigit() or int(file_name) not in g.files:
                file.unlink()  # pragma: no cover


def create_resized_images() -> None:
    for e in Entity.get_by_class('file'):
        if e.id in g.files and e.get_file_ext() in g.display_file_ext:
            resize_image(f"{e.id}{e.get_file_ext()}")
