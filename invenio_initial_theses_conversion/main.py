import logging
import os
import re
import sys
import uuid
from io import BytesIO
from logging import StreamHandler
from xml.etree import ElementTree

import click
import requests
from dojson.contrib.marc21.utils import split_stream, create_record

from invenio_initial_theses_conversion.rules.model import old_nusl


def path_safe(text):
    return "".join([c for c in text if re.match(r'\w', c)])


class NuslLogHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)

    def setRecord(self, record):
        self.source_record = record

    def emit(self, record):
        msg = self.format(record)
        recid = None
        for cf in self.source_record.iter('{http://www.loc.gov/MARC21/slim}controlfield'):
            if cf.attrib['tag'] == '001':
                recid = cf.text
                break
        else:
            recid = str(uuid.uuid4())

        print(f'{msg} at {recid}')
        if not os.path.exists('/tmp/import-nusl-theses'):
            os.makedirs('/tmp/import-nusl-theses')

        with open(f'/tmp/import-nusl-theses/{path_safe(recid)}.xml', 'w') as f:
            f.write(ElementTree.tostring(self.source_record, encoding='unicode', method='xml'))

        with open(f'/tmp/import-nusl-theses/{path_safe(recid)}.txt', 'a') as f:
            print(f'{msg} at {recid}', file=f)


ch = NuslLogHandler()
ch.setLevel(logging.INFO)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
    handlers=[
        ch
    ]
)


@click.command()
@click.option('--url',
              default='https://invenio.nusl.cz/search?ln=cs&p=&f=&action_search=Hledej&c=Vysoko%C5%A1kolsk%C3%A9+kvalifika%C4%8Dn%C3%AD+pr%C3%A1ce&rg=1000&sc=0&of=xm',
              help='Collection URL')
@click.option('--break-on-error/--no-break-on-error',
              default=True,
              help='Break on first error')
def run(url, break_on_error):
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
            ch.setRecord(data)
            try:
                transformed = old_nusl.do(create_record(data))
            except:
                logging.exception('Error in transformation')
                if break_on_error:
                    raise

            # TODO: validate

            # TODO: import to invenio

        start += count


if __name__ == '__main__':
    run()
