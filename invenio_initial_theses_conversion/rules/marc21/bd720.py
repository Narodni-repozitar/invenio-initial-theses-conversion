from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.serializer import get_taxonomy_term
from invenio_initial_theses_conversion.nusl_overdo import merge_results
from ..model import old_nusl
from ..utils import get_ref_es
from ...scripts.link import link_self


@old_nusl.over("creator", '^720')
@merge_results
def people(self, key, value):
    """Creator and contributor"""
    creator = []
    contributor = []
    for person in value:
        if person.get('a'):
            creator.append({
                "name": person.get('a'),
            })
        if person.get('i'):
            contributor.append({
                "name": person.get('i'),
                "role": get_role(person.get('e')),
            })
    return {
        "creator": creator,
        "contributor": contributor
    }


def get_role(role):
    res = current_flask_taxonomies_es.get("contributor-type", role)
    if not res:
        tax = Taxonomy.get("contributor-type")
        term = tax.get_term(role)
        if term:
            return {
                "$ref": link_self(tax.slug, term)
            }
        else:
            return
    return get_ref_es(res)
