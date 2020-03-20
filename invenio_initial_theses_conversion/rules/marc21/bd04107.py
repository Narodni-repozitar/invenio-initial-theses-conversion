import pycountry
from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
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
        lang = get_lang("a", value)
        if lang is None:
            return None
        languages.append(get_ref(lang, tax))
    if "b" in value:
        lang = get_lang("b", value)
        if lang is None:
            return None
        languages.append(get_ref(lang, tax))
    return languages


def get_lang(key, value):
    lang = value.get(key)
    lang = ensure_lang_code(lang)
    return lang


def get_ref(lang, taxonomy):
    res = current_flask_taxonomies_es.get("languages", lang)
    if len(res) > 0 and isinstance(res, dict):
        return {
            "$ref": res["links"]["self"]
        }
    lang_tax = taxonomy.get_term(lang)
    if lang_tax is None:
        return None
    return {
        "$ref": link_self(taxonomy.slug, lang_tax)
    }


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
