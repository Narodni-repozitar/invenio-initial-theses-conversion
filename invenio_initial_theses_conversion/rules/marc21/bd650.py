from functools import lru_cache
from urllib.parse import urlparse

from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy, TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from ..model import old_nusl
from ..utils import jsonify_fields, get_ref_es


@old_nusl.over("subject", '^650_7')
@append_results
@list_value
@handled_values('0', '2', 'a', 'j', '7')
def subject(self, key, values):
    """Subject."""
    taxonomy = Taxonomy.get("subjects")
    return get_subject(taxonomy, values)


def get_subject(taxonomy, value):
    id_ = value.get("7")
    url = value.get("0")
    type = value.get("2")
    cz_keyword = value.get("a")
    eng_keyword = value.get("j")
    if id_:
        results = find_by_id(id_, taxonomy.slug, type)
        if len(results) > 0 and results is not None:
            return get_ref_es(results[0])
    if url:
        results = find_by_url(url, taxonomy.slug, type)
        if len(results) > 0 and results is not None:
            return get_ref_es(results[0])
    if cz_keyword or eng_keyword:
        for keyword in [cz_keyword, eng_keyword]:
            results = find_by_title(keyword, taxonomy.slug, type)
            if len(results) > 0 and results is not None:
                return get_ref_es(results[0])
    return {
        "title": [
            {
                "value": cz_keyword,
                "lang": "cze"
            },
            {
                "value": eng_keyword,
                "lang": "eng"
            },
        ],
        "type": type
    }


def find_by_title(keyword, tax, type):
    query = Q("term", taxonomy__keyword=tax) & Q("term", title__value__keyword=keyword)
    results = current_flask_taxonomies_es.search(query)
    if len(results) > 0:
        return results
    return db_search(keyword, type, search_taxonomy_by_title)


def find_by_id(id_, tax, type):
    query = Q("term", taxonomy__keyword=tax) & Q("term", slug__keyword=id_)
    results = current_flask_taxonomies_es.search(query)
    if len(results) > 0:
        return results
    return db_search(id_, type, search_json_by_slug)


def find_by_url(url, tax, type):
    query = Q("term", taxonomy__keyword=tax) & Q("term", url__keyword=url)
    results = current_flask_taxonomies_es.search(query)
    if len(results) > 0:
        return results
    url_parser = urlparse(url)
    path = url_parser.path
    path_array = path.split("/")
    path_array = [node for node in path_array if len(node) > 0]
    slug = path_array[-1]
    query = Q("term", taxonomy__keyword=tax) & Q("term", slug__keyword=slug)
    results = current_flask_taxonomies_es.search(query)
    if len(results) > 0:
        return results
    return db_search(slug, type, search_json_by_slug)


def db_search(slug, type, handler):
    taxonomy_term = get_taxonomy_term(type)
    if not taxonomy_term:
        return []
    results = handler(slug, taxonomy_term)
    return jsonify_fields(results)


@lru_cache(maxsize=10000)
def search_taxonomy_by_title(keyword, parent_term):
    subject = parent_term.descendants.filter(
        TaxonomyTerm.extra_data["title"].contains([{"value": keyword}])).all()
    return subject


@lru_cache(maxsize=10000)
def search_json_by_slug(id, parent_term):
    subject = parent_term.descendants.filter(
        TaxonomyTerm.slug == id).all()
    return subject


@lru_cache(maxsize=10000)
def get_taxonomy_term(type: str):
    taxonomy = Taxonomy.get("subject")
    taxonomy_term = taxonomy.get_term(type.lower())
    return taxonomy_term
