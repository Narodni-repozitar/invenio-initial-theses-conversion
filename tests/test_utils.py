from collections import OrderedDict
from pprint import pprint

from dojson.utils import GroupableOrderedDict

from invenio_initial_theses_conversion.rules.utils import get_ref_es
from invenio_initial_theses_conversion.utils import fix_grantor, split_keywords


def test_split_keywords_1():
    keywords = (
        GroupableOrderedDict(OrderedDict({"a": "mladší školní věk - slovo"})),
        GroupableOrderedDict(OrderedDict({
            "a": "internacionalismus|neologismus|lexikální "
                 "sémantika|pragmatika|kultura|politika|zpravodajství|deník"
        })),
    )
    res = split_keywords(keywords)
    assert res == (
        GroupableOrderedDict(OrderedDict({'a': 'mladší školní věk'})),
        GroupableOrderedDict(OrderedDict({'a': 'slovo'})),
        GroupableOrderedDict(OrderedDict({'a': 'internacionalismus'})),
        GroupableOrderedDict(OrderedDict({'a': 'neologismus'})),
        GroupableOrderedDict(OrderedDict({'a': 'lexikální sémantika'})),
        GroupableOrderedDict(OrderedDict({'a': 'pragmatika'})),
        GroupableOrderedDict(OrderedDict({'a': 'kultura'})),
        GroupableOrderedDict(OrderedDict({'a': 'politika'})),
        GroupableOrderedDict(OrderedDict({'a': 'zpravodajství'})),
        GroupableOrderedDict(OrderedDict({'a': 'deník'}))
    )


def test_split_keywords_2():
    keywords = (
        GroupableOrderedDict(OrderedDict({"a": "mladší školní věk - slovo"})),
        GroupableOrderedDict(OrderedDict({
            "a": "internacionalismus - neologismus - lexikální sémantika - pragmatika - kultura - "
                 "politika - "
                 "zpravodajství - deník"
        })),
    )
    res = split_keywords(keywords)
    assert res == (
        GroupableOrderedDict(OrderedDict({'a': 'mladší školní věk'})),
        GroupableOrderedDict(OrderedDict({'a': 'slovo'})),
        GroupableOrderedDict(OrderedDict({'a': 'internacionalismus'})),
        GroupableOrderedDict(OrderedDict({'a': 'neologismus'})),
        GroupableOrderedDict(OrderedDict({'a': 'lexikální sémantika'})),
        GroupableOrderedDict(OrderedDict({'a': 'pragmatika'})),
        GroupableOrderedDict(OrderedDict({'a': 'kultura'})),
        GroupableOrderedDict(OrderedDict({'a': 'politika'})),
        GroupableOrderedDict(OrderedDict({'a': 'zpravodajství'})),
        GroupableOrderedDict(OrderedDict({'a': 'deník'}))
    )


