from flask import current_app
from werkzeug.utils import cached_property


class Constants:
    @cached_property
    def server_name(self):
        return current_app.config.get('SERVER_NAME')


constants = Constants()


def link_self(taxonomy_code, taxonomy_term):
    SERVER_NAME = constants.server_name
    base = f"https://{SERVER_NAME}/api/taxonomies"
    path = [base, taxonomy_code + "/" + taxonomy_term.slug]
    return "/".join(path)
