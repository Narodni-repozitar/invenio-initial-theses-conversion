import csv
import os
from werkzeug.utils import cached_property


class StudyFieldsTaxonomy(object):

    # def __init__(self, app):
    #     """Initialize state."""
    #     self.app = app

    # @cached_property
    def load_fields(self):
        dir = os.path.dirname(__file__)
        filepath = os.path.abspath(
            os.path.join(dir, "..", "..", "invenio-nusl", "invenio_nusl", "data", "studijni_obory.csv"))
        with open(filepath) as f:
            reader = csv.DictReader(f, delimiter=";")
            fields = {}
            for row in reader:
                record = {
                    "name": row["Název oboru"],
                    "programme": {
                        "name": row["Název programu"],
                        "code": row["STUDPROG"]
                    },
                    "university": row["Název VŠ"],
                    "faculty": row["Součást vysoké školy"],
                    "language": row["Jazyk výuky"],
                    "degree": row["Typ programu"]
                }
                if row["AKVO"] in fields:
                    fields[row["AKVO"]].append(record)
                else:
                    fields[row["AKVO"]] = [record]
        return fields

    def check_field(self, codes, grantor=None, doc_type=None):
        matched_codes = self.degree(codes, doc_type=doc_type)
        matched_codes, matched_fields = self.grantor(matched_codes, grantor=grantor)
        return {
            "studyfield": matched_codes,
            "studyprogramme": [field["programme"]["code"] for field in matched_fields]
        }

    def grantor(self, codes, grantor=None):
        if grantor is None:
            return codes
        studyfields = self.load_fields()
        matched_codes = []
        matched_fields = []
        for code in codes:
            fields = [field for field in studyfields.get(code, {}) if
                      field["language"] == "Česky" and field["university"].lower() == grantor]
            if len(fields) != 0:
                matched_codes.append(code)
                matched_fields.append(fields[0])
        if len(matched_codes) == 0:
            return codes
        return matched_codes, matched_fields

    def degree(self, codes, doc_type=None):
        if doc_type is None:
            return codes
        degree_dict = {
            "R": "bakalarske_prace",
            "T": "diplomove_prace",
            "V": "disertacni_prace"
        }
        match_codes = {code for code in codes if degree_dict[code[4]] == doc_type}
        return match_codes
