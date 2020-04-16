from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy, TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from flask_taxonomies_es.serializer import get_taxonomy_term
from invenio_initial_theses_conversion.nusl_overdo import extra_argument
from .bd998 import get_slug
from ..model import old_nusl
from ..utils import db_search, get_ref_es

TAXONOMY_CODE = "institutions"


@old_nusl.over('degreeGrantor', '^7102_')
@extra_argument('provider', '^998__', single=True)
def degree_grantor(self, key, values, provider):
    provider = provider.get("a")
    grantors = [item for item in values if item.get("9") == "cze"]
    if len(grantors) == 0:
        grantors = values
    grantor = grantors[0]
    university_name = grantor.get("a")
    faculty_name = grantor.get("g")
    department_name = grantor.get("b")
    university_dict = find_org_unit(name=university_name)
    if not university_dict:
        university_dict = get_ref_by_provider(provider)
    if not university_dict:
        university_dict = find_org_unit(name=university_name, query_type="match")
    if not university_dict:
        return
    faculty_dict = find_org_unit(name=faculty_name, parent_slug=university_dict["slug"])
    if not faculty_dict:
        return [get_ref_es(university_dict)]
    department_dict = find_org_unit(name=department_name, parent_slug=university_dict["slug"])
    if not department_dict:
        return [get_ref_es(faculty_dict)]
    else:
        return [get_ref_es(department_dict)]


def find_org_unit(slug=None, name=None, parent_slug=None, parent_name=None, query_type="term"):
    if slug:
        return find_org_by_slug(slug)
    if name:
        return find_uni_by_name(name, parent_name, parent_slug, query_type=query_type)


def find_uni_by_name(name, parent_name=None, parent_slug=None, query_type="term"):
    if query_type == "match":
        query = Q("term", taxonomy__keyword=TAXONOMY_CODE) & Q(query_type,
                                                               title__value=name)
    else:
        query = Q("term", taxonomy__keyword=TAXONOMY_CODE) & Q(query_type, title__value__keyword=name)
    if parent_slug or parent_name:
        if parent_slug:
            parent_query = Q("term", ancestors__slug__keyword=parent_slug)
        else:
            parent_query = Q("term", ancestors__title__value__keyword=parent_slug)
        query = Q('bool',
                  must=[parent_query, query]
                  )
    if query_type == "match":
        results = current_flask_taxonomies_es.search(query, match=True)
    else:
        results = current_flask_taxonomies_es.search(query)
    if not results:
        if query_type == "match":
            query1 = Q(query_type, formerNames=name)
            query2 = Q(query_type, aliases=name)
        else:
            query1 = Q(query_type, formerNames__keyword=name)
            query2 = Q(query_type, aliases__keyword=name)
        q = Q('bool',
              should=[query1, query2]
              )
        if query_type == "match":
            results = current_flask_taxonomies_es.search(q, match=True)
        else:
            results = current_flask_taxonomies_es.search(q)
    if not results:
        tax = Taxonomy.get(TAXONOMY_CODE)
        results = db_search(name, tax, json_address=("title", 0, "value"))
    if results:
        return results[0]


def find_org_by_slug(slug):
    result = current_flask_taxonomies_es.get(TAXONOMY_CODE, slug)
    if not result:
        result = get_taxonomy_term(code=TAXONOMY_CODE, slug=slug)
    return get_ref_es(result)


#     uni_res = find_university(university, tax, provider)
#     if not uni_res:
#         return
#     faculty_res = get_ref(faculty, tax, university_slug=uni_res["slug"])
#     if not faculty_res:
#         return [get_ref_es(uni_res)]
#     department_res = get_ref(department, tax, faculty_slug=faculty_res["slug"])
#     if not department_res:
#         return [get_ref_es(faculty_res)]
#     else:
#         return [get_ref_es(department_res)]
#
#
# def get_ref(org_unit, taxonomy: Taxonomy, university_slug=None, faculty_slug=None):
#     if not org_unit:
#         return
#     if faculty_slug:
#         query = Q("term", taxonomy__keyword="institutions") & Q("match", title__value=org_unit)
#         & Q(
#             "term", ancestors__slug__keyword=faculty_slug)
#     elif university_slug:
#         query = Q("term", taxonomy__keyword="institutions") & Q("term",
#                                                                 title__value__keyword=org_unit)
#                                                                 & Q(
#             "term", ancestors__slug__keyword=university_slug)
#     else:
#         query = Q("term", taxonomy__keyword="institutions") & Q("match", title__value=org_unit)
#     results = current_flask_taxonomies_es.search(query, match=True)
#     if len(results) == 0:
#         results = db_search(org_unit, taxonomy, json_address=("title", 0, "value"))
#     if len(results) == 0:
#         return
#     return results[0]


#
#
def get_ref_by_provider(provider):
    provider_slug = get_slug(provider)
    if not provider_slug:
        return
    provider = current_flask_taxonomies_es.get('institutions', provider_slug)
    if provider:
        return provider
    return get_taxonomy_term(TAXONOMY_CODE, provider_slug)
    # provider_term = provider_tax.descendants.filter(
    #     TaxonomyTerm.slug == provider).first()
    # try:
    #     # TODO: je potřeba změnit až bude více jazyků
    #     uni_name = provider_term.extra_data["title"][0]["value"]
    # except KeyError:
    #     uni_name = None
    # return uni_name
#
#
# def find_university(uni_name, taxonomy, provider):
#     university = get_ref(uni_name, taxonomy)
#     if not university:
#         uni_name = get_ref_by_provider(provider)
#         university = get_ref(uni_name, taxonomy)
#     return university
