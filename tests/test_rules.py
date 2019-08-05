from dojson.contrib.marc21.utils import create_record, split_stream

from invenio_initial_theses_conversion.main import fix_grantor
from invenio_initial_theses_conversion.rules.model import old_nusl


def test_rules(app, db):
    array = [create_record(data) for data in
             split_stream(open('/home/semtex/Projekty/NUSL_data/XML_test/vskp.xml', 'rb'))]
    for field in array:
        rec = fix_grantor(field)
        transformed = old_nusl.do(rec)
        print(transformed)
