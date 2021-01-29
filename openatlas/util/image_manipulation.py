from io import BytesIO

from PIL import Image


class ImageManipulation:

    @staticmethod
    def image_thumbnail(path: str, thumb_size: int) -> BytesIO:
        img_io = BytesIO()
        img = Image.open(path)
        img.thumbnail((thumb_size, thumb_size))
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io
