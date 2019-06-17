from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl


@old_nusl.over('extent', '^300')
@single_value
@handled_values('a')
def extent(self, key, value):
    """Extent."""
    return value.get('a').strip()
