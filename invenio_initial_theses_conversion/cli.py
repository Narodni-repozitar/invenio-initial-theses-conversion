import click
from flask import cli

from invenio_initial_theses_conversion.stats.oai import OAIRunner


@click.command("nusl_stat")
@cli.with_appcontext
def nusl_stat():
    runner = OAIRunner()
    runner.run()
