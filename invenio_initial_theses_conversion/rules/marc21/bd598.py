from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl


@old_nusl.over('note', '^598__')
@handled_values('a')
@single_value
def note(self, key, value):
    return value.get('a')