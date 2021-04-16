from wand.image import Image

from openatlas import app


class ImageManipulation:

    multi_image = ['pdf', 'mp4', 'gif', 'psd', 'ai', 'xcf']
    single_image = ['jpeg', 'jpg', 'png', 'tiff', 'tif', 'raw', 'eps']

    @staticmethod
    def upload_image(filename: str) -> None:
        name = filename.rsplit('.', 1)[0].lower()
        file_format = filename.rsplit('.', 1)[1].lower()
        if file_format in ImageManipulation.single_image + ImageManipulation.multi_image:
            ImageManipulation.safe_as_thumbnail(name, file_format)

    @staticmethod
    def safe_as_thumbnail(filename: str, file_format: str) -> None:
        path = str(app.config['UPLOAD_DIR']) + '/' + filename + '.' + file_format
        if file_format in ImageManipulation.multi_image:
            path += '[0]'
        with Image(filename=path) as src:
            with src.convert('png') as img:
                # https://docs.wand-py.org/en/0.6.6/guide/resizecrop.html?highlight=down%20scale#transform-images
                img.transform(resize='400x400>')
                #img.compression_quality = 75
                img.save(filename=str(app.config['UPLOAD_DIR']) + '/thumbnails/' + filename + '.png')


    # @staticmethod
    # def image_resize(filename: str, thumb_size: int) -> Image:
    #     path = str(app.config['UPLOAD_DIR']) + '/' + filename
    #     with Image(filename=path) as src:
    #         print(src.size)
    #         print(path)
    #         with src.clone() as img:
    #             size = str(thumb_size)
    #             # https://docs.wand-py.org/en/0.6.6/guide/resizecrop.html?highlight=down%20scale#transform-images
    #             img.transform(resize=size+'x'+size+'>')
    #             print(type(img))
    #             return img
    #
