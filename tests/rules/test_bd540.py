from pprint import pprint
from urllib.parse import urlparse

from invenio_initial_theses_conversion.rules.marc21.bd540 import rights


def test_rights_1(app, db, overdo_instance):
    value = [
        {
            "9": "cze",
            "a": "Dílo je chráněno podle autorského zákona č. 121/2000 Sb."
        },
        {
            "9": "cze",
            "a": "Licence Creative Commons Uveďte autora-Nezasahujte do díla 3.0 Česko"
        },
        {
            "9": "eng",
            "a": "This work is protected under the Copyright Act No. 121/2000 Coll."
        },
        {
            "9": "eng",
            "a": "License: Creative Commons Attribution-NoDerivs 3.0 Czech Republic"
        }
    ]
    res = rights(overdo_instance, "key", value)
    res = res["rights"]
    url = res[0]["$ref"]
    pprint(res)
    url = urlparse(url)
    assert url.path == '/api/taxonomies/licenses/copyright/'
    url = res[1]["$ref"]
    url = urlparse(url)
    assert url.path == '/api/taxonomies/licenses/3-BY-ND-CZ/'


def test_rights_2(app, db, overdo_instance):
    value = [
        {
            "9": "cze",
            "a": "blbost"
        }
    ]
    res = rights(overdo_instance, "key", value)
    res = res["rights"]
    url = res[0]["$ref"]
    url = urlparse(url)
    assert url.path == '/api/taxonomies/licenses/copyright/'
