from pprint import pprint
from urllib.parse import urlparse

import pytest
from flask_taxonomies.models import Taxonomy
from invenio_search import current_search_client

from .fixtures import grantor_filter_fix, doc_filter_fix

from invenio_initial_theses_conversion.rules.marc21.bd656 import study_programme_field, \
    doc_filter, \
    es_search_title, grantor_filter, es_search_aliases, db_search, aliases


def test_study_programme_field_1(app, db, overdo_instance):
    value = {
        'a': 'Psychologie/Arteterapie',
        '2': 'AKVO'
    }
    doc_type = {
        'a': 'bakalarske_prace'
    }
    grantor = {
        'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
        '9': 'cze'
    }
    results = study_programme_field(overdo_instance, "key", [value], grantor, doc_type)
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/B7701/7701R012/'


def test_study_programme_field_2(app, db, overdo_instance):
    value = {
        'a': 'Psychologie',
        '2': 'AKVO'
    }
    doc_type = {
        'a': 'bakalarske_prace'
    }
    grantor = {
        'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
        '9': 'cze'
    }
    results = study_programme_field(overdo_instance, "key", [value], grantor, doc_type)
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/B7701/7701R005/'


def test_study_programme_field_3(app, db, overdo_instance):
    value = {
        'a': 'Učitelství pro střední školy/ČJ-L/SŠ',
        '2': 'AKVO'
    }
    doc_type = {
        'a': 'bakalarske_prace'
    }
    grantor = {
        'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
        '9': 'cze'
    }
    results = study_programme_field(overdo_instance, "key", [value], grantor, doc_type)
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/N7504/7504T039/'


def test_study_programme_field_4(app, db, overdo_instance):
    value = {
        'a': 'blbost',
        '2': 'AKVO'
    }
    doc_type = {
        'a': 'bakalarske_prace'
    }
    grantor = {
        'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
        '9': 'cze'
    }
    results = study_programme_field(overdo_instance, "key", [value], grantor, doc_type)
    assert results is None


def test_study_programme_field_5(app, db, overdo_instance):
    try:
        app.config.update(TAXONOMY_ELASTICSEARCH_INDEX="test_taxonomies_es")
        value = {
            'a': 'Psychologie/Arteterapie',
            '2': 'AKVO'
        }
        doc_type = {
            'a': 'bakalarske_prace'
        }
        grantor = {
            'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
            '9': 'cze'
        }
        results = study_programme_field(overdo_instance, "key", [value], grantor, doc_type)
        assert isinstance(results, dict)
        url = urlparse(results["studyField"][0]["$ref"])
        assert url.path == '/api/taxonomies/studyfields/B7701/7701R012/'
    finally:
        with app.app_context():
            current_search_client.indices.delete(
                index="test_taxonomies_es")


def test_es_search_title(app, db):
    results = es_search_title("Filozofie", "studyfields")
    assert len(results) == 8


def test_es_search_aliases(app, db):
    results = es_search_aliases("ČJ-L/SŠ", "studyfields")
    assert len(results) == 1


def test_doc_filter(doc_filter_fix):
    res = doc_filter(doc_filter_fix, 'bakalarske_prace')
    assert len(res) == 1


def test_grantor_filter(grantor_filter_fix):
    res = grantor_filter(grantor_filter_fix, 'Jihočeská univerzita v Českých Budějovicích')
    assert len(res) == 2


def test_db_search(app, db):
    tax = Taxonomy.get("studyfields", required=True)
    fields = db_search("Arteterapie", tax, json_address=("title", 0, "value"))
    assert isinstance(fields, list)
    for field in fields:
        assert "slug" in field.keys()
        assert "title" in field.keys()
        assert "links" in field.keys()


def test_aliases(app, db):
    try:
        app.config.update(TAXONOMY_ELASTICSEARCH_INDEX="test_taxonomies_es")
        tax = Taxonomy.get("studyfields", required=True)
        fields = aliases(tax, "ČJ-L/SŠ")
        assert isinstance(fields, list)
        for field in fields:
            assert "slug" in field.keys()
            assert "title" in field.keys()
            assert "links" in field.keys()
    finally:
        with app.app_context():
            current_search_client.indices.delete(
                index="test_taxonomies_es")
