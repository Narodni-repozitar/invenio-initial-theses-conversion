from pprint import pprint
from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd7102 import degree_grantor


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
    assert url.path == '/api/taxonomies/universities/60076658'


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
    assert url.path == '/api/taxonomies/universities/katedra_zurnalistiky'
