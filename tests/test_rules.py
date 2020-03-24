import pytest
from dojson.contrib.marc21.utils import create_record, split_stream

from invenio_initial_theses_conversion.utils import fix_grantor, fix_keywords, \
    split_stream_oai_nusl, fix_language
from invenio_initial_theses_conversion.rules.model import old_nusl
from invenio_nusl_theses.marshmallow import ThesisMetadataSchemaV1
from tests.conftest import results_fix, results


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected


@pytest.mark.parametrize("field,expected", list(results_fix(results())))
def test_rules(app, db, field, expected):
    # array = [create_record(data) for data in
    #          split_stream(
    #              open(
    #                  '/home/semtex/Projekty/nusl/invenio-initial-theses-conversion/tests'
    #                  '/xml_files/vskp_test2.xml',
    #                  'rb'))]
    # for idx, field in enumerate(array):
    rec = fix_grantor(field)
    # rec = fix_keywords(rec)
    rec = fix_language(rec)
    transformed = old_nusl.do(rec)
    schema = ThesisMetadataSchemaV1()
    marshmallowed = schema.load(transformed).data
    marshmallowed = schema.dump(marshmallowed).data
    print(marshmallowed)
    assert marshmallowed == expected
    # print(transformed)


# @pytest.mark.skip(reason="Problem with subjects was fixed")
def test_rules_2(app, db):
    array = [create_record(data) for data in
             split_stream(
                 open(
                     '/home/semtex/Projekty/nusl/invenio-initial-theses-conversion/tests'
                     '/xml_files/id113.xml',
                     'rb'))]
    for idx, field in enumerate(array):
        rec = fix_grantor(field)
        # rec = fix_keywords(rec)
        rec = fix_language(rec)
        transformed = old_nusl.do(rec)
        schema = ThesisMetadataSchemaV1()
        marshmallowed = schema.load(transformed).data
        marshmallowed = schema.dump(marshmallowed).data
        print(marshmallowed)


@pytest.mark.skip(reason="Problem with subjects was fixed")
def test_rules_3(app, db):
    array = [create_record(data) for data in
             split_stream(
                 open(
                     '/home/semtex/Projekty/nusl/invenio-initial-theses-conversion/tests'
                     '/xml_files/keywords_pipe.xml',
                     'rb'))]
    for idx, field in enumerate(array):
        rec = fix_grantor(field)
        rec = fix_keywords(rec)
        rec = fix_language(rec)
        transformed = old_nusl.do(rec)
        schema = ThesisMetadataSchemaV1()
        marshmallowed = schema.load(transformed).data
        marshmallowed = schema.dump(marshmallowed).data
        print(marshmallowed)


@pytest.mark.skip(reason=None)
def test_rules_oai(app, db):
    array = [create_record(data) for data in
             split_stream_oai_nusl(
                 open(
                     '/home/semtex/Projekty/nusl/invenio-initial-theses-conversion/tests'
                     '/xml_files/oai_nusl_listrecords.xml',
                     'rb'))]
    for field in array:
        rec = fix_grantor(field)
        transformed = old_nusl.do(rec)
        schema = ThesisMetadataSchemaV1()
        marshmallowed = schema.load(transformed).data
        marshmallowed = schema.dump(marshmallowed).data
        print(transformed)
        print("------------MARSHMALLOWED---------------------", marshmallowed)
