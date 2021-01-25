from io import BytesIO
from typing import Any, Dict

from PIL import Image


class ImageManipulation:

    @staticmethod
    def handle_image(path: str, parser: Dict[str, str]) -> BytesIO:
        thumb_size = parser['thumbnail']
        img_io = BytesIO()
        img = Image.open(path)
        if thumb_size:
            img.thumbnail((thumb_size, thumb_size))
        img.save(img_io, 'JPEG')
        img_io.seek(0)

        return img_io

