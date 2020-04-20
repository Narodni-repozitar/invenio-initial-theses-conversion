from datetime import datetime
from functools import lru_cache
from urllib.parse import urlparse

import validators
from elasticsearch_dsl import Q
from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_db import db

from flask_taxonomies.utils import find_in_json
from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from ..model import old_nusl
from ..utils import jsonify_fields, get_ref_es

from flask_taxonomies_es.serializer import get_taxonomy_term as get_tax_term_es

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
    if url:
        if not validators.url(url):
            if not id_:
                id_ = url
            url = None
    if id_:
        results = find_by_id(id_, taxonomy.slug, type)
        if results:
            return get_ref_es(results[0])
    if url:
        results = find_by_url(url, taxonomy.slug, type)
        if results:
            return get_ref_es(results[0])
    if cz_keyword or eng_keyword:
        for keyword in [cz_keyword, eng_keyword]:
            results = find_by_title(keyword, taxonomy.slug, type)
            if results and (type in results[0]["path"]):
                return get_ref_es(results[0])
            else:
                term = create_taxonomy_term(id_, cz_keyword, eng_keyword, type)
                return get_ref_es(get_tax_term_es(code="subjects", slug=term.slug))
    return


def create_taxonomy_term(slug, cz_keyword, en_keyword, type):
    tax = Taxonomy.get("subjects")
    parent_term = tax.get_term(type)
    if not parent_term:
        parent_term = tax.create_term(slug=type)
        db.session.add(parent_term)
        db.session.commit()
    extra_data = {
        "title": [
            {
                "value": cz_keyword,
                "lang": "cze"
            },
            {
                "value": en_keyword,
                "lang": "eng"
            }
        ],
        "approved": False
    }
    term = tax.get_term(slug=slug)
    if not term:
        term = parent_term.create_term(slug=slug, extra_data=extra_data)
        db.session.add(term)
        db.session.commit()
        current_flask_taxonomies_es.set(term, timestamp=datetime.utcnow())
    return term


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
    subject = find_in_json(keyword, parent_term).all()
    return subject


@lru_cache(maxsize=10000)
def search_json_by_slug(id, parent_term):
    subject = parent_term.descendants.filter(
        TaxonomyTerm.slug == id).all()
    return subject


@lru_cache(maxsize=10000)
def get_taxonomy_term(type: str):
    taxonomy = Taxonomy.get("subjects")
    taxonomy_term = taxonomy.get_term(type.lower())
    return taxonomy_term
