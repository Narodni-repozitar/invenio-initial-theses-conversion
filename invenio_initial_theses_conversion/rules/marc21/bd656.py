from invenio_initial_theses_conversion.nusl_overdo import extra_argument, single_value, merge_results
from ..model import old_nusl


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
def studyProgramme_Field(self, key, value):
    """Study programme."""
    study = value.get("a")
    if "/" not in study:
        return {"studyField": {"name": study}}
    studyProgramme, studyField = study.split("/", 1)
    return {
        "studyProgramme": {"name": studyProgramme},
        "studyField": {"name": studyField}
    }
