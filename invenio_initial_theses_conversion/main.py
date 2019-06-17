from io import StringIO, BytesIO

import click
import requests
from xml.etree import ElementTree

import sys
from dojson.contrib.marc21.utils import split_stream, create_record

from invenio_initial_theses_conversion.rules.model import old_nusl


@click.command()
@click.option('--url',
              default='https://invenio.nusl.cz/search?ln=cs&p=&f=&action_search=Hledej&c=Vysoko%C5%A1kolsk%C3%A9+kvalifika%C4%8Dn%C3%AD+pr%C3%A1ce&rg=1000&sc=0&of=xm',
              help='Number of greetings.')
def run(url):
    start = 1
    while True:
        print('\r%08d' % start, end='', file=sys.stderr)
        sys.stderr.flush()
        resp = requests.get(f'{url}&jrec={start}').content
        parsed = ElementTree.fromstring(resp)
        count = len(list(parsed.iter('{http://www.loc.gov/MARC21/slim}record')))
        if not count:
            break

        for data in split_stream(BytesIO(resp)):
            transformed = old_nusl.do(create_record(data))
            # TODO: validate

            # TODO: import to invenio

        start += count


if __name__ == '__main__':
    run()
