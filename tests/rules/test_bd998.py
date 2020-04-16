from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd998 import provider


def test_provider_1(app, db, overdo_instance):
    value = {
        'a': 'jihoceska_univerzita_v_ceskych_budejovicich'
    }
    res = provider(overdo_instance, "key", [value])
    assert isinstance(res, dict)
    url = urlparse(res["$ref"])
    assert url.path == '/api/taxonomies/institutions/60076658/'
