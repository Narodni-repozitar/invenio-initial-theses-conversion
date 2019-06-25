from invenio_initial_theses_conversion.nusl_overdo import handled_values, single_value
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^502')
@handled_values('c', 'b', 'a', 'g', 'd')
@single_value
def degree_grantor(self, key, value):
    ret = {}
    parsed_grantor = None
    if "c" in value:
        parsed_grantor = [x.strip() for x in value.get("c").split(",", maxsplit=2) if x.strip()]
    if parsed_grantor:
        # raise Exception("Degree grantor field is empty")
        ret["name"] = parsed_grantor[0]
        if len(parsed_grantor) > 1:
            ret["faculties"] = [{"name": parsed_grantor[1]}]
            if len(parsed_grantor) > 2:
                ret["faculties"][0]["deparments"] = [parsed_grantor[2]]

        return {
            "language": "cze",
            "university": ret
        }
