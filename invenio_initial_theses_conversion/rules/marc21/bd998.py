from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, merge_results
from invenio_initial_theses_conversion.scripts.link import link_self
from invenio_initial_theses_conversion.taxonomies.nusl_collections import institution_taxonomy
from ..model import old_nusl


@old_nusl.over('provider', '^998__')
@handled_values('a')
@single_value
def provider(self, key, value):
    data = value.get('a')
    tax = Taxonomy.get("provider", required=True)
    provider = tax.descendants.filter(
        TaxonomyTerm.slug == data).one()  # viz: https://stackoverflow.com/questions/29974143/python-sqlalchemy-and-postgres-how-to-query-a-json-element
    result = {
        "$ref": link_self(provider) #TODO: měl by být link_self
    }

    return result

# {
#   "address": "Královopolská 147, 612 00 Brno",
#   "id": 8207,
#   "lib_url": "http://arub.avcr.cz/knihovna/",
#   "links": {
#     "self": "https://127.0.0.1:5000/api/taxonomies/provider/research/avcr/archeologicky_ustav_brno/",
#     "tree": "https://127.0.0.1:5000/api/taxonomies/provider/research/avcr/archeologicky_ustav_brno/?drilldown=True"
#   },
#   "name": [
#     {
#       "lang": "cze",
#       "name": "Archeologický ústav, Brno"
#     }
#   ],
#   "path": "/provider/research/avcr/archeologicky_ustav_brno",
#   "slug": "archeologicky_ustav_brno",
#   "url": "http://www.arub.cz/"
# }
