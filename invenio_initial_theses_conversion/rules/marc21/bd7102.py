from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from flask_taxonomies.utils import find_in_json

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import handled_values, extra_argument
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl
from ..utils import db_search, jsonify_fields, get_ref_es


@old_nusl.over('degreeGrantor', '^7102_')
# @handled_values('a', '9', 'g', 'b')
@extra_argument('provider', '^998__', single=True)
def degree_grantor(self, key, values, provider):
    provider = provider.get("a")
    tax = Taxonomy.get("universities", required=True)
    grantors = [item for item in values if item.get("9") == "cze"]
    if len(grantors) == 0:
        grantors = values
    grantor = grantors[0]
    university = grantor.get("a")
    faculty = grantor.get("g")
    department = grantor.get("b")
    uni_res = find_university(university, tax, provider)
    if not uni_res:
        return
    faculty_res = get_ref(faculty, tax, university_slug=uni_res["slug"])
    if not faculty_res:
        return [get_ref_es(uni_res)]
    department_res = get_ref(department, tax, faculty_slug=faculty_res["slug"])
    if not department_res:
        return [get_ref_es(faculty_res)]
    else:
        return [get_ref_es(department_res)]

# if department is not None:
    #     results = get_ref(department, tax)
    # elif faculty is not None:
    #     results = get_ref(faculty, tax)
    # elif university is not None:
    #     results = get_ref(university, tax)
    #     if len(results) == 0:
    #         university = find_uni_name(provider)
    #         if university is not None:
    #             results = get_ref(university, tax)
    # else:
    #     return
    # if len(results) == 0:
    #     return
    # return [{"$ref": result["links"]["self"]} for result in results]


def get_ref(org_unit, taxonomy: Taxonomy, university_slug=None, faculty_slug=None):
    if not org_unit:
        return
    if faculty_slug:
        query = Q("term", taxonomy__keyword="universities") & Q("match", title__value=org_unit) & Q("term", ancestors__slug__keyword=faculty_slug)
    elif university_slug:
        query = Q("term", taxonomy__keyword="universities") & Q("match", title__value=org_unit) & Q("term", ancestors__slug__keyword=university_slug)
    else:
        query = Q("term", taxonomy__keyword="universities") & Q("match", title__value=org_unit)
    results = current_flask_taxonomies_es.search(query, match=True)
    if len(results) == 0:
        results = db_search(org_unit, taxonomy, json_address=("title", 0, "value"))
        results = jsonify_fields(results)
    if len(results) == 0:
        return
    return results[0]


def find_uni_name(provider):
    provider_tax = Taxonomy.get("provider", required=True)
    provider_term = provider_tax.descendants.filter(
        TaxonomyTerm.slug == provider).first()
    try:
        uni_name = provider_term.extra_data["title"][0]["value"]  # TODO: je potřeba změnit, až
        # bude více jazyků
    except KeyError:
        uni_name = None
    return uni_name


def find_university(uni_name, taxonomy, provider):
    university = get_ref(uni_name, taxonomy)
    if not university:
        uni_name = find_uni_name(provider)
        university = get_ref(uni_name, taxonomy)
    return university
