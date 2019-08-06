from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.ext import StudyFieldsTaxonomy
from invenio_initial_theses_conversion.nusl_overdo import single_value, merge_results, extra_argument
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl


@old_nusl.over("studyProgramme", '^656_7')
@merge_results
@single_value
@extra_argument('grantor', '^7102', single=True)
@extra_argument('doc_type', '^980', single=True)
def studyProgramme_Field(self, key, value, grantor, doc_type):
    """Study programme."""
    doc_type = doc_type.get("a")
    grantor = grantor.get("a").lower()
    study = value.get("a")
    tax = Taxonomy.get("studyfields", required=True)
    studyprogramme_tax = Taxonomy.get("studyprogramme", required=True)
    if "/" not in study:
        return studyfield_ref(study, tax, studyprogramme_tax, grantor, doc_type)
    else:
        programme, field = study.split("/", maxsplit=1)
        field = field.strip()
        return studyfield_ref(field, tax, studyprogramme_tax, grantor, doc_type)


def studyfield_ref(study, tax, studyprogramme_tax, grantor, doc_type):
    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
    fields = tax.descendants.filter(
        TaxonomyTerm.extra_data[("name", 0, "name")].astext == study).all()
    if len(fields) == 0:
        fields = aliases(tax, study)
    if len(fields) == 0:
        raise NoResultFound
    codes = {field.slug for field in fields}
    result = StudyFieldsTaxonomy()
    result_dict = result.check_field(codes, grantor=grantor,
                                     doc_type=doc_type)
    studyfields = result_dict["studyfield"]
    studyprogrammes = result_dict["studyprogramme"]
    field_codes = []
    programme_codes = []
    for field in studyfields:
        studyfield = tax.get_term(field)
        field_codes.append(studyfield)
    for programme in studyprogrammes:
        studyprogramme = studyprogramme_tax.get_term(programme)
        programme_codes.append(studyprogramme)

    return {
        "studyfield": [{"$ref": link_self(field)} for field in field_codes],
        "studyprogramme": [{"$ref": link_self(programme)} for programme in programme_codes],

    }


def aliases(tax, study):
    fields = tax.descendants.filter(
        TaxonomyTerm.extra_data["aliases"].astext == study).all()
    if len(fields) == 0:
        fields = tax.descendants.filter(
            TaxonomyTerm.extra_data["aliases"].contains([study])).all()
    return fields
