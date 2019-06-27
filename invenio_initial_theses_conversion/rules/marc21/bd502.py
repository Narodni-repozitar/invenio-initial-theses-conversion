from invenio_initial_theses_conversion.nusl_overdo import handled_values, single_value
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^502')
@handled_values('c', 'b', 'a', 'g', 'd')
@single_value
def degree_grantor(self, key, value):
    ret = {}
    if "c" in value:
        parsed_grantor = [value.get("c")]
        if "," in value.get("c"):
            parsed_grantor = [x.strip() for x in value.get("c").split(",", maxsplit=2) if x.strip()]
        if "." in value.get("c"):
            parsed_grantor = [x.strip() for x in value.get("c").split(".", maxsplit=2) if x.strip()]
        if parsed_grantor:
            # raise Exception("Degree grantor field is empty")
            ret["name"] = [
                {
                    "name": parsed_grantor[0],
                    "lang": "cze"
                }
            ]
            if len(parsed_grantor) > 1:
                ret["faculties"] = [
                    {
                        "name": [
                            {
                                "name": parsed_grantor[1],
                                "lang": "cze"
                            }
                        ]
                    }
                ]
                if len(parsed_grantor) > 2:
                    ret["faculties"][0]["departments"] = [{"name": parsed_grantor[2], "lang": "cze"}]
            return [
                {"university": ret}
            ]
