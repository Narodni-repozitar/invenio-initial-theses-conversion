from dojson import utils

from ..model import old_nusl


@old_nusl.over("lang", '04107')
def language_code(self, key, value):
    """Language Code."""

    return {
         "language": value.get('a')
    }
