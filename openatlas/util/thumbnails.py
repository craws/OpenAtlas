from wand.image import Image

from openatlas import app


class Thumbnails:
    multi_image = ['pdf', 'mp4', 'gif', 'psd', 'ai', 'xcf']
    single_image = ['jpeg', 'jpg', 'png', 'tiff', 'tif', 'raw', 'eps']

    @staticmethod
    def upload_to_thumbnail(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = filename.rsplit('.', 1)[1].lower()
        if file_format in Thumbnails.single_image + Thumbnails.multi_image:
            sizes = ['400x400>']
            for size in sizes:
                Thumbnails.safe_as_thumbnail(name, file_format, size)

    @staticmethod
    def safe_as_thumbnail(filename: str, file_format: str, size: str) -> None:
        path = str(app.config['UPLOAD_DIR']) + '/' + filename + '.' + file_format
        if file_format in Thumbnails.multi_image:
            path += '[0]'
        with Image(filename=path) as src:
            with src.convert('png') as img:
                # https://docs.wand-py.org/en/0.6.6/guide/resizecrop.html?highlight=down%20scale#transform-images
                img.transform(resize=size)
                # img.compression_quality = 75
                img.save(
                    filename=str(app.config['UPLOAD_DIR']) + '/thumbnails/' + filename + '.png')

