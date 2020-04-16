from pprint import pprint
from urllib.parse import urlparse

import pytest

from invenio_initial_theses_conversion.rules.marc21.bd7102 import degree_grantor, find_uni_by_name
from tests.conftest import grantors


def test_degree_grantor(app, db, overdo_instance):
    value = {
        'a': 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH',
        '9': 'cze'
    }
    provider = {
        'a': 'jihoceska_univerzita_v_ceskych_budejovicich'
    }
    results = degree_grantor(overdo_instance, "key", [value], provider)
    assert isinstance(results, list)
    url = urlparse(results[0]["$ref"])
    assert url.path == '/api/taxonomies/institutions/60076658/'


def test_degree_grantor_2(app, db, overdo_instance):
    value = {
        'a': 'Univerzita Karlova',
        'b': 'Katedra žurnalistiky',
        'g': 'Fakulta sociálních věd',
        '9': 'cze'
    }
    provider = {
        'a': 'univerzita_karlova_v_praze'
    }
    results = degree_grantor(overdo_instance, "key", [value], provider)
    pprint(results)
    assert isinstance(results, list)
    url = urlparse(results[0]["$ref"])
    assert url.path == '/api/taxonomies/institutions/katedra-zurnalistiky/'


def test_degree_grantor_3(app, db, overdo_instance):
    value = {
        'a': 'bla',
        '9': 'cze'
    }
    provider = {
        'a': 'jihoceska_univerzita_v_ceskych_budejovicich'
    }
    results = degree_grantor(overdo_instance, "key", [value], provider)
    assert isinstance(results, list)
    url = urlparse(results[0]["$ref"])
    assert url.path == '/api/taxonomies/institutions/60076658/'


def test_degree_grantor_4(app, db, overdo_instance):
    value = {
        'a': 'bla',
        '9': 'cze'
    }
    provider = {
        'a': 'bla'
    }
    results = degree_grantor(overdo_instance, "key", [value], provider)
    assert results is None


@pytest.mark.parametrize("value", list(grantors()))
def test_degree_grantor_5(app, db, overdo_instance, value):
    provider = {
        'a': 'bla'
    }
    results = degree_grantor(overdo_instance, "key", [value], provider)
    assert results is not None
    pprint(value)
    pprint(results)
    print("\n\n\n")


def test_find_uni_by_name(app, db):
    find_uni_by_name('Mendelova univerzita', query_type="match")
