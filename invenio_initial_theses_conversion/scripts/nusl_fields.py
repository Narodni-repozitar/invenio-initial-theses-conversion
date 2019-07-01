import functools
import os
import pprint
from difflib import get_close_matches

from invenio_nusl_theses.marshmallow.json import import_csv

DIR = os.path.dirname(__file__)
path = DIR + "/data/obory.txt"
matrika_fields = set(import_csv("field.csv", 1, 2)[0][1:])
matrika_programme = set(import_csv("programme.csv", 1, 2)[0][1:])

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
def refactor_data(nusl_data, matrika_data):
    """
    Compare original data with controlled dictionary. If found data that does not match with dictionary, trying to find
    similar data in dictionary.
    :param nusl_data: Set of NUSL data for comparing
    :param matrika_data: Set of matrika data for comparing
    :return: return list of 3 sets,
     1. set returns data without proposal,
      2. set returns data with more proposals,
       3. set returns data with only one proposal
     """
    nusl_fields = nusl_data - matrika_data
    ref_dict = {}
    decide_dict = {}
    no_match = []
    for field in nusl_fields:
        option = get_close_matches(field, list(matrika_data))
        if len(option) == 0:
            no_match.append(field)
        if len(option) == 1:
            ref_dict[field] = option[0]
        if len(option) > 1:
            decide_dict[field] = option
    return no_match, decide_dict, ref_dict


if __name__ == '__main__':
    print(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[0])
    print(len(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[0]))
    print(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[1])
    print(len(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[1]))
    print(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[2])
    print(len(refactor_data(frozenset(nusl_prg_fields(fields)[0]), frozenset(matrika_programme))[2]))
