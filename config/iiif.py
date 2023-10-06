from config.default import ALLOWED_IMAGE_EXT

IIIF = {
    'activate': False,
    'path': '',
    'url': '',
    'version': 2,
    'conversion': True,
    'compression': 'deflate'  # 'deflate' or 'jpeg'
}

IIIF_IMAGE_EXT = ALLOWED_IMAGE_EXT + ['.pdf']