import pytest


@pytest.fixture
def grantor_filter_fix():
    return [{
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'descendants_count': 4.0,
                'id': 81903,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown'
                                   '=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101/?drilldown=True'
                },
                'path': '/N6101',
                'slug': 'N6101',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'descendants_count': 4.0,
                'id': 81900,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown'
                                   '=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B6101/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B6101/?drilldown=True'
                },
                'path': '/B6101',
                'slug': 'B6101',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'id': 82989,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown'
                                   '=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B6147/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B6147/?drilldown=True'
                },
                'path': '/B6147',
                'slug': 'B6147',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'descendants_count': 4.0,
                'id': 81905,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown'
                                   '=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/?drilldown=True'
                },
                'path': '/P6101',
                'slug': 'P6101',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'ancestors': [{
                                  'level': 1,
                                  'slug': 'N6101',
                                  'title': [{'lang': 'cze', 'value': 'Filozofie'}]
                              }],
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'grantor': [{
                                'faculty': 'Teologická fakulta',
                                'university': 'Jihočeská univerzita v Českých Budějovicích'
                            }],
                'id': 81904,
                'language': ['Česky'],
                'level': 2,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101'
                                   '/?drilldown=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101/6101T004/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/N6101/6101T004'
                            '/?drilldown=True'
                },
                'path': '/N6101/6101T004',
                'programme_type': 'Navazující magisterský',
                'slug': '6101T004',
                'study_duration': '2',
                'study_form': ['P'],
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'descendants_count': 2.0,
                'id': 82207,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown'
                                   '=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6147/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6147/?drilldown=True'
                },
                'path': '/P6147',
                'slug': 'P6147',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'id': 83542,
                'level': 1,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/?drilldown=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/M6101/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/M6101/?drilldown=True'
                },
                'path': '/M6101',
                'slug': 'M6101',
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            },
            {
                'aliases': ['Filozofie - Bohemistika',
                            'Filozofie - Teologie',
                            'NŠ-FIL',
                            'NŠ-HV-C, Filosofie pro děti'],
                'ancestors': [{
                                  'level': 1,
                                  'slug': 'P6101',
                                  'title': [{'lang': 'cze', 'value': 'Filozofie'}]
                              }],
                'date_of_serialization': '2020-03-19 14:56:56.882858',
                'grantor': [{
                                'faculty': 'Teologická fakulta',
                                'university': 'Jihočeská univerzita v Českých Budějovicích'
                            }],
                'id': 81906,
                'language': ['Česky'],
                'level': 2,
                'links': {
                    'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/',
                    'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/?drilldown=True',
                    'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/6101V004/',
                    'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/P6101/6101V004/?drilldown=True'
                },
                'path': '/P6101/6101V004',
                'programme_type': 'Doktorský',
                'slug': '6101V004',
                'study_duration': '4',
                'study_form': ['K', 'P'],
                'taxonomy': 'studyfields',
                'title': [{'lang': 'cze', 'value': 'Filozofie'}]
            }]

@pytest.fixture
def doc_filter_fix():
    return [
        {
            'ancestors': [
                {
                    'level': 1,
                    'slug': 'others',
                    'title': [
                        {
                            'lang': 'cze',
                            'value': 'Obory bez přiřazeného programu'
                        },
                        {
                            'lang': 'eng',
                            'value': 'Field without assigned study '
                                     'programme'
                        }
                    ]
                }
            ],
            'date_of_serialization': '2020-03-19 14:56:56.882858',
            'grantor': [
                {
                    'faculty': '',
                    'university': ''
                }
            ],
            'id': 85945,
            'language': [''],
            'level': 2,
            'links': {
                'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/others/',
                'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/others'
                               '/?drilldown=True',
                'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/others/5342R001/',
                'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/others/5342R001'
                        '/?drilldown=True'
            },
            'path': '/others/5342R001',
            'slug': '5342R001',
            'study_form': [''],
            'taxonomy': 'studyfields',
            'title': [{'lang': None, 'value': 'Arteterapie'}]
        },
        {
            'ancestors': [
                {
                    'level': 1,
                    'slug': 'B7701',
                    'title': [{'lang': 'cze', 'value': 'Psychologie'}]
                }
            ],
            'date_of_serialization': '2020-03-19 14:56:56.882858',
            'grantor': [
                {
                    'faculty': 'Pedagogická fakulta',
                    'university': 'Jihočeská univerzita v Českých Budějovicích'
                }
            ],
            'id': 81747,
            'language': ['Česky'],
            'level': 2,
            'links': {
                'parent': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B7701/',
                'parent_tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B7701'
                               '/?drilldown=True',
                'self': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B7701/7701R012/',
                'tree': 'http://127.0.0.1:5000/api/taxonomies/studyfields/B7701/7701R012'
                        '/?drilldown=True'
            },
            'path': '/B7701/7701R012',
            'programme_type': 'Bakalářský',
            'slug': '7701R012',
            'study_duration': '3',
            'study_form': ['K'],
            'taxonomy': 'studyfields',
            'title': [
                {
                    'lang': 'cze',
                    'value': 'Arteterapie'
                }
            ]
        }
    ]