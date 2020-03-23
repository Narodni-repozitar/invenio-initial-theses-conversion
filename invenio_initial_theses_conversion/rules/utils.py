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