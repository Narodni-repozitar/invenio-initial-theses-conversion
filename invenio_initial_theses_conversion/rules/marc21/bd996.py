from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, merge_results
from ..model import old_nusl


@old_nusl.over('accessibility', '^996__')
@merge_results
@handled_values('a', 'b', '9')
@single_value
def accessibility(self, key, value):
    ret = {}

    accessibility = []
    for k, lang in (('a', 'cze'), ('b', 'eng')):
        if k in value:
            accessibility.append(
                {
                    'name': value.get(k),
                    'lang': lang
                }
            )
    if accessibility:
        ret['accessibility'] = accessibility

    if '9' in value:
        ret['accessRights'] = {
            '1': 'open',
            '0': 'restricted'
        }[value.get('9')]

    return ret
