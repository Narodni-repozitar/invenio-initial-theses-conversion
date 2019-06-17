from invenio_initial_theses_conversion.nusl_overdo import single_value, append_results, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("subject", '^650_7')
@append_results
@list_value
@handled_values('0', '2', 'a', 'j', '7')
def subject(self, key, value):
    """Language Code."""
    if not value.get("a"):
        raise AttributeError("Subject name required (650_7a)")
    subject = {"name": []}
    if "a" in value:
        subject["name"].append({
            "name": value.get("a"),
            "lang": "cze"
        })
    if "j" in value:
        subject["name"].append({
            "name": value.get("j"),
            "lang": "eng"
        })
    if "0" in value:
        if "7" in value:
            raise AttributeError("Id and URL must not be present in single subject (650_70, 650_77)")
        subject["id"] = value.get("0")
    if "7" in value:
        subject["id"] = value.get("7")
    if "2" in value:
        subject["taxonomy"] = value.get("2")
    return subject
