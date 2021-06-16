from pathlib import Path

from wand.image import Image

from openatlas import app, logger


class ImageProcessing:

    @staticmethod
    def resize_image(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = '.' + filename.split('.', 1)[1].lower()
        if file_format in app.config['ALLOWED_IMAGE_EXT']:
            ImageProcessing.loop_resize_image(name, file_format)

    @staticmethod
    def loop_resize_image(name: str, file_format: str) -> None:
        for size in app.config['IMAGE_SIZE'].values():
            ImageProcessing.safe_resize_image(name, file_format, size)

    @staticmethod
    def safe_resize_image(name: str, file_format: str, size: str) -> bool:
        # With python3-wand 0.6. Path seems to work and str conversation can be removed
        try:
            if ImageProcessing.check_if_folder_exist(size, app.config['RESIZED_IMAGES']):
                ImageProcessing.image_resizing(name, file_format, size)
            return False  # pragma: no cover
        except Exception as e:
            logger.log('info', 'image processing', 'failed to save resized image', e)
            return False

    @staticmethod
    def image_resizing(name: str, file_format: str, size: str) -> bool:
        with Image(filename=str(Path(app.config['UPLOAD_DIR']) / f"{name}{file_format}[0]")) as src:
            extension = app.config['PROCESSED_EXT'] \
                if file_format in app.config['NONE_DISPLAY_EXT'] else file_format
            with src.convert(extension.replace('.', '')) as img:
                img.transform(resize=f"{size}x{size}>")
                img.compression_quality = 75
                img.save(filename=str(
                    Path(app.config['RESIZED_IMAGES'])
                    / size
                    / f"{name}{extension}"))
                return True

    @staticmethod
    def check_processed_image(filename: str) -> bool:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = '.' + filename.split('.', 1)[1].lower()
        try:
            if file_format in app.config['ALLOWED_IMAGE_EXT']:
                return ImageProcessing.loop_through_processed_folders(name, file_format)
            return False
        except Exception as e:  # pragma: no cover
            logger.log('info', 'image processing', 'failed to validate file as image', e)
            return False

    @staticmethod
    def loop_through_processed_folders(name: str, file_format: str) -> bool:
        format = app.config['PROCESSED_EXT'] \
            if file_format in app.config['NONE_DISPLAY_EXT'] else file_format
        for size in app.config['IMAGE_SIZE'].values():
            p = Path(app.config['RESIZED_IMAGES']) / size / f"{name}{format}"
            if not p.is_file() and not ImageProcessing.safe_resize_image(name, file_format, size):
                return False  # pragma: no cover
        return True

    @staticmethod
    def check_if_folder_exist(folder: str, path: str) -> bool:
        folder_to_check = Path(path) / folder
        return True if folder_to_check.is_dir() else ImageProcessing.create_folder(folder_to_check)

    @staticmethod
    def create_folder(folder: Path) -> bool:
        try:
            folder.mkdir()
            return True
        except Exception as e:  # pragma: no cover
            logger.log('info', 'image processing', 'failed to create a folder', e)
            return False

    # Todo: implement admin interface
    @staticmethod
    def search_and_delete_orphaned_images() -> None:
        uploaded_files = []
        for uploaded in app.config['UPLOAD_DIR'].glob('**/*'):
            uploaded_files.append(uploaded.name.rsplit('.', 1)[0].lower())
        for size in app.config['IMAGE_SIZE'].values():
            p = Path(app.config['RESIZED_IMAGES']) / size
            for file in p.glob('**/*'):
                if file.name.rsplit('.', 1)[1].lower() not in app.config['PROCESSED_EXT']:
                    file.unlink()
                if file.name.rsplit('.', 1)[0].lower() not in uploaded_files:
                    file.unlink()

    # Todo: implement admin interface
    @staticmethod
    def create_resized_images() -> None:
        for file in app.config['UPLOAD_DIR'].glob('**/*'):
            ImageProcessing.resize_image(file.name)
