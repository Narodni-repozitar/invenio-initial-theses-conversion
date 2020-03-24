from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd04107 import language


def test_language_1(app, db, overdo_instance):
    value = {
        "a": "cze",
        "b": "ger"
    }
    res = language(overdo_instance, "key", [value])
    for result in res:
        assert len(result) == 1
        assert "$ref" in result.keys()
    url = res[0]["$ref"]
    url = urlparse(url)
    assert url.path == '/api/taxonomies/languages/cze'
    url = res[1]["$ref"]
    url = urlparse(url)
    assert url.path == '/api/taxonomies/languages/ger'


