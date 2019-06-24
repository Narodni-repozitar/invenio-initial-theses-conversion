from invenio_initial_theses_conversion.nusl_overdo import handled_values
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
def degree_grantor(self, key, values):
    ret = []
    for item in values:
        university = {
            "name": item.get("a"),

        }
        if item.get("g"):
            university["faculties"] = [
                {
                    "name": item.get("g"),

                }
            ]
            if item.get("b"):
                university["faculties"][0]["departments"] = [
                    item.get("b")
                ]
        ret.append(
            {
                "language": item.get("9"),
                "university": university
            }
        )
    if len(ret) > 2:
        raise Exception("There is more then two records for degreeGrantor")
    return ret
