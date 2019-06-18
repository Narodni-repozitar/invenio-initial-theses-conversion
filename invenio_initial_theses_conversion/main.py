import gzip
import hashlib
import logging
import os
import re
import sys
import traceback
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

    def setRecord(self, record, recid):
        self.source_record = record
        self.recid = recid

    def emit(self, record):
        msg = self.format(record)

        print(f'{msg} at {self.recid}')
        if not os.path.exists('/tmp/import-nusl-theses'):
            os.makedirs('/tmp/import-nusl-theses')

        with open(f'/tmp/import-nusl-theses/{path_safe(self.recid)}.xml', 'w') as f:
            f.write(ElementTree.tostring(self.source_record, encoding='unicode', method='xml'))

        with open(f'/tmp/import-nusl-theses/{path_safe(self.recid)}.txt', 'a') as f:
            print(f'{msg} at {self.recid}', file=f)


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
@click.option('--cache-dir',
              help='Cache dir')
@click.option('--break-on-error/--no-break-on-error',
              default=True,
              help='Break on first error')
def run(url, break_on_error, cache_dir):
    start = 1
    processed_ids = set()
    while True:
        print('\r%08d' % start, end='', file=sys.stderr)
        sys.stderr.flush()
        resp, parsed = fetch_nusl_data(url, start, cache_dir)
        count = len(list(parsed.iter('{http://www.loc.gov/MARC21/slim}record')))
        if not count:
            break

        for data in split_stream(BytesIO(resp)):

            for cf in data.iter('{http://www.loc.gov/MARC21/slim}controlfield'):
                if cf.attrib['tag'] == '001':
                    recid = cf.text
                    break
            else:
                recid = str(uuid.uuid4())
            
            ch.setRecord(data, recid)

            if recid in processed_ids:
                logging.warning('Record with id %s already parsed, probably end of stream', recid)
                return

            processed_ids.add(recid)

            try:
                transformed = old_nusl.do(create_record(data))

                # TODO: validate via marshmallow

                # TODO: validate marshmallowed via json schema

                # TODO: import to invenio
            except:
                logging.exception('Error in transformation')
                if break_on_error:
                    raise

        start += count


def fetch_nusl_data(url, start, cache_dir):
    full_url = f'{url}&jrec={start}'
    if cache_dir:
        hash_val = hashlib.sha512(full_url.encode('utf-8')).hexdigest()
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_path = os.path.join(cache_dir, hash_val)
        if os.path.exists(cache_path):
            try:
                with gzip.open(cache_path, 'rb') as f:
                    ret = f.read()
                    parsed = ElementTree.fromstring(ret)
                    return ret, parsed
            except:
                traceback.print_exc()
            
    resp = requests.get(full_url).content
    if cache_dir:
        with gzip.open(cache_path, 'wb') as f:
            f.write(resp)

    parsed = ElementTree.fromstring(resp)

    return resp, parsed


if __name__ == '__main__':
    run()
