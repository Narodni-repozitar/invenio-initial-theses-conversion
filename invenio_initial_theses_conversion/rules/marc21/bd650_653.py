from functools import lru_cache
from urllib.parse import urlparse

from werkzeug.utils import cached_property

from flask_taxonomies.models import Taxonomy, TaxonomyTerm
from invenio_initial_theses_conversion.nusl_overdo import append_results, list_value, handled_values
from invenio_initial_theses_conversion.scripts.link import link_self
from invenio_nusl_taxonomies.utils import create_slug
from ..model import old_nusl


class Constants:
    @cached_property
    def subject_taxonomy(self):
        return Taxonomy.get("subject", required=True)

    @cached_property
    def keyword(self):
        return self.subject_taxonomy.get_term("keyword")

    @cached_property
    def mednas(self):
        return self.subject_taxonomy.get_term("mednas")

    @cached_property
    def czmesh(self):
        return self.subject_taxonomy.get_term("czmesh")

    @cached_property
    def psh(self):
        return self.subject_taxonomy.get_term("psh")

    @cached_property
    def czenas(self):
        return self.subject_taxonomy.get_term("czenas")


constants = Constants()


@old_nusl.over("subject", '^650_7')
@append_results
@list_value
@handled_values('0', '2', 'a', 'j', '7')
def subject(self, key, value):  # TODO: akceptovat term a vracet rovnou link
    """Subject."""
    subject_taxonomy = constants.subject_taxonomy
    extra_data = extra_data_dict(value)
    if extra_data.get("taxonomy") is not None:
        taxonomy = extra_data["taxonomy"]
        del extra_data["taxonomy"]
        if taxonomy.lower() == "mednas":
            parent_term = constants.mednas
            url = f"http://www.medvik.cz/link/{extra_data['id']}"
            return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url, id=extra_data["id"])
        elif taxonomy.lower() == "czmesh":
            parent_term = constants.czmesh
            url = f"http://www.medvik.cz/link/{extra_data['id']}"
            return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url, id=extra_data["id"])
        elif taxonomy.lower() == "psh":
            parent_term = constants.psh
            if "id" in extra_data:
                url = extra_data["id"]
                parsed_url = urlparse(url)
                url_array = parsed_url.path.split("/")
                id = url_array[-1]
                return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, url=url,
                                    id=id)
        elif taxonomy.lower() == "czenas":
            parent_term = constants.czenas
            if "id" in extra_data:
                id = extra_data["id"]
                return taxonomy_ref(value.get("a"), parent_term, extra_data, subject_taxonomy, id=id)
        else:
            raise ValueError("The taxonomy is not known.")
    else:
        raise ValueError("Taxonomy must be inserted!")


def taxonomy_ref(keyword, parent_term, extra_data=None, taxonomy=None, url=None, id=None, lang=None):
    if id is not None:
        subject = search_json_by_slug(id, parent_term)
    elif extra_data is None or extra_data.get("id") is None:
        if parent_term.slug == "keyword":
            subject = search_json_by_slug(create_slug(keyword), parent_term)
        else:
            subject = search_taxonomy_by_title(keyword, parent_term)
    else:
        id = extra_data["id"]
        subject = search_json_by_slug(id, parent_term)

    if len(subject) == 0:
        return
    if len(subject) == 1:
        return {
            "$ref": link_self(taxonomy.slug, subject[0])
        }

    if len(subject) > 0:
        raise ValueError(f"In taxonomy database is duplicate record: {keyword}. Please check taxonomies")


@lru_cache(maxsize=10000)
def search_taxonomy_by_title(keyword, parent_term):
    subject = parent_term.descendants.filter(
        TaxonomyTerm.extra_data["title"].contains([{"value": keyword}])).all()

    return subject


@lru_cache(maxsize=10000)
def search_json_by_slug(id, parent_term):
    subject = parent_term.descendants.filter(
        TaxonomyTerm.slug == id).all()
    return subject


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


@old_nusl.over("keywords", '^653')
@append_results
@list_value
@handled_values('a')
def keyword(self, key, value):
    """Subject."""
    if key == '653__':
        name = value.get("a")
        return {
            "name": name,
            "lang": "cze"
        }

    if key == '6530_':
        name = value.get("a")
        return {
            "name": name,
            "lang": "eng"
        }
