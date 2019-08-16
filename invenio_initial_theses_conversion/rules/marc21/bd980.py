from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, list_value
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl


@old_nusl.over('doctype', '^980__')
@handled_values('a')
def doctype(self, key, values):
    doc_type = values[0].get('a')
    doctype_tax = Taxonomy.get("doctype", required=True)
    doctype = doctype_tax.descendants.filter(
        TaxonomyTerm.slug == doc_type).one()

    return {
        "$ref": link_self(doctype_tax.slug, doctype)
    }
