from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl
from re import match


@old_nusl.over('dateAccepted', '^046')
@single_value
@handled_values('k')
def control_number(self, key, value):
    """dateAccepted"""
    date = value.get("k")
    if match(f'\d\d\d\d-\d\d-\d\d', date) is not None:
        return date
    elif match(f'\d\d\d\d-\d\d', date) is not None:
        return f"{date}-01"
    else:
        return f"{date[0:4]}-01-01"
