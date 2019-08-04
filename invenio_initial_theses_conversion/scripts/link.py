def link_self(tax):
    def path_self(tax, path):
        path.append(tax.slug)
        if tax.level == 1:
            return path[::-1]
        if getattr(tax, "taxonomy", None) is not None:
            return path_self(tax.taxonomy, path)
        return path[::-1]

    base = "https://127.0.0.1:5000/api/taxonomies"
    path = []
    path = [base] + path_self(tax, path)
    return "/".join(path)