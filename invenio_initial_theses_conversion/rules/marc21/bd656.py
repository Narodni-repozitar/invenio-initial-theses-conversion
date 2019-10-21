import uuid

from invenio_db import db

from flask_taxonomies.models import Taxonomy
from flask_taxonomies.utils import find_in_json, find_in_json_contains
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
        return studyfield_ref(study.strip(), tax, grantor, doc_type)
    else:
        programme, field = study.split("/", maxsplit=1)
        field = field.strip()
        return studyfield_ref(field, tax, grantor, doc_type)


def studyfield_ref(study, tax, grantor, doc_type):
    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#sqlalchemy.dialects.postgresql.JSON
    # https://github.com/sqlalchemy/sqlalchemy/issues/3859  # issuecomment-441935478
    fields = find_in_json(study, tax, tree_address=("title", 0, "value")).all()
    # fields = tax.descendants.filter(
    #     TaxonomyTerm.extra_data[("title", 0, "value")].astext == study).all()
    if len(fields) == 0:
        fields = aliases(tax, study)
    if len(fields) == 0:
        field = find_in_json_contains(study, tax, "source_data").first()
        if field is None:
            not_valid = tax.get_term("no_valid_studyfield")
            slug = f"no_valid_{uuid.uuid4()}"
            field = not_valid.create_term(
                slug=slug,
                extra_data={
                    "title": {
                        "value": "Nevalidní obor nebo program",
                        "lang": "cze"
                    },
                    "source_data": study
                }
            )
            db.session.add(field)
            db.session.commit()
        return {
            "studyField": [{"$ref": link_self(tax.slug, field)}]
        }
    if len(fields) > 1:
        fields = filter(fields, doc_type, grantor)

    return {
        "studyField": [{"$ref": link_self(tax.slug, field)} for field in fields],

    }


def aliases(tax, study):
    fields = find_in_json(study, tax, tree_address="aliases").all()
    # fields = tax.descendants.filter(
    #     TaxonomyTerm.extra_data["aliases"].astext == study).all()
    if len(fields) == 0:
        # fields = tax.descendants.filter(
        #     TaxonomyTerm.extra_data["aliases"].contains([study])).all()
        fields = find_in_json_contains(study, tax, tree_address="aliases").all()
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
            "Navazující magisterský": "diplomove_prace",
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
