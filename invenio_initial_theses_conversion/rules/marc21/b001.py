from dojson import utils

from ..model import old_nusl


@old_nusl.over('id', '^001')
def control_number(self, key, value):
    """Control Number."""
    return {
        "value": value
    }
