from invenio_initial_theses_conversion.lang import assert_language
from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl
from langdetect import detect_langs


@old_nusl.over("subtitle", '24633')
@list_value
@extra_argument('language', '04107', single=True, default={'a': 'cze'})
@handled_values('a', 'b')
def subtitle_value(self, key, value, language):
    """Language Code."""

    record_lang = language.get('a') if language else 'unk'

    if "a" in value:
        a_lang = assert_language(value.get('a'), record_lang)
        return {
            "name": value.get('a'),
            "lang": a_lang
        }
    if "b" in value:
        return {
            "name": value.get('b'),
            "lang": "eng"
        }
