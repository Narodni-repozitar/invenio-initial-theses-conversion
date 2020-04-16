# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the API application."""

from __future__ import absolute_import, print_function

import json
import os
import pathlib
import shutil
import tempfile

import pytest
from dojson import Overdo
from dojson.contrib.marc21.utils import create_record, split_stream
from flask import Flask
from flask_taxonomies import FlaskTaxonomies
from flask_taxonomies.views import blueprint as taxonomies_blueprint
from invenio_app.factory import create_api
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch
from sqlalchemy_utils import create_database, database_exists

from flask_taxonomies_es import FlaskTaxonomiesES


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="oarepo", pw="oarepo",
                                                                  url="127.0.0.1",
                                                                  db="oarepo")),
        SERVER_NAME='localhost',
    )
    InvenioJSONSchemas(app)
    InvenioRecords(app)
    InvenioSearch(app)
    InvenioDB(app)
    FlaskTaxonomies(app)
    FlaskTaxonomiesES(app)
    with app.app_context():
        app.register_blueprint(taxonomies_blueprint)
        yield app

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    yield db_


@pytest.fixture
def overdo_instance():
    overdo = Overdo()
    return overdo


# @pytest.yield_fixture()
def results_fix(results):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, "xml_files/vskp_test2.xml")
    array = [create_record(data) for data in
             split_stream(
                 open(
                     path,
                     'rb'))]
    for idx, field in enumerate(array):
        yield field, results[idx]


def grantors():
    dir = pathlib.Path(__file__).parent.absolute()
    path = dir / "data" / "grantors.json"
    with open(str(path), "r") as f:
        array_ = json.load(f)
        return [_["7102_"] for _ in array_]


