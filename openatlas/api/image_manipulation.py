from __future__ import print_function

import tempfile
from io import BytesIO
from tempfile import NamedTemporaryFile

from wand.image import Image
from wand.display import display


class ImageManipulation:

    @staticmethod
    def image_thumbnail(path: str, thumb_size: int) -> BytesIO:
        with Image(filename=path) as src:
            with src.clone() as img:

                w, h = int(thumb_size), int(thumb_size),
                img.resize(w, h)
                tf = tempfile.NamedTemporaryFile()
                img.save(file=tf)

        return img


        # img_io = BytesIO()
        # img = Image.open(path)
        # img.thumbnail((thumb_size, thumb_size))
        # img.save(img_io, 'JPEG')
        # img_io.seek(0)
        # return img_io
