# -*- coding: utf-8 -*-


"""NUSL theses data model."""

from setuptools import find_packages, setup

tests_require = [
    "pytest"
]

setup_requires = [

]

install_requires = [
    'invenio-nusl-theses>=1.0.0',
    "dojson>=1.4.0",
    "langdetect",
    "pycountry",
    'click',
    'requests',
    'flask',
    'marshmallow'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
version = "1.0.0"

setup(
    name='invenio-initial-theses-conversion',
    version=version,
    description=__doc__,
    # long_description=,
    keywords='nusl Invenio theses initial conversion',
    license='MIT',
    author='Daniel Kopecký',
    author_email='Daniel.Kopecky@techlib.cz',
    url='',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_initial_theses_conversion.rules.marc21': [
            'b001 = invenio_initial_theses_conversion.rules.marc21.b001',
            'bd24500 = invenio_initial_theses_conversion.rules.marc21.bd24500',
            'bd586 = invenio_initial_theses_conversion.rules.marc21.bd586',
            'bd656 = invenio_initial_theses_conversion.rules.marc21.bd656',
            'bd650_653=invenio_initial_theses_conversion.rules.marc21.bd650_653',
            'bd04107=invenio_initial_theses_conversion.rules.marc21.bd04107',
            'bd046xx=invenio_initial_theses_conversion.rules.marc21.bd046xx',
            'bd980 = invenio_initial_theses_conversion.rules.marc21.bd980',
            'bd996 = invenio_initial_theses_conversion.rules.marc21.bd996',
            'bd24633 = invenio_initial_theses_conversion.rules.marc21.bd24633',
            'bd598 = invenio_initial_theses_conversion.rules.marc21.bd598',
            'bd7102 = invenio_initial_theses_conversion.rules.marc21.bd7102',
            'bd005=invenio_initial_theses_conversion.rules.marc21.bd005',
            'bd300xx=invenio_initial_theses_conversion.rules.marc21.bd300xx',
            'bd520=invenio_initial_theses_conversion.rules.marc21.bd520',
            'bd540=invenio_initial_theses_conversion.rules.marc21.bd540',
            'bd998 = invenio_initial_theses_conversion.rules.marc21.bd998',
            'bd720=invenio_initial_theses_conversion.rules.marc21.bd720',
            'identifiers=invenio_initial_theses_conversion.rules.marc21.identifiers',
            'bd502=invenio_initial_theses_conversion.rules.marc21.bd502'
        ],
        'dojson.cli.rule':
            [
                'theses = invenio_initial_theses_conversion.rules.model:old_nusl'
            ],

        'flask.commands': [
            'initial_theses_conversion = invenio_initial_theses_conversion.main:run',
            'initial_theses_conversion_chunks = invenio_initial_theses_conversion.main:run_chunks',
            'collect-org-units = invenio_initial_theses_conversion.extract_departments:run'
        ],
    },
    # extras_require=,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Planning',
    ],
)