# @pytest.fixture
def results():
    return [
        {
            'contributor': [],
            'identifier': [{'type': 'originalRecord', 'value': 'http://www.jcu.cz/vskp/55233'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-396593'},
                           {'type': 'originalOAI', 'value': 'repository/55233'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:396593'},
                           {'type': 'catalogue', 'value': '55233'}],
            'creator': [{'name': 'KNĚZOVÁ, Michaela'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/7701R012'}],
            'abstract': [{
                'name': 'Práce pojednává o výtvarném vzdělávání na základní škole a o jeho '
                        'propojení s\n                arteterapií. Uvádí se požadavky na žáka a '
                        'stanovení úspěšnosti, o fenoménu výtvarného projevu a jeho\n             '
                        '   znacích v dětském projevu, komunikaci ve výtvarném projevu a ve '
                        'výchově, imaginaci, vývoji výtvarného\n                projevu a '
                        'kognitivním vývoji dítěte a krizi ve výtvarném projevu. Dále pokračuje '
                        'seznámením s\n                východisky, přístupy a metodami '
                        'arteterapie. Podrobně se zabývá projektivně intervenční arteterapií,'
                        '\n                která je založena na výtvarném ontogenetickém pojetí, '
                        'její metodikou a metodikou používanou při vedení\n                ve '
                        'výtvarné výchově. Stručně pojednává o artefiletice, která je jedním z '
                        'přístupů ve výtvarném\n                vzdělávání. Dále v praktické '
                        'části seznamuje s konkrétním využitím arteterapie s žáky během výuky\n   '
                        '             výtvarné výchovy formou kazuistiky a popisu výtvarné '
                        'činnosti. Popsána jsou témata zadávaná při\n                výtvarném '
                        'vedení a též různé alternativy metodického vedení a hodnocení posunu ve '
                        'výtvarném vývoji.',
                'lang': 'cze'
            },
                {
                    'name': "The thesis deals with art education at primary school and its "
                            "connection with art\n                therapy. Requirements for the "
                            "pupil and the determination of success, the phenomenon of artistic\n "
                            "               ex-pression and its features in children's "
                            "expression, communication in art expression and in\n                "
                            "edu-cation, imagination, development of artistic expression and "
                            "cognitive development of the child and\n                crisis in "
                            "artistic expression are mentioned. It also continues with the "
                            "introduction to the approaches,\n                approaches and "
                            "methods of art therapy. It deals in detail with the "
                            "design-interventional art therapy,\n                which is based "
                            "on the art ontogenetic conception, its methodology and methodology "
                            "used in leading in art\n                education. It briefly "
                            "discusses artefiletics, which is one of the approaches in art "
                            "education.\n                Furthermore, in the practical part "
                            "introduces the specific use of art therapy with pupils during the\n  "
                            "              education of art education in the form of case studies "
                            "and description of art activities. Described are\n                "
                            "the topics given during the artistic leadership as well as various "
                            "alternatives of methodological\n                guidance and "
                            "evaluation of the shift in visual development.",
                    'lang': 'eng'
                }],
            'keywords': [{'name': 'mladší školní věk', 'lang': 'cze'},
                         {'lang': 'cze', 'name': 'výtvarná výchova'},
                         {'name': 'vývoj zobrazování', 'lang': 'cze'},
                         {'name': 'výtvarný projev', 'lang': 'cze'},
                         {'name': 'projektivně intervenční arteterapie', 'lang': 'cze'},
                         {'name': 'arteterapie s dětmi', 'lang': 'cze'},
                         {'name': 'Junger school age', 'lang': 'eng'},
                         {'name': 'Art Education', 'lang': 'eng'},
                         {'name': 'developing of imaging', 'lang': 'eng'},
                         {'name': 'artistic expression', 'lang': 'eng'},
                         {'name': 'projective interpretative art therapy', 'lang': 'eng'},
                         {'name': 'art therapy with children', 'lang': 'eng'}], 'id': '396593',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider'
                        '/jihoceska_univerzita_v_ceskych_budejovicich'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/bakalarske_prace'},
            'degreeGrantor': [
                {'$ref': 'http://127.0.0.1:5000/api/taxonomies/universities/60076658'}],
            'title': [
                {
                    'name': 'Využití arteterapeutických přístupů při výuce výtvarné výchovy na '
                            '1.stupni ZŠ',
                    'lang': 'cze'
                }],
            'accessibility': [
                {'name': 'Plný text je dostupný v digitálním repozitáři JČU.', 'lang': 'cze'},
                {
                    'name': 'Fulltext is available in the Digital Repository of University of '
                            'South Bohemia.',
                    'lang': 'eng'
                }], 'extent': '90 s. (123 325 znaků)', 'dateAccepted': '2019-07-10',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Hrdlička, Pavel', 'role': 'advisor'},
                            {'name': 'Markéta, Markéta', 'role': 'referee'}],
            'identifier': [{
                'type': 'originalRecord',
                'value': 'https://is.czu.cz/zp/index.pl?podrobnosti_zp=200082'
            },
                {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-315989'},
                {'type': 'originalOAI', 'value': 'oai:czu.cz:vskp/d200082'},
                {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:315989'}],
            'creator': [{'name': 'Kocová, Petra'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/6208T094'}],
            'abstract': [{
                'name': 'Předmětem diplomové práce je problematika nezaměstnanosti osob starších '
                        '50 let v České\n                republice. Na základě stanovených '
                        'hypotéz zjišťuje příčiny nezaměstnanosti zkoumané věkové skupiny z\n     '
                        '           pohledu zaměstnavatelů.\n                Diplomová práce '
                        'nejprve seznamuje s teoretickými východisky, které jsou spojené s '
                        'nezaměstnaností a\n                jejími souvislostmi, trhem práce i '
                        'diskriminací na trhu práce. Zmiňuje také pohled z druhé strany trhu\n    '
                        '            práce a uvádí informace ohledně náboru a výběru nových '
                        'zaměstnanců do společnosti. V další části je\n                proveden '
                        'empirický výzkum, poté následuje diskuze a vyhodnocení, které potvrdí či '
                        'vyvrátí stanovené\n                hypotézy a tím odpoví na cíl práce, '
                        'kterým jsou příčiny nezaměstnanosti zkoumané rizikové skupiny osob\n     '
                        '           starších 50 let.',
                'lang': 'cze'
            },
                {
                    'name': 'The subject of the thesis is the issue of unemployment of people '
                            'over 50 years in the\n                Czech Republic. On the basic '
                            'of thypotheses it determines the causes of unemyployment surveyed '
                            'age\n                groups from the perspective of employers. The '
                            'thesis first introduces the theoretical bases that are\n             '
                            '   associated with unemployment and its context, labor market and '
                            'labor market discrimination. Also\n                mentions the view '
                            'from the other side of the labor market, and provides informaiton '
                            'regarding the\n                recruitment and selection of new '
                            'employees into the company. The next part is done empirical '
                            'research,\n                followed by discussion and evaluation to '
                            'confirm or disprove the hypothesis and thus responds to the\n        '
                            '        aim, which are the causes of unemployment examined risk '
                            'group of people over 50 years.',
                    'lang': 'eng'
                }],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH1264'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH1465'}],
            'keywords': [{'name': 'rizikové skupiny', 'lang': 'cze'},
                         {'name': 'výběrové řízení', 'lang': 'cze'}],
            'id': '315989', 'provider': {
            '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/ceska_zemedelska_univerzita'
        },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60460709_no_faculty_no_department'
            }],
            'title': [
                {
                    'name': 'Analýza příčin nezaměstnanosti věkové skupiny nad 50 let z pohledu '
                            'zaměstnavatele',
                    'lang': 'cze'
                }],
            'accessibility': [
                {'name': 'Dostupné registrovaným uživatelům v repozitáři ČZU.', 'lang': 'cze'},
                {'name': 'Available to registered users in the CZU repository.', 'lang': 'eng'}],
            'dateAccepted': '2017-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Tichý, Vladimír', 'role': 'advisor'},
                            {'name': 'Willi, Barbara', 'role': 'referee'},
                            {'name': 'Bažantová, Ivana', 'role': 'referee'}],
            'identifier': [{'type': 'originalRecord', 'value': 'http://hdl.handle.net/10318/5091'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-79353'},
                           {'type': 'originalOAI', 'value': 'oai:dspace.amu.cz:10318/5091'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:79353'}],
            'creator': [{'name': 'Vendl, Lukáš'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/8201V095'}],
            'abstract': [{
                'name': 'Problematika tzv. staré hudby je dnes velmi skloňovaným odvětvím v '
                        'oblasti hudební\n                interpretace, hudební teorie a hudební '
                        'vědy. Pro adekvátní porozumění a uchopení hudebního textu\n              '
                        '  potřebuje dnešní interpret rozsáhlé teoretické povědomí. Hudebně '
                        'teoretická východiska, jež stála v\n                pozadí tvorby autorů '
                        '17. století, formovala a předdefinovala možná řešení detailů hudební '
                        'kompozice.\n                Teoretické nástroje, které nám poskytuje '
                        'moderní nauka o kontrapunktu, o harmonii a hudební tektonice,\n          '
                        '      nemohou odhalit jemné odstíny tehdejšího hudebního výraziva.\n     '
                        '           V prvním oddíle je stručně nastíněno pozadí vzniku hudby pro '
                        'klávesové nástroje v 17. století a popsán\n                charakter a '
                        'oblasti společenské poptávky a souvislosti vedoucí ke vzniku škály '
                        'žánrů.\n                Druhý oddíl probírá v jednotlivých kapitolách '
                        'nejpodstatnější informace o stavu či vývoji různých\n                '
                        'oblastí hudební teorie: tónový materiál ? mody, církevní a varhanické '
                        'tóniny, nauka o klauzulích, vývoj\n                kontrapunktu a teorie '
                        'fugy, rétorické dispositio jako nevyslovený obecný formální rámec tzv. '
                        '?volných?,\n                fantazijních forem, preludií, toccat; praxe '
                        'používání rétorických figur.\n                Další oddíl podává přehled '
                        'technických předpokladů dobových nástrojů a souvislost s výskytem '
                        'určitých\n                hudebních obratů, souzvuků apod. v literatuře. '
                        'Je popsán vliv ladění a temperatury, zejména hojně\n                '
                        'rozšířené středotónové. Hojné používání krátké, lomené a zkrácené oktávy '
                        'vysvětluje výskyt souzvuků a\n                postupů na moderní '
                        'klaviatuře nesnadno realizovatelných. Více manuálů na jednom nástroji a '
                        'klaviatura\n                dělená na bas a diskant umožňuje a '
                        'předpokládá speciální druhy sazby.\n                Ve čtvrtém oddíle '
                        'následuje detailnější analýza několika skladeb různého typu regionálního '
                        'a časového.\n                Na cyklu ricercarů G. M. Trabaciho je '
                        'zkoumán vliv modality na hudební formu. Frescobaldiho toccaty\n          '
                        '      stojí na počátku obrovského vývoje tvorby pro klávesové nástroje a '
                        'je studijním materiálem pro\n                skladatele bezmála 3 '
                        'následujících staletí. Analyzována je Toccata prima ze sbírky Il secondo '
                        'libro di\n                toccate (1627). Vrchol varhanní tvorby najdeme '
                        'v 17. stol. bezpochyby v oblasti severního Německa, a zde\n              '
                        '  především v díle D. Buxtehude. Následuje rozbor Preambula BuxWV 152.\n '
                        '               Závěrem je zařazena úvaha o významu zkoumání daných '
                        'témat, zda jde o pouhé odkrývání dnes již\n                irelevantních '
                        'souvislostí, nebo zda lze najít inspiraci pro interpretaci děl starších '
                        'epoch, která dnes\n                již neodmyslitelně patří k současnému '
                        'hudebnímu dění.',
                'lang': 'cze'
            },
                {
                    'name': 'Early Music, its history, theory and practice, has become a '
                            'vigorously discussed theme in\n                the field of '
                            'musicology. To be able to grasp a musical text adequately, '
                            'a contemporary performer\n                requires an extensive '
                            'theoretical knowledge. The theoretical background lying behind the '
                            'origins of the\n                seventeenth-century musical material '
                            'was essential in the formation and pre-definition of the possible\n  '
                            '              solutions of the details of compositional techniques '
                            'and approaches of the period. The theoretical\n                '
                            'methods employed by the modern disciplines of counterpoint and '
                            'harmony and the tectonics of music are\n                not '
                            'sufficient if we wish to examine the nuances of the musical '
                            'phraseology of those times.\n                Offering a short '
                            'introduction into the environment in which keyboard music of the '
                            'seventeenth century\n                was originating, the first '
                            'section looks into the character and areas of social demand which '
                            'resulted in\n                a broad range of musical genres.\n      '
                            '          The individual chapters of the following section touch '
                            'upon the key facts about the state and\n                development '
                            'of different areas of music theory, such as tonal material ? modes, '
                            'Church and organ keys,\n                the doctrine of clauses, '
                            'the development of counterpoint and the theory of the fugue, '
                            'the rhetorical\n                dispositio as the unpronounced, '
                            'general formal frame of the so-called ?free?, fantasia forms, '
                            'preludes\n                and toccatas; the application of figures '
                            'of speech.\n                The third section brings a survey of the '
                            'technical conditions which were formative in the case of period\n    '
                            '            musical instruments and traces down some of the '
                            'occurrences of specific musical terms and consonances in\n           '
                            '     literature. One of the chapters tracks down the influence of '
                            'tuning and tempering systems, especially of\n                the '
                            'widespread mean-tone tuning system. The profuse usage of the short, '
                            'broken and shortened octave\n                accounts for the '
                            'consonances and sequences which are difficult to perform on modern '
                            'keyboards. Multiple\n                manuals and the division of the '
                            'keyboard into the bass and the discant part presupposed a special '
                            'kind\n                of typesetting.\n                In the fourth '
                            'section I propose an analysis of several compositions coming from '
                            'various places and\n                decades. In an analysis of the '
                            'cycle of ricercares by G. M. Trabaci I inspect the influence of '
                            'modality\n                on musical form. Standing at the beginning '
                            'of the massive development of composition for keyboard\n             '
                            '   instruments, Frecobaldi?s toccatas would have been consulted as a '
                            'study material by composers throughout\n                the '
                            'following three centuries at least. Among others, I analyse Toccata '
                            'prima from Il secondo libro di\n                toccate (1627). The '
                            'peak of the seventeenth century organ production is undoubtedly to '
                            'be found in the\n                area of Northern Germany, namely in '
                            'the work of D. Buxtehude. The section is closed by an analysis of\n  '
                            '              his Preambulum BuxWV 152.\n                By way of '
                            'conclusion I speculate about the possible values of studying and '
                            'theorizing of such issues: if\n                they can only result '
                            'in excavation of anachronic circumstances, irrelevant to our time, '
                            'or if they can\n                provide a source of inspiration for '
                            'the interpretation of early music which has become an inseparable\n  '
                            '              part of contemporary musical scene and culture.',
                    'lang': 'eng'
                }],
            'id': '79353', 'provider': {
            '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/akademie_muzickych_umeni_v_praze'
        },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/disertacni_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/61384984_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Hudebně teoretická východiska nechorálních skladeb pro '
                        'klávesové nástroje v 17. stol.',
                'lang': 'cze'
            }],
            'accessibility': [{
                'name': 'Dostupné registrovaným uživatelům v digitálním '
                        'repozitáři AMU.',
                'lang': 'cze'
            }, {
                'name': 'Available to registered users in the Digital '
                        'Repository of Academy of Performing Arts.',
                'lang': 'eng'
            }], 'dateAccepted': '2010-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [],
            'identifier': [{'type': 'originalRecord', 'value': 'http://www.jcu.cz/vskp/22464'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-180713'},
                           {'type': 'originalOAI', 'value': 'repository/22464'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:180713'},
                           {'type': 'catalogue', 'value': '22464'}],
            'creator': [{'name': 'KREJČOVÁ, Kateřina'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/7503T094'},
                           {'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/7503T111'}],
            'abstract': [{
                'name': 'Diplomová práce se zabývá analýzou projevu španělsky mluvících '
                        'adolescentů na\n                internetových diskuzních fórech. '
                        'Teoretická část se věnuje zejména problematice dichotomií\n              '
                        '  mluvenost/psanost a hovorovost/formálnost, které se nemalou měrou '
                        'podílejí na výsledné podobě jazyka na\n                internetu. '
                        'Popisuje také obecné rysy jazyka užívaného v internetovém prostředí se '
                        'zaměřením na\n                španělštinu a na adolescentní uživatele. '
                        'Praktická část analyzuje v rovině grafické, morfosyntaktické,\n          '
                        '      sémantické a pragmatické jazykový vzorek sesbíraný na '
                        'internetových diskuzních fórech.',
                'lang': 'cze'
            },
                {
                    'name': 'The diploma thesis folows up the analysis of the language of spanish '
                            'speaking adolescents\n                acros online discussion '
                            'forums. The theoretic section mainly pursues the issues of the '
                            'oral/written and\n                colloquial/formal dichotomies '
                            'which takes an important part in the resultant form of the language '
                            'used\n                on the internet. It also describes the general '
                            'features of language, used on the internet, focusing\n               '
                            ' spanish and adolescent users. The practical section analyses the '
                            'graphic, morphosyntactical, semantic\n                and pragmatic '
                            'level of the language sample found on the internet discussion forums.',
                    'lang': 'eng'
                }],
            'keywords': [{'name': 'mluvenost/psanost', 'lang': 'cze'},
                         {'name': 'hovorovost/formálnost', 'lang': 'cze'},
                         {'name': 'jazyk na internetu', 'lang': 'cze'},
                         {'name': 'komunikace v období adolescence', 'lang': 'cze'},
                         {'name': 'the oral/written dichotomie', 'lang': 'eng'},
                         {'name': 'the colloquial/formal dichotomie', 'lang': 'eng'},
                         {'name': 'language on the internet', 'lang': 'eng'},
                         {'name': 'communication in adolescence', 'lang': 'eng'}], 'id': '180713',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider'
                        '/jihoceska_univerzita_v_ceskych_budejovicich'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60076658_no_faculty_no_department'
            }],
            'title': [
                {'name': 'Analýza španělštiny v internetových diskuzních fórech', 'lang': 'cze'}],
            'accessibility': [
                {'name': 'Plný text je dostupný v digitálním repozitáři JČU.', 'lang': 'cze'},
                {
                    'name': 'Fulltext is available in the Digital Repository of University of '
                            'South Bohemia.',
                    'lang': 'eng'
                }], 'extent': '102 stran', 'dateAccepted': '2014-12-19',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Bič, Josef', 'role': 'advisor'},
                            {'name': 'Hnát, Pavel', 'role': 'referee'}],
            'identifier': [{'type': 'originalRecord', 'value': 'http://www.vse.cz/vskp/eid/68845'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-361615'},
                           {'type': 'originalOAI', 'value': 'oai:vse.cz:vskp/68845'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:361615'}],
            'creator': [{'name': 'Stropkaiová, Aneta'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/6210T010'}],
            'abstract': [{
                'name': 'Silicon Valley a společnosti seskupeny kolem Massachusettského '
                        'technologického institutu\n                jsou známé jako světové '
                        'centra aktivit investorů rizikového kapitálu. Právě tyto oblasti s '
                        'množstvím\n                start-upů a firem podílejících se na výzkumu '
                        'a vývoji jsou dnes hodnoceny jako území s nejvyšší\n                '
                        'koncentrací inovací na světě a společnosti jako Apple, Facebook, '
                        'Microsoft či Google sídlící v Silicon\n                Valley, '
                        'patří mezi nejinovativnější a nejdůležitější společnosti generace. '
                        'Počínaje z Windows až přes\n                FedEx, technologie zrozené v '
                        'útrobách firem financovaných rizikovým kapitálem, změnily zásadním '
                        'způsobem\n                náš svět. Cílem mé diplomové práce je '
                        'identifikovat vztah mezi rizikovým kapitálem, inovacemi a\n              '
                        '  ekonomickou výkonnosti na příkladu USA. V první kapitole vymezuje '
                        'pojem rizikový kapitál, vysvětluji jak\n                probíhá proces '
                        'investování rizikového kapitálu, a které subjekty se tohoto procesu '
                        'účastní. Ve druhé\n                kapitole hodnotím úlohu rizikového '
                        'kapitálu v americké ekonomice. Dále zkoumám jakým způsobem přispívá\n    '
                        '            rizikový kapitál k zakládání a rozvoji inovativních firem. '
                        'Ve třetí kapitole aplikuji závěry výzkumů na\n                příkladu '
                        'konkrétní americké společnosti, která splňuje 2 podmínky a to, '
                        'že je financována rizikovým\n                kapitálem a má velký '
                        'inovační potenciál. Na praktickém příkladu tak ověřuji vztah mezi '
                        'rizikovým\n                kapitálem, inovacemi a ekonomickou výkonností '
                        'země.',
                'lang': 'cze'
            },
                {
                    'name': 'Silicon Valley and companies grouped around MIT are known as world '
                            'centres for investor\n                activity for venture capital. '
                            'These areas with many start-ups and companies participating on R&D '
                            'are\n                today ranked as regions with highest '
                            'concentration of innovations in the world and companies such as\n    '
                            '            Apple, Facebook, Microsoft or Google who are based in '
                            'Silicon Valley, belong among the most innovative\n                '
                            'and most important companies of our generation. From Windows to '
                            'FedEx, technologies created within the\n                companies '
                            'financed by venture capital, changed our world. The purpose of my '
                            'diploma thesis is identify\n                relationship between '
                            'venture capital, innovations and economic productivity on example of '
                            'USA. In first\n                chapter I define the term venture '
                            'capital, explain how the process of investing venture capital is\n   '
                            '             happening, and which subjects are involved in the '
                            'process. In second chapter I evaluate the role of\n                '
                            'venture capital in American economy. I´m also researching in what '
                            'way venture capital is contributing\n                with creation '
                            'and development of innovatory companies. In third chapter I apply '
                            'conclusions of my\n                findings on an example of '
                            'specific American company, which fulfills two conditions; it is '
                            'financed by\n                venture capital and has high innovation '
                            'potential. On practical example I verify the relationship\n          '
                            '      between venture capital, innovations and economic productivity '
                            'of country.',
                    'lang': 'eng'
                },
                {
                    'name': 'Sillicon Valley a spoločnosti zoskupené okolo Massachutského '
                            'technologického inštitútu sú\n                známe ako svetové '
                            'centrá aktivít investorov rizikového kapitálu. Práve tieto oblasti s '
                            'množstvom\n                start-upov a firiem podieľajúcich sa na '
                            'výskume a vývoji sú dnes hodnotené ako územia s najvyššou\n          '
                            '      koncentráciou inovácií na svete a spoločnosti ako Apple, '
                            'Facebook, Microsoft či Google sídliace v\n                Sillicon '
                            'Valley, patria medzi najinovatívnejšie a najdôležitejšie spoločnosti '
                            'generácie. Počínajuc\n                Windowsom až cez FedEx, '
                            'technológie zrodené v útrobach firiem financovaných rizikovým '
                            'kapitálom, zmenili\n                zásadným spôsobom náš svet. '
                            'Cieľom mojej diplomovej práce je identifikovať vzťah medzi '
                            'rizikovým\n                kapitálom, inováciami a ekonomickou '
                            'výkonnosťou na príklade USA. V prvej kapitole vymedzujem pojem\n     '
                            '           rizikový kapitál, vysvetľujem ako prebieha proces '
                            'investovania rizikového kapitálu, a ktoré subjekty sa\n              '
                            '  ho zúčastňujú. V druhej kapitole hodnotím úlohu rizikového '
                            'kapitálu v americkej ekonomike. Ďalej skúmam\n                akým '
                            'spôsobom prispieva rizikový kapitál k zakladaniu a rozvoju '
                            'inovatívnych firiem. V tretej kapitole\n                aplikujem '
                            'závery výskumov na príklade konkrétnej americkej spoločnosti, '
                            'ktorá spĺňa 2 podmienky a to, že\n                je financovaná '
                            'rizikovým kapitálom a má veľký inovačný potenciál. Na praktickom '
                            'príklade tak overujem\n                vzťah medzi rizikovým '
                            'kapitálom, inováciami a ekonomickou výkonnosťou krajiny.',
                    'lang': 'slo'
                }],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH12002'}],
            'keywords': [{'name': 'USA', 'lang': 'eng'}, {'name': 'innovation', 'lang': 'eng'},
                         {'name': 'economic growth', 'lang': 'eng'},
                         {'name': 'venture capital', 'lang': 'eng'},
                         {'name': 'USA', 'lang': 'cze'},
                         {'name': 'rizikový kapitál', 'lang': 'cze'},
                         {'name': 'ekonomická výkonnost', 'lang': 'cze'}], 'id': '361615',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider'
                        '/vysoka_skola_ekonomicka_v_praze'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/61384399_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Podpora inovácií v USA prostredníctvom rizikového kapitálu',
                'lang': 'slo'
            }],
            'accessibility': [{'name': 'Dostupné v digitálním repozitáři VŠE.', 'lang': 'cze'},
                              {
                                  'name': 'Available in the digital repository of the University '
                                          'of Economics, Prague.',
                                  'lang': 'eng'
                              }], 'dateAccepted': '2017-06-02',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/slo'}]
        },
        {
            'contributor': [{'name': 'Fiedler, Jiří', 'role': 'advisor'},
                            {'name': 'Horáková, Jana', 'role': 'referee'}],
            'identifier': [{
                'type': 'originalRecord',
                'value': 'https://is.czu.cz/zp/index.pl?podrobnosti_zp=205103'
            },
                {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-316011'},
                {'type': 'originalOAI', 'value': 'oai:czu.cz:vskp/b205103'},
                {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:316011'}],
            'creator': [{'name': 'Jirát, Tomáš'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/6208R076'}],
            'abstract': [{
                'name': 'Tato bakalářská práce se zabývá termínem motivace a možností jejího '
                        'využití při vedení\n                lidí. Práce je složena ze dvou '
                        'hlavních částí. První část se nazývá literární rešerše a vysvětluje\n    '
                        '            veškeré informace, které jsou potřeba pro pochopení daného '
                        'tématu. Literární rešerše poskytuje informace\n                o vedení '
                        'lidí, motivaci, manažerech a jejich funkcích a také o motivačních '
                        'teoriích. Dále vysvětluje\n                pojmy jako stimul, '
                        'motiv a poruchy motivace. Druhá část bakalářské práce je praktická. '
                        'Snaží se potvrdit\n                teoretické poznatky v praxi. Popisuje '
                        'vybrané společnosti a pět zkušených vedoucích pracovníků, kteří v\n      '
                        '          daných společnostech pracují. Manažeři dostali za úkol '
                        'zodpovědět jedenáct otevřených otázek na téma\n                motivace '
                        'jako způsob vedení lidí. Jelikož jde o manažery na různých pozicích a z '
                        'různých společností,\n                jejich odpovědi jsou mezi sebou '
                        'porovnány a okomentovány. Závěr této práce je vyvozen z porovnání\n      '
                        '          teoretických poznatků se zkušenostmi dotazovaných manažerů z '
                        'praxe.',
                'lang': 'cze'
            },
                {
                    'name': 'This thesis deals with the concept of motivation as a leadership for '
                            'its use in people\n                management. The work is contains '
                            'two main parts. The first part is called a literature review and\n   '
                            '             describe all the information that is needed for an '
                            'understanding of the topic. Literature research\n                '
                            'provides information on leadership, motivation, managers, and their '
                            'functions and also about\n                motivational theories. It '
                            'also explains the concepts like stimulus, motive and motivation '
                            'disorders. The\n                second part is practical. It is '
                            'trying to confirm the theoretical knowledge in practice. Describes\n '
                            '               selected companies and five experienced managers who '
                            'work in these companies. Managers were asked to\n                '
                            'answer a dozen open questions on the subject of motivation as a way '
                            'of leading people. Since it is\n                managers at '
                            'different positions and from different companies, their answers are '
                            'compared with each other\n                and commented. The summary '
                            'is drawn from a comparison of theoretical knowledge with the '
                            'experience of\n                managers.',
                    'lang': 'eng'
                }],
            'keywords': [{'name': 'Management', 'lang': 'cze'}, {'name': 'Motivace', 'lang': 'cze'},
                         {'name': 'Stimuly', 'lang': 'cze'}], 'id': '316011',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/ceska_zemedelska_univerzita'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/bakalarske_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60460709_no_faculty_no_department'
            }],
            'title': [{'name': 'Motivace jako způsob vedení lidí', 'lang': 'cze'}],
            'accessibility': [
                {'name': 'Dostupné registrovaným uživatelům v repozitáři ČZU.', 'lang': 'cze'},
                {'name': 'Available to registered users in the CZU repository.', 'lang': 'eng'}],
            'dateAccepted': '2017-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [],
            'identifier': [{'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-363443'},
                           {'type': 'originalOAI', 'value': 'oai:oai_provider.mendelu.cz:164101'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:363443'}],
            'creator': [{'name': 'Tunys, Pavel'}],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH1658'}],
            'keywords': [{'name': 'ekologické problémy', 'lang': 'cze'},
                         {'name': 'ekologické poplatky', 'lang': 'cze'},
                         {'name': 'ekologická daň', 'lang': 'cze'}], 'id': '363443',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/mendelova_univerzita_v_brne'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'degreeGrantor': [
                {'$ref': 'http://127.0.0.1:5000/api/taxonomies/universities/43110_no_department'}],
            'title': [{
                'name': 'Vybrané problémy ekologické analýzy fiskálních nástrojů '
                        'státního rozpočtu',
                'lang': 'cze'
            }],
            'accessibility': [
                {
                    'name': 'Dostupné registrovaným uživatelům v knihovně Mendelovy univerzity v '
                            'Brně.',
                    'lang': 'cze'
                },
                {
                    'name': 'Available to registered users in the Library of Mendel University.',
                    'lang': 'eng'
                }],
            'extent': '45 listů', 'dateAccepted': '1994-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Čeňková, Jana', 'role': 'advisor'},
                            {'name': 'Malý, Radek', 'role': 'referee'}],
            'identifier': [
                {'type': 'originalRecord', 'value': 'http://hdl.handle.net/20.500.11956/107892'},
                {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-398853'},
                {'type': 'originalOAI', 'value': 'oai:dspace.cuni.cz:20.500.11956/107892'},
                {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:398853'}],
            'creator': [{'name': 'Kubiková, Karolína'}], 'accessRights': 'open', 'abstract': [{
            'name': 'This Master Thesis is focused on analysis of media response to editions '
                    'Fresh and Raketa of publishing\n                house Labyrint in the '
                    'context of history of publishing practice in the Czech Republic in the '
                    'nineties.\n                It also discusses contemporary literature for '
                    'children and youth. Thesis studies critical media response\n                '
                    'to three particular books from studied editions Tajemství oblázkové hory by '
                    'Bára Dočkalová, Robinson by\n                Petr Sís and Plyš by Michal '
                    'Hvorecký. Novel Plyš by Michal Hvorecký was covered the most in the media.\n '
                    '               The smallest number of articles was published about Tajemství '
                    'oblázkové hory by Bára Dočkalová. Even\n                though it was '
                    'nominated for Magnesia Litera Award, it did not win the price in the end. '
                    'The closing part\n                focuses on a unique project by publishing '
                    'house Labyrint, a magazine for children called Raketa. Media\n               '
                    ' attention is focused on creators of magazine, either it is the owner of '
                    'publishing house Labyrint\n                Joachim Dvořák or its chief '
                    'editors Johana Švejdíková and Radana Litošová. Critical reflection is rare,'
                    '\n                there are mostly short notes recommending buying the '
                    'magazine or describing a new issue. There is a\n                broad '
                    'spectrum of media chosen for this analysis, from news media to cultural and '
                    'literary periodical\n                such as Tvar, Host, A2 and catalog '
                    'Nejlepší knihy dětem.',
            'lang': 'eng'
        }, {
            'name': 'Diplomová práce se zabývá analýzou mediálního ohlasu edic Fresh a Raketa '
                    'nakladatelství Labyrint v\n                kontextu vývoje nakladatelské '
                    'praxe v České republice v devadesátých letech. Věnuje se také současné\n     '
                    '           literatuře pro děti a mládež. Součástí práce je kritický ohlas na '
                    'tři konkrétní díla, jedná se o knihy\n                ze zkoumaných edic '
                    'Tajemství oblázkové hory Báry Dočkalové, Robinson Petra Síse a Plyš '
                    'Michala\n                Hvoreckého. Nejčastěji bylo v médiích referováno o '
                    'románu Plyš slovenského spisovatele Michala\n                Hvoreckého. '
                    'Nejméně příspěvků se věnovalo debutu Báry Dočkalové Tajemství oblázkové '
                    'hory, který byl sice\n                nominován na cenu Magnesia Litera '
                    '2019, nominaci ale neproměnil. Závěrečná část se věnuje unikátnímu\n         '
                    '       projektu nakladatelství Labyrint, kterým je dětský časopis Raketa. '
                    'Mediální pozornost přitahují zejména\n                jeho tvůrci, ať už jde '
                    'o majitele nakladatelství Joachima Dvořáka nebo šéfredaktorky Johanu '
                    'Švejdíkovou\n                a Radanu Litošovou. Kritická percepce časopisu '
                    'se objevuje sporadicky, jedná se zejména o představení\n                '
                    'časopisu nebo jeho doporučení. Spektrum zkoumaných periodik je široké od '
                    'zpravodajských webů a deníků až\n                po kulturní a literární '
                    'periodika Tvar, Host, A2 kulturní čtrnáctideník a katalog Nejlepší knihy '
                    'dětem.',
            'lang': 'cze'
        }],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH7020'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH7034'}],
            'keywords': [{'name': 'Labyrint', 'lang': 'cze'}, {'name': 'edice', 'lang': 'cze'},
                         {'name': 'mediální ohlas', 'lang': 'cze'},
                         {'name': 'Literature for Children and Youth', 'lang': 'eng'},
                         {'name': 'publishing house', 'lang': 'eng'},
                         {'name': 'Labyrint', 'lang': 'eng'},
                         {'name': 'edition', 'lang': 'eng'},
                         {'name': 'media response', 'lang': 'eng'}], 'id': '398853',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/univerzita_karlova_v_praze'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'degreeGrantor': [
                {'$ref': 'http://127.0.0.1:5000/api/taxonomies/universities/katedra_zurnalistiky'}],
            'title': [{
                'name': 'Nakladatelství Labyrint a mediální reflexe edic Fresh a Raketa',
                'lang': 'cze'
            }],
            'accessibility': [{'name': 'Dostupné v digitálním repozitáři UK.', 'lang': 'cze'},
                              {
                                  'name': 'Available in the Charles University Digital Repository.',
                                  'lang': 'eng'
                              }],
            'dateAccepted': '2019-06-20',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}],
            'defended': True
        },
        {
            'contributor': [],
            'identifier': [{'type': 'originalOAI', 'value': 'oai:medvik.cz:122605'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:189110'}],
            'creator': [{'name': 'Kratochvíl, Bohumil'}, {'name': 'Akademie věd České republiky'}],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/nlk20040148348'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/nlk20040147252'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/D002626'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/D002620'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/D004304'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph120179'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph114722'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph135174'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph116084'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph121510'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph114295'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/ph116680'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH11857'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH13081'}],
            'id': '189110',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/narodni_lekarska_knihovna'
            },
            'note': ['Souhrn angl'],
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/disertacni_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60461373_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Příspěvek k poznání polymorfie farmaceutických substancí',
                'lang': 'cze'
            }], 'accessibility': [{
            'name': 'Dokument je dostupný v NLK. Dokument je dostupný též v digitální formě v '
                    'Digitální knihovně NLK. Přístup\n                může být vázán na '
                    'prohlížení z počítačů NLK.',
            'lang': 'cze'
        },
            {
                'name': 'Available in the National Medical Library. Also available via the NML '
                        'digital library. Viewing may be\n                restricted to NML '
                        'computers.',
                'lang': 'eng'
            }],
            'extent': '40 s. :', 'dateAccepted': '2004-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Vlk, Jan', 'role': 'referee'},
                            {'name': 'Chudý, Peter', 'role': 'advisor'}],
            'identifier': [{'type': 'originalRecord', 'value': 'http://hdl.handle.net/11012/85155'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-386172'},
                           {'type': 'originalOAI', 'value': 'oai:dspace.vutbr.cz:11012/85155'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:386172'}],
            'creator': [{'name': 'Zembjaková, Martina'}], 'abstract': [{
            'name': 'Táto bakalárska práca sa zaoberá modernou vizualizáciou letových dát. '
                    'Obsahuje historický vývoj návrhu\n                vizualizácie letových dát '
                    'v pilotnej kabíne a súčasné trendy vizualizácie letových dát. Ďalej je v '
                    'práci\n                popísaný matematicko-fyzikálny popis lietadla, '
                    'návrh vizualizácie futuristického displeja so zameraním\n                na '
                    'jednopilotnú prevádzku a jeho samotná implementácia v prostredí 3D '
                    'grafického softvéru. Aplikácia je\n                navrhnutá pre použitie v '
                    'leteckom simulátore.',
            'lang': 'eng'
        }, {
            'name': 'This bachelor thesis addresses modern visualization of flight data. It '
                    'includes the historical\n                development of the flight data '
                    'visualization design and current flight data visualization trends.\n         '
                    '       Further, '
                    'thethesisdescribesamathematicalandphysicaldescriptionofanaircraft, '
                    'a proposal for the\n                futuristic display with focus on the '
                    'Single Pilot Operations and its implementation in a 3D graphic\n             '
                    '   engine environment. The application was designed to be used in the flight '
                    'simulator.',
            'lang': 'cze'
        }],
            'keywords': [{'name': 'Flight Data Visualization', 'lang': 'cze'},
                         {'name': 'Futuristic Cockpit', 'lang': 'cze'},
                         {'name': 'Head-Up Display', 'lang': 'cze'},
                         {'name': 'Single Pilot Operations', 'lang': 'cze'},
                         {'name': 'Flight Simulator', 'lang': 'cze'},
                         {'name': 'Virtual Reality', 'lang': 'cze'},
                         {'name': 'Unity 3D', 'lang': 'cze'},
                         {'name': 'vizualizácia letových dát', 'lang': 'eng'},
                         {'name': 'futuristický kokpit', 'lang': 'eng'},
                         {'name': 'priehľadový displej', 'lang': 'eng'},
                         {'name': 'jednopilotná prevádzka', 'lang': 'eng'},
                         {'name': 'letecký simulátor', 'lang': 'eng'},
                         {'name': 'virtuálna realita', 'lang': 'eng'},
                         {'name': 'Unity 3D', 'lang': 'eng'}], 'id': '386172',
            'provider': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/vutbr'},
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/bakalarske_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/00216305_no_faculty_no_department'
            }],
            'title': [{'name': 'Futuristický kokpit moderního letounu', 'lang': 'eng'}],
            'accessibility': [
                {'name': 'Plný text je dostupný v Digitální knihovně VUT.', 'lang': 'cze'},
                {
                    'name': 'Fulltext is available in the Brno University of Technology Digital '
                            'Library.',
                    'lang': 'eng'
                }], 'dateAccepted': '2018-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/eng'}]
        },
        {
            'contributor': [],
            'identifier': [{'type': 'originalRecord', 'value': 'http://www.jcu.cz/vskp/55245'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-396596'},
                           {'type': 'originalOAI', 'value': 'repository/55245'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:396596'},
                           {'type': 'catalogue', 'value': '55245'}],
            'creator': [{'name': 'NESTŘEBOVÁ, Jitka'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/7507R028'}],
            'id': '396596',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider'
                        '/jihoceska_univerzita_v_ceskych_budejovicich'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/bakalarske_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60076658_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Česká soudobá přednesová klavírní literatura pro děti a mládež '
                        'na konci 20. století',
                'lang': 'cze'
            }],
            'accessibility': [
                {'name': 'Plný text je dostupný v digitálním repozitáři JČU.', 'lang': 'cze'},
                {
                    'name': 'Fulltext is available in the Digital Repository of University of '
                            'South Bohemia.',
                    'lang': 'eng'
                }], 'extent': '53 stran', 'dateAccepted': '2019-07-12',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Borůvka, Luboš', 'role': 'advisor'}],
            'identifier': [{
                'type': 'originalRecord',
                'value': 'https://is.czu.cz/zp/index.pl?podrobnosti_zp=211079'
            },
                {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-259678'},
                {'type': 'originalOAI', 'value': 'oai:czu.cz:vskp/x211079'},
                {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:259678'}],
            'creator': [{'name': 'Skipalová, Klára'}],
            'studyField': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/4106V029'}],
            'abstract': [{
                'name': 'Písemná práce ke státní doktorské zkoušce se zabývá tématem, jak důlní a '
                        'metalurgická oblast ovlivňuje\n                životní prostředí. '
                        'Teoretická část se zabývá geochemií a chováním (mobilita, '
                        'biodostupnost)rizikových\n                prvků v půdě se zaměřením na '
                        'selen a molybden v oblastech ovlivněných těžbou a zpracováním\n          '
                        '      polymetalických rud Kombat a Berg Akuas, Namibie. Vlastní práce se '
                        'věnuje analýze a rozboru selenu a\n                molybdenu. Po rozboru '
                        'budou následovat doporučení, jak zabráni zvýšené mobilitě a nebezpečnému '
                        'až\n                toxickému působení selenu a molybdenu v těchto '
                        'oblastech.',
                'lang': 'cze'
            },
                {
                    'name': 'The aim of this thesis is to understand how mining and processing of '
                            'polymetallic ores in areas Kombat\n                and Berg Aukas of '
                            'Namibia may affect the geochemistry and behavior of hazardous '
                            'elements (selenium and\n                molybdenum), especially then '
                            'their mobility and bioavailability in the soil environment and '
                            'consequently\n                assess their potential hazardous '
                            'properties and factors affecting them.',
                    'lang': 'eng'
                }],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH5016'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH5808'},
                        {'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH5769'}],
            'id': '259678',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/ceska_zemedelska_univerzita'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/disertacni_prace'},
            'degreeGrantor': [{
                '$ref':
                    'http://127.0.0.1:5000/api/taxonomies/universities'
                    '/60460709_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Geochemie rizikových prvků v oblasti postižené těžbou a zpracováním '
                        'polymetalických rud - Namibie,\n                Afrika',
                'lang': 'cze'
            }],
            'accessibility': [
                {'name': 'Dostupné registrovaným uživatelům v repozitáři ČZU.', 'lang': 'cze'},
                {'name': 'Available to registered users in the CZU repository.', 'lang': 'eng'}],
            'dateAccepted': '2015-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'name': 'Gaff, Milan', 'role': 'advisor'},
                            {'name': 'Sarvašová Kvietková, Monika', 'role': 'referee'}],
            'identifier': [{
                'type': 'originalRecord',
                'value': 'https://is.czu.cz/zp/index.pl?podrobnosti_zp=204181'
            },
                {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-258349'},
                {'type': 'originalOAI', 'value': 'oai:czu.cz:vskp/b204181'},
                {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:258349'}],
            'creator': [{'name': 'Kroupa, Michal'}], 'studyField': [
            {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/no_valid_fcc50779-a5d7'
                        '-4359-b9f8-2660d0e738f1'
            }],
            'abstract': [{
                'name': 'Bakalářská práce Vlastnosti Thermowoodu v závislosti na ochranných '
                        'látkách je rozdělena do několika\n                kapitol. První '
                        'kapitola objasňuje pojem ThermoWood, kapitola druhá je zaměřena na '
                        'modifikaci dřeva,\n                třetí kapitola se věnuje vlastnostem '
                        'dřeva ThermoWood. Čtvrtá kapitola poukazuje na vliv ThermoWood na\n      '
                        '          životní prostředí. Pátá kapitola se zaměřuje na analýzu '
                        'literárních poznatků, šestá kapitola se věnuje\n                rozboru '
                        'využití nátěrových hmot v praxi. Předposlední sedmá kapitola je věnována '
                        'novým trendům v této\n                oblasti a poslední osmá kapitola '
                        'poukazuje na grafy finské společnosti ThermoWood, jež jsou zaměřeny na\n '
                        '               výrobní statistiku.',
                'lang': 'cze'
            }, {
                'name': 'Bachelor thesis Thermowood properties depending on the protective '
                        'substances is divided into several\n                chapters. The first '
                        'chapter explains the concept ThermoWood, the second chapter focuses on '
                        'wood\n                modification, the third chapter deals with the '
                        'properties of wood ThermoWood. The fourth chapter shows\n                '
                        'the impact on the environment ThermoWood. The fifth chapter focuses on '
                        'the analysis of literary\n                knowledge, chapter sixth '
                        'chapter is devoted to the analysis of the use of paints in practice. '
                        'The\n                penultimate seventh chapter is dedicated to new '
                        'trends in this area and the last eighth chapter shows\n                '
                        'the graphs of the Finnish ThermoWood companies that are focused on '
                        'production statistics.',
                'lang': 'eng'
            }],
            'keywords': [{'name': 'Modifikace dřeva', 'lang': 'cze'},
                         {'name': 'nátěrové látky', 'lang': 'cze'},
                         {'name': 'ochrana dřeva', 'lang': 'cze'},
                         {'name': 'vlastnosti dřeva', 'lang': 'cze'},
                         {'name': 'ThermoWood', 'lang': 'cze'}], 'id': '258349',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider/ceska_zemedelska_univerzita'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/bakalarske_prace'},
            'degreeGrantor': [{
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/universities'
                        '/60460709_no_faculty_no_department'
            }],
            'title': [{
                'name': 'Vlastnosti Thermowoodu v závislosti na ochranných látkách',
                'lang': 'cze'
            }],
            'accessibility': [
                {'name': 'Dostupné registrovaným uživatelům v repozitáři ČZU.', 'lang': 'cze'},
                {'name': 'Available to registered users in the CZU repository.', 'lang': 'eng'}],
            'dateAccepted': '2016-01-01',
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}]
        },
        {
            'contributor': [{'role': 'advisor', 'name': 'Kastl, Jan'},
                            {'role': 'referee', 'name': 'Nováček, Jan'},
                            {'role': 'referee', 'name': 'Svoboda, Karel'}], 'id': '113',
            'studyField': [
                {
                    '$ref': 'http://127.0.0.1:5000/api/taxonomies/studyfields/no_valid_dd3100ed'
                            '-53cc-4d5c-b4f8-74c04b177db6'
                }],
            'accessRights': 'open', 'creator': [{'name': 'Jung, Roman'}], 'abstract': [{
            'lang': 'cze',
            'name': 'Cílem práce je zpřístupnit dostupné prostředky pro přenos EDIFACTu v '
                    'internetu, seznámit s\n                bezpečnostními aspekty, '
                    'které z daného vyplývají a přiblížit je oboru dopravy v ČR v návaznosti na\n '
                    '               automatizované informační systémy i jim předcházející prvotní '
                    'vkládání dat z webových formulářů,\n                především menšími '
                    'institucemi. Práce nově představuje normy AS1, AS2 a AS3 skupiny EDIINT pro '
                    'přenos EDI\n                zpráv internetem pod protokoly SMTP, HTTP a FTP.'
        }],
            'dateAccepted': '2006-06-12',
            'provider': {
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/provider'
                        '/vysoka_skola_ekonomicka_v_praze'
            },
            'doctype': {'$ref': 'http://127.0.0.1:5000/api/taxonomies/doctype/diplomove_prace'},
            'keywords': [{'lang': 'cze', 'name': 'Česká republika'}, {'lang': 'cze', 'name': 'AS3'},
                         {'lang': 'cze', 'name': 'AS2'}, {'lang': 'cze', 'name': 'AS1'},
                         {'lang': 'cze', 'name': 'EDI'},
                         {'lang': 'cze', 'name': 'EDIFACT'}, {'lang': 'cze', 'name': 'Internet'}],
            'subject': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/subject/PSH1038'}],
            'title': [{
                'lang': 'cze',
                'name': 'Studie využitelnosti Internetu pro přenos EDIFACTu v oblasti dopravy v ČR'
            }],
            'degreeGrantor': [{
                '$ref': 'http://127.0.0.1:5000/api/taxonomies/universities'
                        '/61384399_no_faculty_no_department'
            }],
            'identifier': [{'type': 'originalRecord', 'value': 'http://www.vse.cz/vskp/eid/205'},
                           {'type': 'nusl', 'value': 'http://www.nusl.cz/ntk/nusl-113'},
                           {'type': 'nuslOAI', 'value': 'oai:invenio.nusl.cz:113'}],
            'language': [{'$ref': 'http://127.0.0.1:5000/api/taxonomies/languages/cze'}],
            'accessibility': [{'lang': 'cze', 'name': 'Dostupné v digitálním repozitáři VŠE.'}, {
                'lang': 'eng',
                'name': 'Available in the digital repository of the University of Economics, '
                        'Prague.'
            }]
        }

    ]
