from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from flask_taxonomies.utils import find_in_json
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
    university = find_in_json(uni_name, universities, tree_address=("title", 0, "value")).one_or_none()
    if university is not None:
        if item.get("g") is not None:
            faculty = fac_ref(item, university)
            if faculty is not None:
                if item.get("b") is not None:
                    department = department_ref(faculty, item)
                    if department is not None:
                        return [
                            {
                                "$ref": link_self(universities.slug, department)
                            }
                        ]

                no_department = universities.get_term(f"{faculty.slug}_no_department")
                return [
                    {
                        "$ref": link_self(universities.slug, no_department)
                    }
                ]

        no_department = universities.get_term(f"{university.slug}_no_faculty_no_department")
        return [
            {
                "$ref": link_self(universities.slug, no_department)
            }
        ]

    if provider is not None:
        uni_name = find_uni_name(provider)
        if uni_name is not None:
            return uni_ref(item, uni_name, universities)


def department_ref(faculty, item):
    department_name = item.get("b")
    department = find_in_json(department_name, faculty).first()
    # department = faculty.descendants.filter(
    #     TaxonomyTerm.extra_data[("title", 0, "value")].astext == department_name).first()
    return department


def fac_ref(item, university):
    fac_name = item.get("g")
    faculty = find_in_json(fac_name, university).all()
    # faculty = university.descendants.filter(
    #     TaxonomyTerm.extra_data[("title", 0, "value")].astext == fac_name).all()
    faculty = [fac for fac in faculty if fac.level == 3]
    if len(faculty) != 0:
        faculty = faculty[0]
    else:
        return None
    return faculty


def find_uni_name(provider):
    provider_tax = Taxonomy.get("provider", required=True)
    provider_term = provider_tax.descendants.filter(
        TaxonomyTerm.slug == provider).first()
    try:
        uni_name = provider_term.extra_data["title"][0]["value"] #TODO: je potřeba změnit, až bude více jazyků
    except KeyError:
        uni_name = None
    return uni_name
