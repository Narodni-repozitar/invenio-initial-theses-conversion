from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, list_value
from ..model import old_nusl


@old_nusl.over('doctype', '^980__')
@handled_values('a')
@list_value
def doctype(self, key, value):
    # nusl collection
    if value.get('a') not in (
            'bakalarske_prace',
            'diplomove_prace',
            'disertacni_prace',
            'habilitacni_prace',
            'rigorozni_prace'
    ):
        raise AttributeError(f'Unhandled doctype {value.get("a")}')

    return {
        'taxonomy': 'NUSL',
        'value': [
            'vskp',
            value.get('a')
        ]
    }
