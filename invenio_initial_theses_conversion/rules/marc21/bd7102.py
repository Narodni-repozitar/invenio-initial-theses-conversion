from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
def degree_grantor(self, key, values):
    ret = {}
    for val in values:
        if 'a' in val:
            ret.setdefault('university', []).append({
                'name': val.get('a'),
                'lang': val.get('9', 'cze')
            })
        if 'g' in val:
            ret.setdefault('faculty', []).append({
                'name': val.get('g'),
                'lang': val.get('9', 'cze')
            })
        if 'b' in val:
            ret.setdefault('department', []).append({
                'name': val.get('b'),
                'lang': val.get('9', 'cze')
            })
    return ret