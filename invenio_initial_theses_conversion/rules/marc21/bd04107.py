from invenio_initial_theses_conversion.nusl_overdo import single_value, append_results, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("language", '^041')
@single_value
@handled_values('a', 'b')
def language(self, key, value):
    """Language Code."""
    print(value)
    languages = []
    if not value.get("a"):
        raise AttributeError("Subject name required (04107)")
    if "a" in value:
        languages.append(value.get("a"))
    if "b" in value:
        languages.append(value.get("b"))
    return languages
