from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, list_value
from ..model import old_nusl


@old_nusl.over('doctype', '^980__')
@handled_values('a')
def doctype(self, key, values):
    # nusl collection
    if values[0].get('a') not in (
            'bakalarske_prace',
            'diplomove_prace',
            'disertacni_prace',
            'habilitacni_prace',
            'rigorozni_prace'
    ):
        raise AttributeError(f'Unhandled doctype {values[0].get("a")}')

    return {
        'taxonomy': 'NUSL',
        'value': [
            'vskp',
            values[0].get('a')
        ]
    }
