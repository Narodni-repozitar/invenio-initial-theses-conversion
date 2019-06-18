from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl
from re import match


@old_nusl.over('dateAccepted', '^046')
@single_value
@handled_values('k', 'j')
def date_accepted(self, key, value):
    """dateAccepted"""
    # j was decided not to be converted

    date = value.get("k")
    if not date:
        date = value.get("j", '')

    date = date.strip()
    if date.startswith('['):
        date = date[1:]
    if date.endswith(']'):
        date = date[:-1]
    date = date.strip()
    if match(r'\d\d\d\d-\d\d-\d\d', date) is not None:
        return date
    elif match(r'\d\d\d\d-\d\d', date) is not None:
        return f"{date}-01"
    elif match(r'\d\d\d\d', date) is not None:
        return f"{date[0:4]}-01-01"
    else:
        raise AttributeError(f'Wrong date format: {date}')