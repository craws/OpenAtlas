from io import BytesIO
from typing import Any, Dict

from PIL import Image


class ImageManipulation:

    @staticmethod
    def handle_image(path: str, parser: Dict[str, str]) -> BytesIO:
        parser['thumbnail'] = False
        img_io = BytesIO()
        img = Image.open(path)
        if parser['thumbnail']:
            img.thumbnail((200, 200))

        img.save(img_io, 'JPEG')
        img_io.seek(0)

        return img_io

