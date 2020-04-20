from pprint import pprint
from urllib.parse import urlparse

from flask_taxonomies.models import TaxonomyTerm

from flask_taxonomies_es.proxies import current_flask_taxonomies_es
from invenio_initial_theses_conversion.rules.marc21.bd650 import subject, get_taxonomy_term


def test_subject_1(app, db, overdo_instance):
    value = [
        {
            '2': 'mednas',
            '7': 'nlk20040148348',
            'a': 'přírodní vědy',
        },
        {
            '2': 'czmesh',
            '7': 'D002626',
            'a': 'chemie farmaceutická',
        },
        {
            '2': 'czmesh',
            '7': 'D002620',
            'a': 'farmakologické a toxikologické jevy a procesy',
        },
        {
            '2': 'czenas',
            '0': 'ph114722',
            'a': 'hudebniny',
        },
        {
            '2': 'czenas',
            '0': 'ph114722',
            'a': 'hudba',
        },
        {
            '0': 'http://psh.ntkcz.cz/skos/PSH11857',
            '2': 'PSH',
            'a': 'hudba',
            'j': 'music'
        },
    ]
    results = subject(overdo_instance, "key", value)
    assert len(results) == 6
    for result in results:
        assert "$ref" in result.keys()
        url = urlparse(result["$ref"])
        path_array = url.path.split("/")
        slug = path_array[-2]
        assert current_flask_taxonomies_es.get("subjects", slug) is not None


def test_get_taxonomy_term(app, db):
    taxonomy_term = get_taxonomy_term("PSH")
    assert isinstance(taxonomy_term, TaxonomyTerm)


def test_get_taxonomy_term_2(app, db):
    taxonomy_term = get_taxonomy_term("BLBOST")
    assert taxonomy_term is None


def test_subject_2(app, db, overdo_instance):
    value = [
        {
            "a": "filigrány(papír)",
            "0": "ph120179",
            "2": "czenas"
        }
    ]
    results = subject(overdo_instance, "key", value)
    pprint(results)
    # assert len(results) == 6
    # for result in results:
    #     assert "$ref" in result.keys()
    #     url = urlparse(result["$ref"])
    #     path_array = url.path.split("/")
    #     slug = path_array[-2]
    #     assert current_flask_taxonomies_es.get("subjects", slug) is not None
