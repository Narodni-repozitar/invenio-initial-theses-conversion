from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from invenio_initial_theses_conversion.rules.model import old_nusl


@old_nusl.over("keywords", '^653')
@append_results
@list_value
@handled_values('a')
def keyword(self, key, value):
    """Subject."""
    if key == '653__':
        name = value.get("a")
        return {
            "name": name,
            "lang": "cze"
        }

    if key == '6530_':
        name = value.get("a")
        return {
            "name": name,
            "lang": "eng"
        }