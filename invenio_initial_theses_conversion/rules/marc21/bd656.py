from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, flatten_dict_value
from ..model import old_nusl

@old_nusl.over("studyProgramme", '^656_7')
@flatten_dict_value
@single_value
def studyProgramme_Field(self, key, value):
    """Language Code."""
    study = value.get("a")
    if "/" not in study:
        raise AttributeError("Slash is not in study code")
    studyProgramme, studyField = study.split("/", 1)
    return {
        "studyProgramme": {"name": studyProgramme},
        "studyField": {"name": studyField}
    }
