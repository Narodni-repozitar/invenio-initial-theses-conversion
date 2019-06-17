from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl


@old_nusl.over('id', '^001')
@single_value
def control_number(self, key, value):
    """Control Number."""
    assert isinstance(value, str)
    return value
