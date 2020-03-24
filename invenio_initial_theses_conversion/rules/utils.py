from urllib.parse import urlparse, urlunparse

from flask_taxonomies.utils import find_in_json

from flask_taxonomies_es.serializer import get_taxonomy_term


def db_search(query, tax, json_address=None):
    fields = find_in_json(query, tax, tree_address=json_address).all()
    fields = jsonify_fields(fields)
    return fields


def jsonify_fields(fields):
    new_fields = []
    for field in fields:
        new_fields.append(get_taxonomy_term(code=field.taxonomy.slug, slug=field.slug))
    fields = new_fields
    return fields


def get_ref_es(json_dict):
    # TODO: odebrat API až se vyřeší link_self
    taxonomy = json_dict["taxonomy"]
    url = urlparse(json_dict["links"]["self"])
    path_array = url.path.split("/")
    path_array = [node for node in path_array if len(node) > 0]
    if path_array[0] != "api":
        path_array = ["api", *path_array]
    slug = path_array[-1]
    taxonomy_index = path_array.index(taxonomy)
    path_array = [*path_array[:taxonomy_index + 1], slug]
    path = "/" + "/".join(path_array)
    url = url._replace(path=path)
    return {
        "$ref": urlunparse(url)
    }
