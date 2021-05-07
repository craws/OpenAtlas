from pathlib import Path

from wand.image import Image

from openatlas import app, logger


class ImageProcessing:

    @staticmethod
    def resize_image(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = '.' + filename.split('.', 1)[1].lower()
        if file_format in app.config['PROCESSED_IMAGE_EXT']:
            for size in app.config['IMAGE_SIZE'].values():
                ImageProcessing.safe_resized_image(name, file_format, size)

    @staticmethod
    def safe_resized_image(name: str, file_format: str, size: str) -> None:
        try:
            ImageProcessing.check_if_folder_exist(size, app.config['RESIZED_IMAGES'])
            path = str(Path(app.config['UPLOAD_DIR']) / f"{name}{file_format}[0]")
            with Image(filename=path) as src:
                with src.convert('png') as img:
                    img.transform(resize=size + 'x' + size + '>')
                    img.save(
                        filename=str(Path(app.config['RESIZED_IMAGES']) / size / (name + '.png')))
        except Exception as e:
            logger.log('debug', 'image resizing', 'failed to save', e)

    @staticmethod
    def check_processed_image(filename: str) -> bool:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = '.' + filename.split('.', 1)[1].lower()
        try:
            if file_format in app.config['PROCESSED_IMAGE_EXT']:
                for size in app.config['IMAGE_SIZE'].values():
                    p = Path(app.config['RESIZED_IMAGES']) / size / f'{name}.png'
                    if not p.is_file():
                        ImageProcessing.safe_resized_image(name, file_format, size)
                return True
            return False
        except Exception as e:
            logger.log('debug', 'image validation failed', 'fail to validate file as image', e)
            return False

    @staticmethod
    def check_if_folder_exist(folder: str, path: str) -> bool:
        folder_to_check = Path(path) / folder
        return True if folder_to_check.is_dir() else ImageProcessing.create_folder(folder_to_check)

    @staticmethod
    def create_folder(folder: Path) -> bool:
        return True if folder.mkdir() else False

    @staticmethod
    def display_as_thumbnail(filename: str, size: str) -> None:
        path = str(app.config['UPLOAD_DIR']) + '/' + filename
        with Image(filename=path) as img:
            img.transform(resize=size + 'x' + size + '>')
            img.save(filename=f"{app.config['OA_TMP_DIR']}/{filename}")