def test_get_ref():
    json_dict = {
        "uri": "http://psh.techlib.cz/skos/PSH2917",
        "@type": "Concept",
        "pshid": "PSH2917",
        "title": [
            {
                "lang": "cze",
                "value": "atomová hmotnost"
            },
            {
                "lang": "eng",
                "value": "atomic mass"
            }
        ],
        "baseurl": "http://psh.techlib.cz/skos/",
        "broader": "PSH2916",
        "related": [],
        "altTitle": [
            {
                "lang": "eng",
                "value": "atomic weight"
            }
        ],
        "modified": "2007-01-26T16:14:37",
        "narrower": [],
        "date_of_serialization": "2020-03-17 16:05:47.589116",
        "id": 11511,
        "slug": "PSH2917",
        "taxonomy": "subject",
        "path": "/psh/PSH2910/PSH2911/PSH2914/PSH2916/PSH2917",
        "links": {
            "self": "http://127.0.0.1:5000/taxonomies/subject/psh/PSH2910/PSH2911/PSH2914/PSH2916"
                    "/PSH2917/",
            "tree": "http://127.0.0.1:5000/taxonomies/subject/psh/PSH2910/PSH2911/PSH2914/PSH2916"
                    "/PSH2917/?drilldown=True",
            "parent": "http://127.0.0.1:5000/taxonomies/subject/psh/PSH2910/PSH2911/PSH2914"
                      "/PSH2916/",
            "parent_tree": "http://127.0.0.1:5000/taxonomies/subject/psh/PSH2910/PSH2911/PSH2914"
                           "/PSH2916/?drilldown=True"
        },
        "level": 6,
        "ancestors": [
            {
                "url": "https://psh.techlib.cz/skos/",
                "title": [
                    {
                        "lang": "cze",
                        "value": "Polytematický strukturovaný heslář"
                    },
                    {
                        "lang": "eng",
                        "value": "Polythematic Structured Subject Heading System"
                    }
                ],
                "level": 1,
                "slug": "psh"
            },
            {
                "uri": "http://psh.techlib.cz/skos/PSH2910",
                "@type": "Concept",
                "pshid": "PSH2910",
                "title": [
                    {
                        "lang": "cze",
                        "value": "fyzika"
                    },
                    {
                        "lang": "eng",
                        "value": "physics"
                    }
                ],
                "baseurl": "http://psh.techlib.cz/skos/",
                "broader": "",
                "related": [
                    "PSH8230"
                ],
                "altTitle": [],
                "modified": "2010-02-18T12:47:07",
                "narrower": [
                    "PSH2928",
                    "PSH2911",
                    "PSH3722",
                    "PSH3718",
                    "PSH3740",
                    "PSH3753",
                    "PSH3767",
                    "PSH3719",
                    "PSH13654",
                    "PSH3612",
                    "PSH3197",
                    "PSH3097",
                    "PSH3158",
                    "PSH3291",
                    "PSH3423",
                    "PSH3525",
                    "PSH3198",
                    "PSH3345",
                    "PSH3548",
                    "PSH3602",
                    "PSH3634",
                    "PSH3181"
                ],
                "level": 2,
                "slug": "PSH2910"
            },
            {
                "uri": "http://psh.techlib.cz/skos/PSH2911",
                "@type": "Concept",
                "pshid": "PSH2911",
                "title": [
                    {
                        "lang": "cze",
                        "value": "obecná fyzika"
                    },
                    {
                        "lang": "eng",
                        "value": "general physics"
                    }
                ],
                "baseurl": "http://psh.techlib.cz/skos/",
                "broader": "PSH2910",
                "related": [],
                "altTitle": [
                    {
                        "lang": "cze",
                        "value": "teoretická fyzika"
                    }
                ],
                "modified": "2007-01-26T16:14:37",
                "narrower": [
                    "PSH2926",
                    "PSH2924",
                    "PSH2925",
                    "PSH2912",
                    "PSH2914",
                    "PSH2927"
                ],
                "level": 3,
                "slug": "PSH2911"
            },
            {
                "uri": "http://psh.techlib.cz/skos/PSH2914",
                "@type": "Concept",
                "pshid": "PSH2914",
                "title": [
                    {
                        "lang": "cze",
                        "value": "fyzikální veličiny"
                    },
                    {
                        "lang": "eng",
                        "value": "physical quantities"
                    }
                ],
                "baseurl": "http://psh.techlib.cz/skos/",
                "broader": "PSH2911",
                "related": [],
                "altTitle": [
                    {
                        "lang": "cze",
                        "value": "bezrozměrné veličiny"
                    },
                    {
                        "lang": "cze",
                        "value": "fyzikální veličiny skalární"
                    },
                    {
                        "lang": "cze",
                        "value": "fyzikální veličiny vektorové"
                    },
                    {
                        "lang": "eng",
                        "value": "dimensionless quantities"
                    },
                    {
                        "lang": "eng",
                        "value": "scalar physical quantities"
                    },
                    {
                        "lang": "eng",
                        "value": "vector physical quantities"
                    }
                ],
                "modified": "2007-01-26T16:14:37",
                "narrower": [
                    "PSH2921",
                    "PSH2916",
                    "PSH2923",
                    "PSH2915",
                    "PSH2922",
                    "PSH2920",
                    "PSH2919"
                ],
                "level": 4,
                "slug": "PSH2914"
            },
            {
                "uri": "http://psh.techlib.cz/skos/PSH2916",
                "@type": "Concept",
                "pshid": "PSH2916",
                "title": [
                    {
                        "lang": "cze",
                        "value": "hmotnost"
                    },
                    {
                        "lang": "eng",
                        "value": "mass"
                    }
                ],
                "baseurl": "http://psh.techlib.cz/skos/",
                "broader": "PSH2914",
                "related": [],
                "altTitle": [
                    {
                        "lang": "cze",
                        "value": "váha"
                    }
                ],
                "modified": "2007-01-26T16:14:37",
                "narrower": [
                    "PSH2917",
                    "PSH2918"
                ],
                "level": 5,
                "slug": "PSH2916"
            }
        ]
    }
    ref = get_ref_es(json_dict)
    assert ref == {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH2917'}
