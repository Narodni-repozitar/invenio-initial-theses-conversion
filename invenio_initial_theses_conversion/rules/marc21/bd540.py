from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, list_value, handled_values, \
    append_results, merge_results
from ..model import old_nusl
import re


def _CC_version(text):
    pattern = re.compile(r'\d.\d')
    mo = pattern.search(text)
    version = mo.group()
    if version is not None:
        return version
    else:
        raise AttributeError("Version number has not been found")


def _CC_license_CZ(text):
    if ("Uveďte původ-Neužívejte komerčně-Nezpracovávejte" in text) or \
            ("Uveďte autora-Neužívejte dílo komerčně-Nezasahujte do díla" in text):
        return "CC BY-NC-ND"
    elif ("Uveďte původ-Neužívejte dílo komerčně-Zachovejte licenci" in text) or \
            ("Uveďte autora-Neužívejte dílo komerčně-Zachovejte licenci" in text) or \
            ("Uveďte původ-Neužívejte komerčně-Zachovejte licenci" in text):
        return "CC BY-NC-SA"
    elif ("Uveďte původ-Neužívejte komerčně" in text) or \
            ("Uveďte autora-Neužívejte dílo komerčně" in text):
        return "CC BY-NC"
    elif ("Uveďte původ-Nezpracovávejte" in text) or \
            ("Uveďte autora-Nezasahujte do díla" in text):
        return "CC BY-ND"
    elif ("Uveďte původ-Zachovejte licenci" in text) or \
            ("Uveďte autora-Zachovejte licenci" in text):
        return "CC BY-SA"
    elif ("Uveďte původ" in text) or \
            ("Uveďte autora " in text):
        return "CC BY"
    else:
        return _CC_license_EN(text)


def _CC_license_EN(text):
    if "Attribution-NonCommercial-NoDerivs" in text:
        return "CC BY-NC-ND"
    elif "Attribution-NonCommercial-ShareAlike" in text:
        return "CC BY-NC-SA"
    elif "Attribution-NonCommercial" in text:
        return "CC BY-NC"
    elif "Attribution-NoDerivs" in text:
        return "CC BY-ND"
    elif "Attribution-ShareAlike" in text:
        return "CC BY-SA"
    elif "Attribution" in text:
        return "CC BY"
    else:
        raise AttributeError('The CC license has not been found')


@old_nusl.over("rights", '540')
@handled_values('a', '9')
def rights(self, key, values):
    """Rights."""
    for value in values:
        licence = value.get("a")
        if "121/2000" in licence:
            if 'rights' not in locals() or 'rights' not in globals():
                rights = {"copyright": []}
            if "121/2000 Sb." in licence:
                rights["copyright"].append({
                    "name": "Dílo je chráněno podle autorského zákona č. 121/2000 Sb.",
                    "lang": "cze"
                })

            if "121/2000 Coll." in licence:
                rights["copyright"].append({
                    "name": "This work is protected under the Copyright Act No. 121/2000 Coll.",
                    "lang": "eng"
                })
        if "Creative Commons" in licence:
            if 'rights' not in locals() or 'rights' not in globals():
                rights = {
                    "CC": {
                        "code": None,
                        "version": None,
                        "country": None
                    }
                }
            if rights.get("CC", None) is None:
                rights["CC"] = {
                    "code": None,
                    "version": None,
                    "country": None
                }

                rights["CC"]["code"] = _CC_license_CZ(licence)
                rights["CC"]["version"] = _CC_version(licence)
                if _CC_version(licence) == "4.0":
                    rights["CC"]["country"] = "INT"
                elif _CC_version(licence) == "3.0":
                    rights["CC"]["country"] = "CZE"
                else:
                    rights["CC"]["country"] = "CZE"

    return rights
