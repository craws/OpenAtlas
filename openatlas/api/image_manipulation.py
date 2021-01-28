from __future__ import print_function

from io import BytesIO
from wand.image import Image
from wand.display import display


class ImageManipulation:

    @staticmethod
    def image_thumbnail(path: str, thumb_size: int) -> BytesIO:
        with Image(filename=path) as img:
            with img.clone() as i:
                img_io = BytesIO()
                i.sample(int(thumb_size), int(thumb_size))
                i.rotate(180)
                i.save(file=img_io)
                #i.save(filename=path.format('1'))
        return i
        # img_io = BytesIO()
        # img = Image.open(path)
        # img.thumbnail((thumb_size, thumb_size))
        # img.save(img_io, 'JPEG')
        # img_io.seek(0)
        # return img_io
