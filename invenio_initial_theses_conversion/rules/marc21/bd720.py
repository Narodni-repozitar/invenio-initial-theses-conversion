from invenio_initial_theses_conversion.nusl_overdo import merge_results
from ..model import old_nusl


@old_nusl.over("creator", '^720')
@merge_results
def people(self, key, value):
    """Creator and contributor"""
    creator = []
    contributor = []
    for person in value:
        if person.get('a'):
            creator.append({
                "name": person.get('a'),
                "id": {
                    "value": None,
                    "type": None
                }
            })
        if person.get('i'):
            contributor.append({
                "name": person.get('i'),
                "role": person.get('e'),
                "id": {
                    "value": None,
                    "type": None
                }
            })
    return {
        "creator": creator,
        "contributor": contributor
    }
