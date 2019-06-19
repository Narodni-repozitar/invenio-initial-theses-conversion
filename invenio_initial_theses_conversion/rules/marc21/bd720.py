from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("creator", '720')
@list_value
@handled_values('a', 'i', 'e')
def creator(self, key, value):
    """Creator."""
    # print(value)
    if not value.get("i"):
        return {
            "name": value.get("a"),
            "id": {
                "value": None,
                "type": None
            }
        }

@old_nusl.over("contributor", '720')
@list_value
@handled_values('a', 'i', 'e')
def contributor(self, key, value):
    """Contributor"""
    print(value)
    if value.get("i"):
        return {
            "name": value.get("i"),
            "role": value.get("e"),
            "id": {
                "value": None,
                "type": None
            }
        }

