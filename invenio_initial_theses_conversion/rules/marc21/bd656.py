from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import single_value, merge_results
from ..model import old_nusl
from invenio_initial_theses_conversion.ext import StudyFieldsTaxonomy


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
def studyProgramme_Field(self, key, value):
    """Study programme."""
    study = value.get("a")
    tax = Taxonomy.get("studyfields", required=True)
    if "/" not in study:
        # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
        fields = tax.descendants.filter(
            TaxonomyTerm.extra_data[("name", 0, "name")].astext == study).all()
        codes = {field.slug for field in fields}
        result = StudyFieldsTaxonomy()
        result_dict = result.check_field(codes, grantor="Vysoká škola chemicko-technologická v Praze",
                                         doc_type="diplomove_prace")
        term = tax.get_term(result_dict["studyfield"])
        return {
            "studyfield": {
                "$ref": term.link_self
            }
        }

    # studyProgramme, studyField = study.split("/", 1)
    # studyField = studyField.strip()
    # studyProgramme = studyProgramme.strip()
    #
    # return {
    #     "studyProgramme": {"name": studyProgramme},
    #     "studyField": {"name": studyField}
    # }
