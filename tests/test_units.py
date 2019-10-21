from invenio_initial_theses_conversion.main import fetch_nusl_data, url_nusl_data_generator
import shutil
import os


def test_fetch_nusl_data():
    cache = "/tmp/cache"

    if os.path.isdir(cache):
        shutil.rmtree('/tmp/cache')
    print(fetch_nusl_data("https://invenio.nusl.cz/oai2d/", 1, "/tmp/cache",
                          oai=True)[2])


def test_url_nusl_data_generator():
    cache = "/tmp/cache"

    if os.path.isdir(cache):
        shutil.rmtree('/tmp/cache')
    gen = url_nusl_data_generator(1, "https://invenio.nusl.cz/oai2d/?verb=ListRecords&metadataPrefix=marcxml", "/tmp/cache",
                            oai=True)
    for data in gen:
        print(data)
