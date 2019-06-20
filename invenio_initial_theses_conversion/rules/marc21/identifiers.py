from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("identifier", '^856')
@extra_argument('originalOAI', '^035')
@extra_argument('nuslOAI', '^909C')
@extra_argument('catalogue', '^970')
# @handled_values('a', 'b')
def identifier(self, key, value, originalOAI, nuslOAI, catalogue):
    """Identifiers"""
    identifier = []
    for id in value:
        if id.get("z") == 'Odkaz na původní záznam':
            identifier.append({
                "value": id.get("u"),
                "type": "originalRecord"
            })
        if id.get("z") == "PID NUŠL":
            identifier.append({
                "value": id.get("u"),
                "type": "nusl"
            })
    if originalOAI is not None:
        identifier.append({
            "value": originalOAI.get("a"),
            "type": "originalOAI"
        })
    identifier.append({
        "value": nuslOAI.get("o"),
        "type": "nuslOAI"
    })
    if catalogue:
        identifier.append({
            "value": catalogue.get("a"),
            "type": "catalogue"
        })
    return identifier

