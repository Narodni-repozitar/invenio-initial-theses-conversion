from urllib.parse import urlparse

from flask_taxonomies.models import Taxonomy
from invenio_search import current_search_client

from invenio_initial_theses_conversion.rules.marc21.bd656 import study_programme_field, \
    es_search_title, aliases
from invenio_initial_theses_conversion.rules.utils import db_search


def test_study_programme_field_1(app, db, overdo_instance):
    value = {
        'a': 'Psychologie/Arteterapie',
        '2': 'AKVO'
    }
    results = study_programme_field(overdo_instance, "key", [value])
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/O_arteterapie/'


def test_study_programme_field_2(app, db, overdo_instance):
    value = {
        'a': 'Psychologie',
        '2': 'AKVO'
    }
    results = study_programme_field(overdo_instance, "key", [value])
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/P_psychologie/'


def test_study_programme_field_3(app, db, overdo_instance):
    value = {
        'a': 'Učitelství pro střední školy/ČJ-L/SŠ',
        '2': 'AKVO'
    }
    results = study_programme_field(overdo_instance, "key", [value])
    assert isinstance(results, dict)
    url = urlparse(results["studyField"][0]["$ref"])
    assert url.path == '/api/taxonomies/studyfields/O_ucitelstvi-ceskeho-jazyka-a-literatury-pro' \
                       '-stredni-skoly/'


def test_study_programme_field_4(app, db, overdo_instance):
    value = {
        'a': 'blbost',
        '2': 'AKVO'
    }

    results = study_programme_field(overdo_instance, "key", [value])
    assert results is None


def test_study_programme_field_5(app, db, overdo_instance):
    try:
        app.config.update(TAXONOMY_ELASTICSEARCH_INDEX="test_taxonomies_es")
        value = {
            'a': 'Psychologie/Arteterapie',
            '2': 'AKVO'
        }
        results = study_programme_field(overdo_instance, "key", [value])
        assert isinstance(results, dict)
        url = urlparse(results["studyField"][0]["$ref"])
        assert url.path == '/api/taxonomies/studyfields/O_arteterapie/'
    finally:
        with app.app_context():
            current_search_client.indices.delete(
                index="test_taxonomies_es")


def test_es_search_title(app, db):
    results = es_search_title("Filozofie", "studyfields")
    assert len(results) == 2


def test_db_search(app, db):
    tax = Taxonomy.get("studyfields", required=True)
    fields = db_search("Arteterapie", tax, json_address=("title", 0, "value"))
    assert isinstance(fields, list)
    for field in fields:
        assert "slug" in field.keys()
        assert "title" in field.keys()
        assert "links" in field.keys()


def test_aliases(app, db):
    ret = aliases('Zemědělství - Prvovýroba')
    assert ret == 'Zemědělství'
