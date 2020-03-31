from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, \
    merge_results
from ..model import old_nusl
from ..utils import get_ref_es
from ...scripts.link import link_self


@old_nusl.over('accessibility', '^996__')
@merge_results
@handled_values('a', 'b', '9')
@single_value
def accessibility(self, key, value):
    ret = {}
    sentence = value.get("a")
    if not sentence:
        return
    access_right_dict = {
        "0": "c_14cb",
        "1": "c_abf2",
        "2": "c_16ec "
    }

    sentence_dict = {
        "Dokument je dostupný v repozitáři Akademie věd.": "1",
        "Dokumenty jsou dostupné v systému NK ČR.": "1",
        "Plný text je dostupný v Digitální knihovně VUT.": "1",
        "Dostupné v digitálním repozitáři VŠE.": "1",
        "Plný text je dostupný v digitálním repozitáři JČU.": "1",
        "Dostupné v digitálním repozitáři UK.": "1",
        "Dostupné v digitálním repozitáři Mendelovy univerzity.": "1",
        "Dostupné v repozitáři ČZU.": "1",
        "Dostupné registrovaným uživatelům v digitálním repozitáři AMU.": "2",
        "Dokument je dostupný v NLK. Dokument je dostupný též v digitální formě v Digitální "
        "knihovně NLK. Přístup může být vázán na prohlížení z počítačů NLK.": "2",
        "Dostupné v digitálním repozitáři UK (pouze z IP adres univerzity).": "2",
        "Text práce je neveřejný, pro více informací kontaktujte osobu uvedenou v repozitáři "
        "Mendelovy univerzity.": "2",
        "Dokument je dostupný na vyžádání prostřednictvím repozitáře Akademie věd.": "2",
        "Dokument je dostupný v příslušném ústavu Akademie věd ČR.": "0",
        "Dokument je po domluvě dostupný v budově Ministerstva životního prostředí.": "0",
        "Plný text není k dispozici.": "0",
        "Dokument je dostupný v NLK.": "0",
        'Dokument je po domluvě dostupný v budově <a '
        'href=\"http://www.mzp.cz/__C125717D00521D29.nsf/index.html\" '
        'target=\"_blank\">Ministerstva životního prostředí</a>.': "0",
        "Dostupné registrovaným uživatelům v knihovně Mendelovy univerzity v Brně.": "0"
    }

    slug = access_right_dict.get(sentence_dict.get(sentence))
    accessibility = get_ref(slug)

    ret["accessibility"] = accessibility
    return ret


def get_ref(slug):
    res = current_flask_taxonomies_es.get("accessRights", slug)
    if len(res) > 0 and isinstance(res, dict):
        return get_ref_es(res)
    tax = Taxonomy.get("accessRights", required=True)
    res = tax.get_term(slug)
    if res is None:
        return None
    return {
        "$ref": link_self(res.slug, tax)
    }
