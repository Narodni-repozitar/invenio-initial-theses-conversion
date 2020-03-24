import xmltodict
from dojson.contrib.marc21.utils import create_record
from dojson.utils import GroupableOrderedDict
from lxml import etree
from sickle.models import Record


class MarcXMLParser(Record):
    # Your XML unpacking implementation goes here.
    def __init__(self, record_element):
        super().__init__(record_element, strip_ns=True)
        # self.json = self._get_json()
        self.marc_dict = self._get_dict()

    def _get_json(self):
        json_dict = xmltodict.parse(etree.tostring(self.xml))
        return json_dict

    def _get_dict(self):
        record = create_record(self.raw)
        return self.transform_to_dict(record)

    def transform_to_dict(self, source):
        if isinstance(source, (GroupableOrderedDict, dict)):
            new_dict = {}
            for k, v in source.items():
                if k == "__order__":
                    continue
                new_dict[k] = self.transform_to_dict(v)
            return new_dict
        if isinstance(source, (list, tuple)):
            new_list = []
            for item in source:
                new_list.append(self.transform_to_dict(item))
            return new_list
        else:
            return source
