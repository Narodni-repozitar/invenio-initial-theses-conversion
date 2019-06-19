# from invenio_initial_theses_conversion.nusl_overdo import single_value, handled_values, merge_results
# from invenio_initial_theses_conversion.taxonomies.nusl_collections import institution_taxonomy
# from ..model import old_nusl
#
#
# @old_nusl.over('provider', '^998__')
# @handled_values('a')
# @single_value
# def provider(self, key, value):
#     institution = institution_taxonomy[value.get('a')]
#     if not institution:
#         pass# raise Exception('No institution for', value.get('a'))
#
#     return {
#         "id": {
#             "value": value.get('a'),
#             "type": "nusl"
#         },
#         "address": institution['address'],
#         # "contactPoint": {
#         #     "description": "vkladatel - email",
#         #     "type": "string"
#         # },
#         "name": [{
#             "name": institution['institution'],
#             "lang": "cze"
#         }],
#         "url": institution["url"],
#         # "provider": {
#         #     "type": "boolean"
#         # },
#         "isPartOf": [x for x in (institution['isPartOf2'], institution['isPartOf']) if x]
#     }
