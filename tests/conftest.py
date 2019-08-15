# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# My site is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the API application."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from invenio_app.factory import create_api
from invenio_db import InvenioDB
from invenio_db import db as db_
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_records import InvenioRecords
from sqlalchemy_utils import create_database, database_exists

from flask_taxonomies import FlaskTaxonomies

from flask_taxonomies.views import blueprint as taxonomies_blueprint


@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return create_api


@pytest.yield_fixture()
def app():
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        JSONSCHEMAS_HOST="nusl.cz",
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="oarepo", pw="oarepo", url="127.0.0.1",
                                                                  db="oarepo")),
        SERVER_NAME='localhost',
    )
    InvenioJSONSchemas(app)
    InvenioRecords(app)
    InvenioDB(app)
    FlaskTaxonomies(app)
    with app.app_context():
        app.register_blueprint(taxonomies_blueprint)
        yield app

    shutil.rmtree(instance_path)


@pytest.yield_fixture()
def db(app):
    """Database fixture."""
    if not database_exists(str(db_.engine.url)):
        create_database(str(db_.engine.url))
    yield db_
