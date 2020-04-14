import json

from flask import url_for

from flask_taxonomies.models import Taxonomy, TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl
from ..utils import get_ref_es


@old_nusl.over('provider', '^998__')
@handled_values('a')
@single_value
def provider(self, key, value):
    nusl_slug = value.get("a")
    slug = get_slug(nusl_slug).strip()
    if not slug:
        return
    provider = current_flask_taxonomies_es.get('institutions', slug)
    if provider:
        return get_ref_es(provider)
    tax = Taxonomy.get("institutions", required=True)
    provider = tax.descendants.filter(
        TaxonomyTerm.slug == slug).one()  # viz:
    # https://stackoverflow.com/questions/29974143/python-sqlalchemy-and-postgres-how-to-query-a
    # -json-element
    return {
        "$ref": link_self(tax.slug, provider)
    }


def get_slug(nusl_slug):
    from pathlib import Path
    package_dir = Path(__file__).parents[2]
    path = package_dir / "data" / "providers.json"
    with open(str(path), "r") as f:
        nusl_mapping = json.load(f)
    return nusl_mapping.get(nusl_slug)
