from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd996 import accessibility


def test_language_1(app, db, overdo_instance):
    value = {
        "a": 'Plný text je dostupný v digitálním repozitáři JČU.',
        "b": 'Fulltext is available in the Digital Repository of University of South Bohemia.'
    }
    res = accessibility(overdo_instance, "key", [value])
    url = urlparse(res["accessibility"]["$ref"])
    assert url.path == '/api/taxonomies/accessRights/c_abf2/'
