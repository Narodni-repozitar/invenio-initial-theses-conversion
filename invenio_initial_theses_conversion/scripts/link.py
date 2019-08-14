import os

reverse_path = []


def link_self(tax):
    SERVER_NAME = os.environ.get('SERVER_NAME')
    base = f"https://{SERVER_NAME}/api/taxonomies"
    taxonomy = tax.taxonomy.slug
    tree_path = tax.tree_path
    path = [base, taxonomy + tree_path]
    return "/".join(path)


# def recursive_parent(tax):
#     if tax.parent is not None:
#         reverse_path.append(tax.slug)
#         recursive_parent(tax)
#     else:
#         return reverse_path
