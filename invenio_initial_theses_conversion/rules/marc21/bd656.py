import json

from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, merge_results
from ..model import old_nusl
from ..utils import db_search, get_ref_es


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
def study_programme_field(self, key, value):
    """Study programme."""
    source = value.get("a")
    tax = Taxonomy.get("studyfields", required=True)
    if "/" not in source:
        return studyfield_ref(source.strip(), tax)
    else:
        programme, field = source.split("/", maxsplit=1)
        field = field.strip()
        return studyfield_ref(field, tax)


def es_search_title(study, tax):
    query = Q("term", taxonomy__keyword=tax) & Q("term", title__value__keyword=study)
    return current_flask_taxonomies_es.search(query)


def studyfield_ref(study_title, tax):
    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
    # https://github.com/sqlalchemy/sqlalchemy/issues/3859  # issuecomment-441935478
    if study_title is None:
        return
    fields = es_search_title(study_title, tax.slug)
    if len(fields) == 0:
        fields = db_search(study_title, tax, json_address=("title", 0, "value"))
    if len(fields) > 0:
        fields_filtered = [field for field in fields if field["slug"].startswith("P")]
        if len(fields_filtered) > 0:
            fields = fields_filtered
        return {
            "studyField": [get_ref_es(field) for field in fields],
        }
    else:
        return studyfield_ref(aliases(study_title), tax)


def aliases(field):
    from pathlib import Path
    package_dir = Path(__file__).parents[2]
    path = package_dir / "data" / "aliases.json"
    with open(str(path), "r") as f:
        alias_dict = json.load(f)
    return alias_dict.get(field)
