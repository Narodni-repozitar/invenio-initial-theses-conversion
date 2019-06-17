from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("title", '24500')
@list_value
@extra_argument('language', '04107', single=True)
@handled_values('a', 'b')
def title_value(self, key, value, language):
    """Language Code."""
    if "a" in value:
        return {
            "name": value.get('a'),
            "lang": language.get('a') if language else 'unk'
        }
    if "b" in value:
        return {
            "name": value.get('b'),
            "lang": "eng"
        }
