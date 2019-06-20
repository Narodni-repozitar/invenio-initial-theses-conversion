from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl


@old_nusl.over('defended', '^586__')
@handled_values('a', 'b')
@single_value
def defended(self, key, value):
    if value.get("a") == "obhájeno":
        return True
    if value.get("a") == "neobhájeno":
        return False