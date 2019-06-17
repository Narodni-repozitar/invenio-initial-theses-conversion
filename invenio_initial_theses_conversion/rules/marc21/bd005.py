from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl
from re import match


@old_nusl.over('modified', '^005')
@single_value
def modified(self, key, value):
    """modified"""
    assert isinstance(value, str)
    date_time = f"{value[0:4]}-{value[4:6]}-{value[6:8]}T{value[8:10]}:{value[10:12]}:{value[12:14]}+00:00"
    return date_time
