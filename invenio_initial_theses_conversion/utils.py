from collections import OrderedDict

from dojson.utils import GroupableOrderedDict

from flask_taxonomies.models import Taxonomy
from flask_taxonomies.utils import find_in_json_contains

LANGUAGE_EXCEPTIONS = {"scc": "srp", "scr": "hrv"}


def psh_term_filter(psh_list_terms, name):
    if len(psh_list_terms) == 0:
        return None
    matched_terms = []
    for term in psh_list_terms:
        match = False
        for dict in term.extra_data["title"]:
            for v in dict.values():
                if v == name:
                    match = True
        if match:
            matched_terms.append(term)
    if len(matched_terms) > 0:
        return matched_terms[0]
    return None


def fix_language(datafield, tag, ind1, ind2, code):
    if datafield.attrib["tag"] == tag and datafield.attrib["ind1"] == ind1 and datafield.attrib["ind2"] == ind2:
        for subfield in datafield:
            if subfield.attrib["code"] == code:
                subfield.text = LANGUAGE_EXCEPTIONS.get(subfield.text, subfield.text)


def fix_grantor(data):
    data = dict(data)
    if "502__" in data:
        value = data.get("502__")
        parsed_grantor = value.get("c")
        if parsed_grantor is not None:
            if "," in value.get("c"):
                parsed_grantor = [x.strip() for x in value.get("c").split(",", maxsplit=2) if x.strip()]
            elif "." in value.get("c"):
                parsed_grantor = [x.strip() for x in value.get("c").split(".", maxsplit=2) if x.strip()]
            else:
                parsed_grantor = [parsed_grantor]

            if parsed_grantor:
                if "7102_" not in data:
                    data["7102_"] = [
                        {
                            "a": parsed_grantor[0],
                            "9": "cze"
                        }
                    ]
                    if len(parsed_grantor) > 1:
                        data["7102_"][0].update(
                            {
                                "g": parsed_grantor[1]
                            }
                        )
                        if len(parsed_grantor) > 2:
                            data["7102_"][0].update(
                                {
                                    "b": parsed_grantor[2]
                                }
                            )
                    data["7102_"] = tuple(data["7102_"])

        del data["502__"]

    if ("502__" not in data) and ("7102_" not in data) and ("998__" in data):
        if data["998__"]["a"] == "vutbr":
            data["7102_"] = [
                {
                    "a": "Vysoké učení technické v Brně",
                    "9": "cze"
                }
            ]
        if data["998__"]["a"] == "ceska_zemedelska_univerzita":
            data["7102_"] = [
                {
                    "a": "Česká zemědělská univerzita v Praze",
                    "9": "cze"
                }
            ]
        if data["998__"]["a"] == "jihoceska_univerzita_v_ceskych_budejovicich":
            data["7102_"] = [
                {
                    "a": "Jihočeská univerzita v Českých Budějovicích",
                    "9": "cze"
                }
            ]
        if data["998__"]["a"] == "mendelova_univerzita_v_brne":
            data["7102_"] = [
                {
                    "a": "Mendelova univerzita v Brně",
                    "9": "cze"
                }
            ]
        data["7102_"] = tuple(data["7102_"])

    return GroupableOrderedDict(OrderedDict(data))


def fix_keywords(data):
    tax = Taxonomy.get("subject")
    data = dict(data)
    subject_tuple = []
    if "653__" in data or "6530_" in data:
        values = data.get("653__")
        delete_position = []
        for idx, value in enumerate(values):
            parsed_keyword = value.get("a")
            psh_list_terms = find_in_json_contains(parsed_keyword, tax, "title").all()
            if len(psh_list_terms) == 0:
                psh_list_terms = find_in_json_contains(parsed_keyword, tax, "altTitle").all()
            term = psh_term_filter(psh_list_terms, parsed_keyword)
            if len(psh_list_terms) == 0 or term is None:
                continue
            record_dict = {
                "2": "psh",
                "7": term.slug,
                "a": parsed_keyword
            }
            subject_tuple.append(GroupableOrderedDict(OrderedDict(record_dict)))
            delete_position.append(idx)

        if len(delete_position) > 0:
            keyword_list = list(data["653__"])
            for position in reversed(delete_position):
                del keyword_list[position]
            data["653__"] = tuple(keyword_list)

        if len(subject_tuple) > 0:
            if "650_7" in data:
                old_subject_tuple = list(data["650_7"])
                subject_tuple.extend(old_subject_tuple)
            data["650_7"] = tuple(subject_tuple)
    return GroupableOrderedDict(OrderedDict(data))