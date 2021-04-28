from pathlib import Path

from wand.image import Image

from openatlas import app


class ImageProcessing:
    multi_image = ['pdf', 'mp4', 'gif', 'psd', 'ai', 'xcf']
    single_image = ['jpeg', 'jpg', 'png', 'tiff', 'tif', 'raw', 'eps']

    @staticmethod
    def upload_to_thumbnail(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = filename.rsplit('.', 1)[1].lower()
        if file_format in ImageProcessing.single_image + ImageProcessing.multi_image:
            sizes = app.config['PROCESSED_IMAGE_SIZES']
            for size in sizes:
                ImageProcessing.safe_as_thumbnail(name, file_format, size)

    @staticmethod
    def safe_as_thumbnail(filename: str, file_format: str, size: str) -> None:
        path = str(Path(app.config['UPLOAD_DIR']) / f"{filename}.{file_format}")
        if file_format in ImageProcessing.multi_image:
            path += '[0]'
        with Image(filename=path) as src:
            with src.convert('png') as img:
                img.transform(resize=size + 'x' + size + '>')
                img.save(
                    filename=str(
                        Path(app.config['PROCESSED_IMAGE_DIR']) / 'thumbnails' / size / (filename + '.png')))

    @staticmethod
    def display_as_thumbnail(filename: str, size: str) -> None:
        path = str(app.config['UPLOAD_DIR']) + '/' + filename
        with Image(filename=path) as img:
            img.transform(resize=size + 'x' + size + '>')
            img.save(filename=f"{app.config['TMP_DIR']}/{filename}")
