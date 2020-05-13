from flask import cli

from invenio_initial_theses_conversion.stats.oai import OAIRunner
from invenio_nusl.cli import migration


# TODO: přesunout do nového modulu nusl-migration
@migration.command("es")
@cli.with_appcontext
def es():
    runner = OAIRunner()
    runner.run()
