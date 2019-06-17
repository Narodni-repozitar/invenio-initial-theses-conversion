from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("abstract", '520')
@list_value
@handled_values('a', '9')
def abstract(self, key, value):
    """Language Code."""
    return {
        "name": value.get("a"),
        "lang": value.get("9")
    }
