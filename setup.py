# -*- coding: utf-8 -*-


"""NUSL theses data model."""

import os

from setuptools import find_packages, setup

tests_require = [

]

setup_requires = [

]

install_requires = [
    'invenio-nusl-theses>=1.0.0',
    "dojson>=1.4.0"
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
            'b001 = invenio_initial_theses_conversion.rules.marc21.b001'
        ],
        'dojson.cli.rule':
            [
                'theses = invenio_initial_theses_conversion.rules.model:old_nusl'
            ]
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
# xd