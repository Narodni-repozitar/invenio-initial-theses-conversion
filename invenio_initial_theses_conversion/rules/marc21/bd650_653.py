from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from invenio_initial_theses_conversion.scripts.link import link_self
from ..model import old_nusl
from invenio_nusl.cli import create_slug
from invenio_db import db
from urllib.parse import urlparse


@old_nusl.over("subject", '^650_7')
@append_results
@list_value
@handled_values('0', '2', 'a', 'j', '7')
def subject(self, key, value):
    """Subject."""
    subject_taxonomy = Taxonomy.get("subject", required=True)
    extra_data = extra_data_dict(value)
    if extra_data.get("taxonomy") is not None:
        taxonomy = extra_data["taxonomy"]
        if taxonomy.lower() == "mednas":
            parent_term = subject_taxonomy.get_term("MEDNAS")
            url = f"http://www.medvik.cz/link/{extra_data['id']}"
            return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url, id=extra_data["id"])
        elif taxonomy.lower() == "czmesh":
            parent_term = subject_taxonomy.get_term("CZMESH")
            url = f"http://www.medvik.cz/link/{extra_data['id']}"
            return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url, id=extra_data["id"])
        elif taxonomy.lower() == "psh":
            parent_term = subject_taxonomy.get_term("PSH")
            if "id" in extra_data:
                url = extra_data["id"]
                parsed_url = urlparse(url)
                url_array = parsed_url.path.split("/")
                id = url_array[-1]
                return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url,
                                    id=id)
        elif taxonomy.lower() == "czenas":
            parent_term = subject_taxonomy.get_term("CZENAS")
            if "id" in extra_data:
                id = extra_data["id"]
                return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, id=id)
        else:
            raise ValueError("The taxonomy is not known.")
    else:
        raise ValueError("Taxonomy must be inserted!")


def taxonomy_ref(keyword, parent_term, extra_data=None, taxonomy=None, url=None, id=None, lang=None):
    if id is not None:
        subject = parent_term.descendants.filter(
            TaxonomyTerm.slug == id).all()
    elif extra_data is None or extra_data.get("id") is None:
        subject = parent_term.descendants.filter(
            TaxonomyTerm.extra_data["title"].contains([{"value": keyword}])).all()
    else:
        id = extra_data["id"]
        subject = parent_term.descendants.filter(
            TaxonomyTerm.slug == id).all()

    if len(subject) == 0:
        slug = add_to_taxonomy(keyword, parent_term, extra_data=extra_data, id=id, url=url, lang=lang)
        subject = taxonomy.get_term(slug)

        return {
            "$ref": link_self(subject)
        }
    if len(subject) == 1:
        return {
            "$ref": link_self(subject[0])
        }

    if len(subject) > 0:
        raise ValueError(f"In taxonomy database is duplicate record: {keyword}. Please check taxonomies")


def extra_data_dict(value):
    if not value.get("a"):
        raise AttributeError("Subject name required (650_7a)")
    subject = {}
    if "a" in value:
        subject["title"] = [
            {
                "value": value.get("a"),
                "lang": "cze"
            }
        ]
    if "j" in value:
        if "title" not in subject:
            subject["title"] = [
                {
                    "value": value.get("j"),
                    "lang": "eng"
                }
            ]
        else:
            subject["title"].append(
                {
                    "value": value.get("j"),
                    "lang": "eng"
                }
            )
    if "0" in value:
        if "7" in value:
            raise AttributeError("Id and URL must not be present in single subject (650_70, 650_77)")
        subject["id"] = value.get("0")
    if "7" in value:
        subject["id"] = value.get("7")
    if "2" in value:
        subject["taxonomy"] = value.get("2")
    return subject


@old_nusl.over("subject", '^653')
@append_results
@list_value
@handled_values('a')
def subject(self, key, value):
    """Subject."""
    if key == '653__':
        keyword = value.get("a")
        subjects = Taxonomy.get("subject", required=True)
        parent_term = subjects.get_term("keyword")
        return taxonomy_ref(keyword, parent_term, lang="cze", taxonomy=subjects)

    if key == '6530_':
        keyword = value.get("a")
        subjects = Taxonomy.get("subject", required=True)
        parent_term = subjects.get_term("keyword")
        return taxonomy_ref(keyword, parent_term, lang="eng", taxonomy=subjects)


def add_to_taxonomy(keyword, taxonomy_term=None, extra_data=None, lang=None, id=None, url=None):
    if id is None:
        slug = create_slug(keyword)
    else:
        slug = id
    if extra_data is None:
        extra_data = {
            "title": [
                {
                    "value": keyword,
                    "lang": lang
                }
            ]
        }
    if id is not None:
        extra_data["id"] = id
    if url is not None:
        extra_data["url"] = url
    subject = taxonomy_term.create_term(
        slug=slug,
        extra_data=extra_data
    )
    db.session.add(subject)
    db.session.commit()
    return slug
