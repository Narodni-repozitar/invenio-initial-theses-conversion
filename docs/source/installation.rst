#############
Instalace
#############

Z requirements.txt
###################

Je nutné mít nainstalované Invenio.
Instalace Invenia je popsaná v balíčku Invenio-Nusl.

Závislosti se nainstalují příkazem:

.. code-block:: console

    pip install -r requirements.txt

Všechny balíčky z requirements.txt by měly být ve stejné složce jako tento balík.

Import dat
###########

Taxonomie
-----------
Naimportují se všechny taxonomie do databáze:

.. code::

    invenio nusl taxonomies import_languages
    invenio nusl taxonomies import_doctype
    invenio nusl taxonomies import_providers
    invenio nusl taxonomies import_studyfields
    invenio nusl taxonomies import_universities
    invenio nusl taxonomies import_subject

Indexace taxonomii do Elasticsearch:

.. code::

    invenio taxonomies es reindex
