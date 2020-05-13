from flask import current_app
from werkzeug.utils import cached_property


class Constants:
    @cached_property
    def server_name(self):
        return current_app.config.get('SERVER_NAME')


constants = Constants()


def link_self(taxonomy_code, taxonomy_term=None, taxonomy_slug=None, parent=False):
    """
    Function returns reference to the taxonomy from taxonomy code and taxonomy term.
    :param taxonomy_code:
    :param taxonomy_term:
    :return:
    """

    SERVER_NAME = constants.server_name
    base = f"https://{SERVER_NAME}/api/taxonomies"
    if taxonomy_term and not taxonomy_slug:
        slug = taxonomy_term.slug
    elif not taxonomy_term and taxonomy_slug:
        slug = taxonomy_slug
    else:
        assert False, "Must insert taxonomy term or taxonomy slug, but you must not insert together"
    if not parent:
        path = [base, taxonomy_code + "/" + slug]
    else:
        path = [base, taxonomy_code + "/"]
    return "/".join(path)


def get_taxonomy_links(taxonomy, slug):
    self = link_self(taxonomy_code=taxonomy, taxonomy_slug=slug)
    parent = link_self(taxonomy_code=taxonomy, taxonomy_slug=slug, parent=True)
    return {
        "self": self,
        "tree": self + "/?drilldown=True",
        "parent": parent,
        "parent_tree": parent + "/?drilldown=True"
    }
