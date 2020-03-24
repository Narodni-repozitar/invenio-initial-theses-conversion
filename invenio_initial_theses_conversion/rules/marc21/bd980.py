from flask_taxonomies.models import Taxonomy, TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, list_value
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl
from ..utils import get_ref_es


@old_nusl.over('doctype', '^980__')
@handled_values('a')
def doctype(self, key, values):
    doc_type = values[0].get('a')
    es_result = current_flask_taxonomies_es.get("doctype", doc_type)
    if es_result:
        return get_ref_es(es_result)
    doctype_tax = Taxonomy.get("doctype", required=True)
    doctype = doctype_tax.descendants.filter(
        TaxonomyTerm.slug == doc_type).one()

    return {
        "$ref": link_self(doctype_tax.slug, doctype)
    }
