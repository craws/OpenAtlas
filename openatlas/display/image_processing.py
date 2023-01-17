from pathlib import Path

from flask import g
from wand.image import Image

from openatlas import app


def resize_image(filename: str) -> None:
    file_format = '.' + filename.split('.', 1)[1].lower()
    if file_format in app.config['ALLOWED_IMAGE_EXT']:
        loop_resize_image(filename.rsplit('.', 1)[0].lower(), file_format)


def loop_resize_image(name: str, file_format: str) -> None:
    for size in app.config['IMAGE_SIZE'].values():
        safe_resize_image(name, file_format, size)


def safe_resize_image(name: str, file_format: str, size: str) -> bool:
    if check_if_folder_exist(size, app.config['RESIZED_IMAGES']):
        return image_resizing(name, file_format, size)
    return False


def image_resizing(name: str, format_: str, size: str) -> bool:
    conf = app.config
    filename = Path(conf['UPLOAD_DIR']) / f"{name}{format_}[0]"
    with Image(filename=filename) as src:
        ext = conf['PROCESSED_EXT'] \
            if format_ in conf['NONE_DISPLAY_EXT'] else format_
        with src.convert(ext.replace('.', '')) as img:
            img.transform(resize=f"{size}x{size}>")
            img.compression_quality = 75
            img.save(
                filename=Path(conf['RESIZED_IMAGES']) / size / f"{name}{ext}")
            return True


def check_processed_image(filename: str) -> bool:
    file_format = '.' + filename.split('.', 1)[1].lower()
    try:
        if file_format in app.config['ALLOWED_IMAGE_EXT']:
            return loop_through_processed_folders(
                filename.rsplit('.', 1)[0].lower(),
                file_format)
    except OSError as e:  # pragma: no cover
        g.logger.log(
            'info',
            'image processing',
            'failed to validate file as image',
            e)
    return False


def loop_through_processed_folders(name: str, file_format: str) -> bool:
    ext = app.config['PROCESSED_EXT'] \
        if file_format in app.config['NONE_DISPLAY_EXT'] else file_format
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
            if not file_name.isdigit() or int(file_name) not in g.file_stats:
                file.unlink()  # pragma: no cover


def create_resized_images() -> None:
    from openatlas.models.entity import Entity
    for entity in Entity.get_by_class('file'):
        if entity.id in g.file_stats \
                and g.file_stats[entity.id]['ext'] \
                in app.config['ALLOWED_IMAGE_EXT']:
            resize_image(f"{entity.id}{g.file_stats[entity.id]['ext']}")
