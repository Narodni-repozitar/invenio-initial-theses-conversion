from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("identifier", '^85640')
@list_value
def identifier(self, key, value):
    """Identifier"""
    # print(value)
    return None
    # if "a" in value:
    #     return {
    #         "name": value.get('a'),
    #         "lang": language.get('a') if language else 'unk'
    #     }
    # if "b" in value:
    #     return {
    #         "name": value.get('b'),
    #         "lang": "eng"
    #     }
