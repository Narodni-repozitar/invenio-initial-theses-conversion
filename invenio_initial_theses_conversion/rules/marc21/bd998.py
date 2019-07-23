from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, merge_results
from invenio_initial_theses_conversion.taxonomies.nusl_collections import institution_taxonomy
from ..model import old_nusl


@old_nusl.over('provider', '^998__')
@handled_values('a')
@single_value
def provider(self, key, value):
    data = value.get('a')
    tax = Taxonomy.get("provider", required=True)
    provider = tax.descendants.filter(TaxonomyTerm.slug == data).one()   #viz: https://stackoverflow.com/questions/29974143/python-sqlalchemy-and-postgres-how-to-query-a-json-element
    return provider.extra_data
