from invenio_initial_theses_conversion.nusl_overdo import handled_values
from ..model import old_nusl


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
def degree_grantor(self, key, values):
    ret = [
        {
            "university": {
                "name": [],
            }
        }
    ]
    for item in values:
        uni = ret[0]["university"]
        uni["name"].append(
            {
                "name": item.get("a"),
                "lang": item.get("9")
            }
        )
        if item.get("g"):
            if "faculties" not in uni:
                uni["faculties"] = [
                    {
                        "name": []
                    }
                ]
            faculty = ret[0]["university"]["faculties"][0]
            faculty["name"].append(
                {
                    "name": item.get("g"),
                    "lang": item.get("9")
                }
            )
        if item.get("b"):
            if "faculties" in uni:
                if "departments" not in faculty:
                    faculty["departments"] = []
                department = faculty["departments"]
                department.append(
                    {
                        "name": item.get("b"),
                        "lang": item.get("9")
                    }
                )

    return ret
