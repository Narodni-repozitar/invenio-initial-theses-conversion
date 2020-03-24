from pprint import pprint

from flask_taxonomies.models import TaxonomyTerm

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
    assert results[0] == {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/D010811'}
    assert isinstance(results, list)


def test_get_taxonomy_term(app, db):
    taxonomy_term = get_taxonomy_term("PSH")
    assert isinstance(taxonomy_term, TaxonomyTerm)


def test_get_taxonomy_term_2(app, db):
    taxonomy_term = get_taxonomy_term("BLBOST")
    assert taxonomy_term is None
