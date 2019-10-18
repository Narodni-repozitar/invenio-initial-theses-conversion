def psh_term_filter(psh_list_terms, name):
    if len(psh_list_terms) == 0:
        return None
    matched_terms = []
    for term in psh_list_terms:
        match = False
        for dict in term.extra_data["title"]:
            for v in dict.values():
                if v == name:
                    match = True
        if match:
            matched_terms.append(term)
    if len(matched_terms) > 0:
        return matched_terms[0]
    return None
