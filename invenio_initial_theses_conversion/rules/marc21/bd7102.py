from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import handled_values, extra_argument
from ..model import old_nusl
from sqlalchemy.orm.exc import NoResultFound
from invenio_initial_theses_conversion.scripts.link import link_self


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
@extra_argument('provider', '^998__', single=True)
def degree_grantor(self, key, values, provider):
    ret = [
        {
            "university": {
                "$ref": "link",
                "faculties": [
                    {
                        "$ref": "link",
                        "departments": []
                    }
                ]
            }
        }
    ]

    universities = Taxonomy.get("universities", required=True)
    provider_tax = Taxonomy.get("provider", required=True)
    for item in values:
        if item.get("9") == "cze":
            uni_name = item.get("a")
            university = find_uni_taxonomy(uni_name, provider, provider_tax, universities)
            ret[0]["university"]["$ref"] = link_self(university)

            if item.get("g"):
                fac_name = item.get("g")
                faculty = university.descendants.filter(
                    TaxonomyTerm.extra_data[("name", 0, "name")].astext == fac_name).one()
                ret[0]["university"]["faculties"][0]["$ref"] = link_self(faculty)
            else:
                del ret[0]["university"]["faculties"]

            if item.get("b"):
                ret[0]["university"]["faculties"][0]["departments"].append(item.get("b"))
            else:
                del ret[0]["university"]["faculties"][0]["departments"]

        return ret


def find_uni_taxonomy(uni_name, provider, provider_tax, universities):
    university = universities.descendants.filter(
        TaxonomyTerm.extra_data[("name", 0, "name")].astext == uni_name).all()
    if len(university) == 0 and provider.get("a") is not None:
        provider_term = provider_tax.descendants.filter(
            TaxonomyTerm.slug == provider).one()
        uni_name = provider_term.extra_data["name"][0]["name"]
        find_uni_taxonomy(uni_name, provider, provider_tax, universities)
    elif len(university) == 1:
        university = university[0]
    else:
        raise NoResultFound
    return university
