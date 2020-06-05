import json
from pathlib import Path

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.serializer import get_taxonomy_term
from invenio_initial_theses_conversion.nusl_overdo import handled_values
from ..model import old_nusl
from ..utils import get_ref_es


@old_nusl.over("rights", '540')
@handled_values('a', '9')
def rights(self, key, values):
    """Rights."""
    res = set()
    package_dir = Path(__file__).parents[2]
    path = package_dir / "data" / "rights.json"
    with open(str(path), "r") as f:
        rights_dict = json.load(f)
    for value in values:
        if value.get("9") == "cze":
            res.add(json.dumps(get_term(rights_dict.get(value.get("a"), "copyright")),sort_keys=True))
    res = list(res)
    res = [json.loads(item) for item in res]
    return res


def get_term(slug):
    res = current_flask_taxonomies_es.get('licenses', slug)
    if not res:
        res = get_taxonomy_term(code="licenses", slug=slug)
    if not res:
        res = current_flask_taxonomies_es.get('licenses', "copyright")
    return get_ref_es(res)
