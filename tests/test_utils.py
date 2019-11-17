from collections import OrderedDict

from dojson.utils import GroupableOrderedDict

from invenio_initial_theses_conversion.utils import fix_grantor, split_keywords


def test_split_keywords_1():
    keywords = (
        GroupableOrderedDict(OrderedDict({"a": "mladší školní věk - slovo"})),
        GroupableOrderedDict(OrderedDict({
            "a": "internacionalismus|neologismus|lexikální sémantika|pragmatika|kultura|politika|zpravodajství|deník"})),
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
            "a": "internacionalismus - neologismus - lexikální sémantika - pragmatika - kultura - politika - "
                 "zpravodajství - deník"})),
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


# def test_fix_grantor():
#     data = GroupableOrderedDict(
#         (
#             ('502__', GroupableOrderedDict((('a', '2019-07-10'), ('b', 'Bc.'),
#                                             ('c', 'JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH'), ('g', 'Bachelor')))),
#         )
#     )
#     fix_grantor(data)
