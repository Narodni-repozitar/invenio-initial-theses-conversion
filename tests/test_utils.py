from collections import OrderedDict

from dojson.utils import GroupableOrderedDict

from invenio_initial_theses_conversion.utils import split_keywords


def test_split_keywords_1():
    keywords = (
        GroupableOrderedDict(OrderedDict({"a": "mladší školní věk - slovo"})),
        GroupableOrderedDict(OrderedDict({
            "a": "internacionalismus|neologismus|lexikální sémantika|pragmatika|kultura|politika|zpravodajství|deník"})),
    )
    res = split_keywords(keywords)
    pass


def test_split_keywords_2():
    keywords = (
        GroupableOrderedDict(OrderedDict({"a": "mladší školní věk - slovo"})),
        GroupableOrderedDict(OrderedDict({
            "a": "internacionalismus|neologismus|lexikální sémantika|pragmatika|kultura|politika|zpravodajství|deník"})),
    )
    split_keywords(keywords)
