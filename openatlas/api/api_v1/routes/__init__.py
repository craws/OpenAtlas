from . import docs
from .system import api_v1_system
from .vocabulary import api_v1_vocabulary
from .lod import api_v1_lod
from .loud import api_v1_loud
from .root import api_v1_root
from .files import api_v1_files
from .metadata import api_v1_metadata

__all__ = [
    'api_v1_system',
    'api_v1_vocabulary',
    'api_v1_lod',
    'api_v1_loud',
    'api_v1_root',
    'api_v1_metadata',
    'api_v1_files']
