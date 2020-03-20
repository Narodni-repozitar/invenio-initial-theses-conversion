from flask import url_for

from flask_taxonomies.models import Taxonomy, TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl


@old_nusl.over('provider', '^998__')
@handled_values('a')
@single_value
def provider(self, key, value):
    slug = value.get('a')
    provider = current_flask_taxonomies_es.get('provider', slug)
    if provider:
        return {
            "$ref": provider["links"]["self"]
        }
    tax = Taxonomy.get("provider", required=True)
    provider = tax.descendants.filter(
        TaxonomyTerm.slug == slug).one()  # viz:
    # https://stackoverflow.com/questions/29974143/python-sqlalchemy-and-postgres-how-to-query-a
    # -json-element
    return {
        "$ref": link_self(tax.slug, provider)
    }
