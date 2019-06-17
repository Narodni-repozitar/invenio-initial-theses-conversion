from invenio_initial_theses_conversion.nusl_overdo import single_value
from ..model import old_nusl


@old_nusl.over('id', '^001')
@single_value
def control_number(self, key, value):
    """Control Number."""
    return {
        "value": value
    }
