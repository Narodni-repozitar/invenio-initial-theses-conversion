from invenio_initial_theses_conversion.nusl_overdo import handled_values
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
def degree_grantor(self, key, values):
    ret = []
    for item in values:
        ret.append(
            {
                "language": item.get("9"),
                "university": {
                    "name": item.get("a"),
                    "faculties": [
                        {
                            "name": item.get("g"),
                            "departments": [
                                item.get("b")
                            ]
                        }
                    ]
                }
            }
        )
    if len(ret) > 2:
        raise Exception("There is more then two records for degreeGrantor")
    return ret
