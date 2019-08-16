from dojson.contrib.marc21.utils import create_record, split_stream

from invenio_initial_theses_conversion.main import fix_grantor
from invenio_initial_theses_conversion.rules.model import old_nusl
from invenio_nusl_theses.marshmallow import ThesisMetadataSchemaV1


def test_rules(app, db):
    array = [create_record(data) for data in
             split_stream(
                 open('/home/semtex/Projekty/nusl/invenio-initial-theses-conversion/tests/xml_files/vskp_test2.xml',
                      'rb'))]
    for field in array:
        rec = fix_grantor(field)
        transformed = old_nusl.do(rec)
        schema = ThesisMetadataSchemaV1()
        marshmallowed = schema.load(transformed).data
        marshmallowed = schema.dump(marshmallowed).data
        print(transformed)
        print("------------MARSHMALLOWED---------------------", marshmallowed)
