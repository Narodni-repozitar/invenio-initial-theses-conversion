import functools
import os
from difflib import get_close_matches

from invenio_nusl_theses.marshmallow.json import import_csv

DIR = os.path.dirname(__file__)
path = DIR + "/data/obory.txt"
matrika_fields = set(import_csv("field.csv", 1, 2)[0][1:])

with open(path) as fp:
    fields = list(fp)


def nusl_prg_fields(fields):
    study_fields = []
    study_prg = []
    for field in fields:
        field = field.strip().replace("\xa0", " ")
        if "/" in field:
            st_prg, st_field = field.split("/", 1)
            study_prg.append(st_prg.strip())
            study_fields.append(st_field.strip())
        else:
            study_fields.append(field)

    return set(study_prg), set(study_fields)


@functools.lru_cache()
def refactor_fields():
    nusl_fields = nusl_prg_fields(fields)[1] - matrika_fields
    ref_dict = {}
    decide_dict = {}
    no_match = []
    for field in nusl_fields:
        option = get_close_matches(field, list(matrika_fields))
        if len(option) == 0:
            no_match.append(field)
        if len(option) == 1:
            ref_dict[field] = option[0]
        if len(option) > 1:
            decide_dict[field] = option
    return no_match, decide_dict, ref_dict


if __name__ == '__main__':
    print(refactor_fields()[2])
    print(len(refactor_fields()[2]))
