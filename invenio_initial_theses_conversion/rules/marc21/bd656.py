from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
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
    if "/" not in study:
        return studyfield_ref(study, tax, grantor, doc_type)
    else:
        programme, field = study.split("/", maxsplit=1)
        field = field.strip()
        return studyfield_ref(field, tax, grantor, doc_type)


def studyfield_ref(study, tax, grantor, doc_type):
    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
    fields = tax.descendants.filter(
        TaxonomyTerm.extra_data[("title", 0, "value")].astext == study).all()
    if len(fields) == 0:
        fields = aliases(tax, study)
    if len(fields) == 0:
        raise NoResultFound
    if len(fields) > 1:
        fields = filter(fields, doc_type, grantor)

    return {
        "studyfield": [{"$ref": link_self(field)} for field in fields],

    }


def aliases(tax, study):
    fields = tax.descendants.filter(
        TaxonomyTerm.extra_data["aliases"].astext == study).all()
    if len(fields) == 0:
        fields = tax.descendants.filter(
            TaxonomyTerm.extra_data["aliases"].contains([study])).all()
    return fields


def filter(fields, doc_type, grantor):
    fields = doc_filter(fields, doc_type)
    fields = grantor_filter(fields, grantor)
    return fields


def doc_filter(fields, doc_type):
    if doc_type is not None:
        degree_dict = {
            "Bakalářský": "bakalarske_prace",
            "Magisterský": "diplomove_prace",
            "Navazující magisterský": "diplomova_prace",
            "Doktorský": "disertacni_prace"
        }
        return [field for field in fields if degree_dict.get(field.extra_data.get("degree_level")) == doc_type]
    return fields


def grantor_filter(fields, grantor):
    if grantor is not None:
        matched_fields = [field for field in fields if
                          field.extra_data.get("grantor") is not None and field.extra_data["grantor"][0][
                              "university"].lower() == grantor]
        if len(matched_fields) == 0:
            return fields
        else:
            return matched_fields
    else:
        return fields
