from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy
from flask_taxonomies.utils import find_in_json_contains

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import single_value, merge_results, \
    extra_argument
from ..model import old_nusl
from ..utils import db_search, jsonify_fields, get_ref_es


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
@extra_argument('grantor', '^7102', single=True)
@extra_argument('doc_type', '^980', single=True)
def study_programme_field(self, key, value, grantor, doc_type):
    """Study programme."""
    doc_type = doc_type.get("a")
    grantor = grantor.get("a").lower()
    slug = value.get("a")
    tax = Taxonomy.get("studyfields", required=True)
    if "/" not in slug:
        return studyfield_ref(slug.strip(), tax, grantor, doc_type)
    else:
        programme, field = slug.split("/", maxsplit=1)
        field = field.strip()
        return studyfield_ref(field, tax, grantor, doc_type)


def es_search_title(study, tax):
    query = Q("term", taxonomy__keyword=tax) & Q("term", title__value__keyword=study)
    return current_flask_taxonomies_es.search(query)


def es_search_aliases(study, tax):
    query = Q("term", taxonomy__keyword=tax) & Q("term", aliases__keyword=study)
    return current_flask_taxonomies_es.search(query)


def studyfield_ref(study_title, tax, grantor: str, doc_type: str):
    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
    # https://github.com/sqlalchemy/sqlalchemy/issues/3859  # issuecomment-441935478
    fields = es_search_title(study_title, tax.slug)
    if len(fields) == 0:
        fields = db_search(study_title, tax, json_address=("title", 0, "value"))
    if len(fields) == 0:
        fields = aliases(tax, study_title)
    if len(fields) == 0:
        return []
    if len(fields) > 1:
        fields = filter(fields, doc_type, grantor)

    return {
        "studyField": [get_ref_es(field) for field in fields],
    }


def aliases(tax, study):
    fields = es_search_aliases(study, tax.slug)
    if len(fields) == 0:
        fields = db_search(study, tax, json_address="aliases")
    if len(fields) == 0:
        fields = find_in_json_contains(study, tax, tree_address="aliases").all()
        fields = jsonify_fields(fields)
    return fields


def filter(fields, doc_type, grantor):
    fields = doc_filter(fields, doc_type)
    fields = grantor_filter(fields, grantor)
    return fields


def doc_filter(fields, doc_type):
    if doc_type is not None:
        if doc_type == "rigorozni_prace":
            doc_type = "disertacni_prace"
        degree_dict = {
            "Bakalářský": "bakalarske_prace",
            "Magisterský": "diplomove_prace",
            "Navazující magisterský": "diplomove_prace",
            "Doktorský": "disertacni_prace"
        }
        new_fields = [field for field in fields if
                      degree_dict.get(field.get("programme_type")) == doc_type]
        if len(new_fields) == 0:
            new_fields = [field for field in fields if "programme_type" not in field.keys()]
        return new_fields
    return fields


def grantor_filter(fields, grantor):
    if grantor is not None:
        matched_fields = [field for field in fields if
                          field.get("grantor") is not None and
                          field["grantor"][0][
                              "university"].lower() == grantor.lower()]
        if len(matched_fields) == 0:
            return fields
        else:
            return matched_fields
    else:
        return fields
