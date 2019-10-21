import pycountry

from flask_taxonomies.models import Taxonomy
from invenio_initial_theses_conversion.nusl_overdo import single_value, append_results, list_value, handled_values
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl


@old_nusl.over("language", '^041')
@single_value
@handled_values('a', 'b')
def language(self, key, value):
    """Language Code."""
    languages = []
    tax = Taxonomy.get("languages")
    if not value.get("a"):
        return None
    if "a" in value:
        lang = value.get("a")
        lang = ensure_lang_code(lang)
        if lang is None:
            return None
        get_ref(lang, languages, tax)
    if "b" in value:
        lang = value.get("b")
        lang = ensure_lang_code(lang)
        if lang is None:
            return None
        get_ref(lang, languages, tax)
    return languages


def get_ref(lang, languages, taxonomy):
    lang_tax = taxonomy.get_term(lang)
    if lang_tax is None:
        return None
    languages.append({
        "$ref": link_self(taxonomy.slug, lang_tax)
    })


def ensure_lang_code(lang):
    alpha3 = pycountry.languages.get(alpha_3=lang)
    bib = pycountry.languages.get(bibliographic=lang)
    if bib is not None:
        lang = bib.bibliographic
    elif alpha3 is not None:
        lang = alpha3.alpha_3
    else:
        return None
    return lang
