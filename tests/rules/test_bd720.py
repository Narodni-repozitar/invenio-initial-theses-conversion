from pprint import pprint
from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd720 import people


def test_person_1(app, db, overdo_instance):
    value = [
        {
            "a": "Dvořáková, Pavlína"
        },
        {
            "i": "Holanová, Petra",
            "e": "advisor"
        },
        {
            "i": "Pucholtová, Romana",
            "e": "referee"
        }
    ]
    results = people(overdo_instance, "key", value)
    assert "creator" in results.keys() and "contributor" in results.keys()
    url1 = urlparse(results["contributor"][0]["role"]["$ref"])
    url2 = urlparse(results["contributor"][1]["role"]["$ref"])
    assert url1.path == '/api/taxonomies/contributor-type/advisor/'
    assert url2.path == '/api/taxonomies/contributor-type/referee/'
    pprint(results)


def test_person_2(app, db, overdo_instance):
    value = [
        {
            "a": "Dvořáková, Pavlína"
        },
        {
            "i": "Holanová, Petra",
            "e": "blbost"
        },
        {
            "i": "Pucholtová, Romana",
            "e": "referee"
        }
    ]
    results = people(overdo_instance, "key", value)
    assert "creator" in results.keys() and "contributor" in results.keys()
    assert results["contributor"][0]["role"] is None
    url2 = urlparse(results["contributor"][1]["role"]["$ref"])
    assert url2.path == '/api/taxonomies/contributor-type/referee/'
    pprint(results)
