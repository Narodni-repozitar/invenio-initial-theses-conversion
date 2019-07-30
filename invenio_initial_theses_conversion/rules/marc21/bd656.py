from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import single_value, merge_results
from ..model import old_nusl


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
def studyProgramme_Field(self, key, value):
    """Study programme."""
    study = value.get("a")
    tax = Taxonomy.get("studyfields", required=True)
    if "/" not in study:
        try:
            # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
            field = tax.descendants.filter(
                TaxonomyTerm.extra_data[("name", 0, "name")].astext == study).all()
            return {
                "studyField": {
                    "$ref": field.tree_path  # TODO: měl by být link_self
                }
            }
        except NoResultFound:
            try:
                field = tax.descendants.filter(
                    TaxonomyTerm.extra_data["aliases"].astext() == study).all()
                if len(field) == 1:
                    return {
                        "studyField": {
                            "$ref": field[0].tree_path  # TODO: měl by být link_self
                        }
                    }  # TODO: dokončit
                else:
                    print(field)  # TODO: dokončit
            except NoResultFound:
                raise
        return {"studyField": {"name": study}}

    studyProgramme, studyField = study.split("/", 1)
    studyField = studyField.strip()
    studyProgramme = studyProgramme.strip()

    return {
        "studyProgramme": {"name": studyProgramme},
        "studyField": {"name": studyField}
    }
