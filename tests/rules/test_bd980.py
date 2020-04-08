from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd980 import doctype


def test_doctype_1(app, db, overdo_instance):
    value = {
        'a': 'bakalarske_prace'
    }
    res = doctype(overdo_instance, "key", [value])
    assert isinstance(res, dict)
    url = urlparse(res["$ref"])
    assert url.path == '/api/taxonomies/doctypes/bakalarske_prace/'