from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from ..model import old_nusl


@old_nusl.over("subject", '^650_7')
@append_results
@list_value
@handled_values('0', '2', 'a', 'j', '7')
def subject(self, key, value):
    """Subject."""
    if not value.get("a"):
        raise AttributeError("Subject name required (650_7a)")
    subject = {}
    if "a" in value:
        subject["name"] = value.get("a")
        subject["lang"] = "cze"
    if "j" in value:
        subject["name"] = value.get("j")
        subject["lang"] = "eng"
    if "0" in value:
        if "7" in value:
            raise AttributeError("Id and URL must not be present in single subject (650_70, 650_77)")
        subject["id"] = value.get("0")
    if "7" in value:
        subject["id"] = value.get("7")
    if "2" in value:
        subject["taxonomy"] = value.get("2")
    return subject


@old_nusl.over("subject", '^653')
@append_results
@list_value
@handled_values('a')
def keyword(self, key, value):
    """Subject."""
    if key == '653__':
        return {
            "name": value.get("a"),
            "lang": "cze"
        }

    if key == '6530_':
        return {
            "name": value.get("a"),
            "lang": "eng"
        }
