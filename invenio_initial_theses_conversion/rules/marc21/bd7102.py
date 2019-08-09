from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import handled_values, extra_argument
from ..model import old_nusl
from sqlalchemy.orm.exc import NoResultFound
from invenio_initial_theses_conversion.scripts.link import link_self


@old_nusl.over('degreeGrantor', '^7102_')
@handled_values('a', '9', 'g', 'b')
@extra_argument('provider', '^998__', single=True)
def degree_grantor(self, key, values, provider):
    provider = provider.get("a")
    universities = Taxonomy.get("universities", required=True)
    for item in values:
        if item.get("9") == "cze":
            uni_name = item.get("a")
            if uni_name is not None:
                return uni_ref(item, uni_name, universities, provider)



def uni_ref(item, uni_name, universities, provider=None):
    university = universities.descendants.filter(
        TaxonomyTerm.extra_data[("title", 0,
                                 "value")].astext == uni_name).one_or_none()  # TODO: bude se muset přepsat, takto hledám jen první položku pole
    if university is not None:
        if item.get("g") is not None:
            faculty = fac_ref(item, university)
            if faculty is not None:
                if item.get("b") is not None:
                    department = department_ref(faculty, item)
                    if department is not None:
                        return {
                                "$ref": link_self(department)
                            }

                return {
                        "$ref": link_self(faculty)
                }

        return {
                "$ref": link_self(university)
        }

    if provider is not None:
        uni_name = find_uni_name(provider)
        if uni_name is not None:
            return uni_ref(item, uni_name, universities)


def department_ref(faculty, item):
    department_name = item.get("b")
    department = faculty.descendants.filter(
        TaxonomyTerm.extra_data[("title", 0, "value")].astext == department_name).one_or_none()
    return department


def fac_ref(item, university):
    fac_name = item.get("g")
    faculty = university.descendants.filter(
        TaxonomyTerm.extra_data[("title", 0, "value")].astext == fac_name).one_or_none()
    return faculty


def find_uni_name(provider):
    provider_tax = Taxonomy.get("provider", required=True)
    provider_term = provider_tax.descendants.filter(
        TaxonomyTerm.slug == provider).first()
    try:
        uni_name = provider_term.extra_data["title"][0]["value"]
    except KeyError:
        uni_name = None
    return uni_name

#     ret = [
#         {
#             "university": {
#                 "$ref": "link",
#                 "faculties": [
#                     {
#                         "$ref": "link",
#                         "departments": []
#                     }
#                 ]
#             }
#         }
#     ]
#     provider = provider.get("a")
#     universities = Taxonomy.get("universities", required=True)
#     provider_tax = Taxonomy.get("provider", required=True)
#     for item in values:
#         if item.get("9") == "cze":
#             uni_name = item.get("a")
#             university = find_uni_taxonomy(uni_name, provider, provider_tax, universities)
#             uni_rid = university.extra_data["RID"]
#             ret[0]["university"]["$ref"] = link_self(university)
#
#             if item.get("g"):
#                 fac_name = item.get("g")
#                 faculty = university.descendants.filter(
#                     TaxonomyTerm.extra_data[("name", 0, "name")].astext == fac_name,
#                     TaxonomyTerm.extra_data["university_RID"] == uni_rid).one_or_none()
#                 if faculty is not None:
#                     ret[0]["university"]["faculties"][0]["$ref"] = link_self(faculty)
#                 else:
#                     del ret[0]["university"]["faculties"]
#                     continue
#             else:
#                 del ret[0]["university"]["faculties"]
#                 continue
#
#             if item.get("b"):
#                 ret[0]["university"]["faculties"][0]["departments"].append(item.get("b"))
#             else:
#                 del ret[0]["university"]["faculties"][0]["departments"]
#
#     return ret
#
#
# def find_uni_taxonomy(uni_name, provider, provider_tax, universities):
#     university = universities.descendants.filter(
#         TaxonomyTerm.extra_data[("name", 0, "name")].astext == uni_name).all()
#     if len(university) == 0 and provider is not None:
#         provider_term = provider_tax.descendants.filter(
#             TaxonomyTerm.slug == provider).first()
#         uni_name = provider_term.extra_data["name"][0]["name"]
#         university = find_uni_taxonomy(uni_name, provider, provider_tax, universities)
#     elif len(university) == 1:
#         university = university[0]
#     else:
#         raise NoResultFound
#     return university
