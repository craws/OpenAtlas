from pathlib import Path

from wand.image import Image

from openatlas import app


class ImageProcessing:
    multi_image = ['pdf', 'mp4', 'gif', 'psd', 'ai', 'xcf']
    single_image = ['jpeg', 'jpg', 'png', 'tiff', 'tif', 'raw', 'eps', 'ico', 'svg', 'bmp']
    image_validation = single_image + multi_image

    @staticmethod
    def resize_image(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = filename.rsplit('.', 1)[1].lower()
        if file_format in ImageProcessing.image_validation:
            for size in app.config['PROCESSED_IMAGE_SIZES']:
                ImageProcessing.create_thumbnail(name, file_format, size)

    @staticmethod
    def create_thumbnail(filename: str, file_format: str, size: str) -> None:
        try:
            ImageProcessing.validate_folder(size, app.config['THUMBNAIL_DIR'])
        except Exception:
            print("Problem with folder checking or creation")
        path = str(Path(app.config['UPLOAD_DIR']) / f"{filename}.{file_format}")
        if file_format in ImageProcessing.multi_image:
            path += '[0]'
        with Image(filename=path) as src:
            with src.convert('png') as img:
                img.transform(resize=size + 'x' + size + '>')
                img.save(
                    filename=str(Path(app.config['THUMBNAIL_DIR']) / size / (filename + '.png')))

    @staticmethod
    def check_if_thumbnail_exist(image_id: int) -> None:
        return True

    @staticmethod
    def validate_folder(folder: str, path: str) -> bool:
        folder_to_check = Path(path) / folder
        if folder_to_check.is_dir():
            return True
        if folder_to_check.mkdir():
            return True
        return False

    @staticmethod
    def display_as_thumbnail(filename: str, size: str) -> None:
        path = str(app.config['UPLOAD_DIR']) + '/' + filename
        with Image(filename=path) as img:
            img.transform(resize=size + 'x' + size + '>')
            img.save(filename=f"{app.config['TMP_DIR']}/{filename}")
