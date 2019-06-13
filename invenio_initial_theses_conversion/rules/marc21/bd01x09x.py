from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value
from ..model import old_nusl


@old_nusl.over("title", '24500')
@single_value
@extra_argument('language', '04107', single=True)
def title_value(self, key, value, language):
    """Language Code."""
    return {
        "value": value.get('a'),
        "language": language.get('a') if language else 'unk'
    }
