import gzip
import hashlib
import io
import json
import logging
import os
import re
import shutil
import sys
import traceback
import uuid
from collections import Counter, defaultdict
from io import BytesIO, RawIOBase, BufferedReader
from logging import StreamHandler
from xml.etree import ElementTree

import click
import requests
from dojson.contrib.marc21.utils import split_stream, create_record
from marshmallow import ValidationError

from invenio_initial_theses_conversion.rules.model import old_nusl
from invenio_nusl_theses.marshmallow.json import ThesisMetadataSchemaV1

ERROR_DIR = "/tmp/import-nusl-theses"
IGNORED_ERROR_FIELDS = {"studyField", "studyProgramme", "degreeGrantor", "title"}


def path_safe(text):
    return "".join([c for c in text if re.match(r'\w', c)])


class NuslLogHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        self.transformed = None

    def setRecord(self, record, recid):
        self.source_record = record
        self.recid = recid

    def setTransformedRecord(self, transformed):
        self.transformed = transformed

    def emit(self, record):
        msg = self.format(record)

        print(f'{msg} at {self.recid}')
        if not os.path.exists('/tmp/import-nusl-theses'):
            os.makedirs('/tmp/import-nusl-theses')

        with open(f'{ERROR_DIR}/{path_safe(self.recid)}.xml', 'w') as f:
            f.write(ElementTree.tostring(self.source_record, encoding='unicode', method='xml'))

        with open(f'{ERROR_DIR}/{path_safe(self.recid)}.txt', 'a') as f:
            print(f'{msg} at {self.recid}', file=f)

        if self.transformed:
            with open(f'{ERROR_DIR}/{path_safe(self.recid)}.json', 'w') as fp:
                json.dump(self.transformed, fp, indent=4, ensure_ascii=False)


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
@click.option('--clean-output-dir/--no-clean-output-dir',
              default=True)
def run(url, break_on_error, cache_dir, clean_output_dir):
    start = 1
    processed_ids = set()
    if clean_output_dir and os.path.exists(ERROR_DIR):
        shutil.rmtree(ERROR_DIR)
    error_counts = Counter()
    error_documents = defaultdict(list)
    try:
        if url.startswith('http'):
            gen = url_nusl_data_generator(start, url, cache_dir)
        else:
            gen = file_nusl_data_generator(start, url, cache_dir)

        for data in gen:

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
                rec = create_record(data)
                if rec.get('980__') and rec['980__'].get('a') not in (
                        'bakalarske_prace',
                        'diplomove_prace',
                        'disertacni_prace',
                        'habilitacni_prace',
                        'rigorozni_prace'
                ):
                    continue

                transformed = old_nusl.do(rec)
                ch.setTransformedRecord(transformed)
                schema = ThesisMetadataSchemaV1(strict=True)
                try:
                    marshmallowed = schema.load(transformed).data
                except ValidationError as e:
                    for field in e.field_names:
                        error_counts[field] += 1
                        error_documents[field].append(recid)
                    if set(e.field_names) - IGNORED_ERROR_FIELDS:
                        raise

                # TODO: validate marshmallowed via json schema

                # TODO: import to invenio
            except Exception as e:
                logging.exception('Error in transformation')
                if break_on_error:
                    raise

    finally:
        if not os.path.exists('/tmp/import-nusl-theses'):
            os.makedirs('/tmp/import-nusl-theses')
        print("Most frequent errors: ", )
        for error_field in error_counts.most_common():
            print(error_field, error_counts[error_field])
        with open(f'{ERROR_DIR}/error_documents.txt', 'a') as f:
            for error, recids in error_documents.items():
                print(error, file=f)
                print(" ".join([str(recid) for recid in recids]), file=f)
                print(" ", file=f)


def session():
    if False:
        i = 0
        while True:
            login = input("Enter your login: ")
            passwd = input("Enter your password: ")
            url = "https://invenio.nusl.cz/youraccount/login"
            payload = {
                "p_un": login,
                "p_pw": passwd
            }
            ses = requests.Session()
            page = ses.post(url, data=payload)
            if "Váš účet" in page.text:
                return ses
            else:
                print("Login or password were wrong. Please retry sign in again.")
                i += 1
            if i == 3:
                raise Exception("Your credentials was inserted three times wrong. Run program again.")
    else:
        return requests.Session()


def url_nusl_data_generator(start, url, cache_dir):
    ses = session()
    while True:
        print('\r%08d' % start, end='', file=sys.stderr)
        sys.stderr.flush()
        resp, parsed = fetch_nusl_data(url, start, cache_dir, ses)
        count = len(list(parsed.iter('{http://www.loc.gov/MARC21/slim}record')))
        if count:
            for data in split_stream(BytesIO(resp)):
                yield data
        start += count


def chain_streams(streams, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Chain an iterable of streams together into a single buffered stream.
    Usage:
        def generate_open_file_streams():
            for file in filenames:
                yield open(file, 'rb')
        f = chain_streams(generate_open_file_streams())
        f.read()
    """

    class ChainStream(RawIOBase):
        def __init__(self):
            self.leftover = b''
            self.stream_iter = iter(streams)
            try:
                self.stream = next(self.stream_iter)
            except StopIteration:
                self.stream = None

        def readable(self):
            return True

        def _read_next_chunk(self, max_length):
            # Return 0 or more bytes from the current stream, first returning all
            # leftover bytes. If the stream is closed returns b''
            if self.leftover:
                return self.leftover
            elif self.stream is not None:
                return self.stream.read(max_length)
            else:
                return b''

        def readinto(self, b):
            buffer_length = len(b)
            chunk = self._read_next_chunk(buffer_length)
            while len(chunk) == 0:
                # move to next stream
                if self.stream is not None:
                    self.stream.close()
                try:
                    self.stream = next(self.stream_iter)
                    chunk = self._read_next_chunk(buffer_length)
                except StopIteration:
                    # No more streams to chain together
                    self.stream = None
                    return 0  # indicate EOF
            output, self.leftover = chunk[:buffer_length], chunk[buffer_length:]
            b[:len(output)] = output
            return len(output)

    return BufferedReader(ChainStream(), buffer_size=buffer_size)


def file_nusl_data_generator(start, filename, cache_dir):
    while True:
        with gzip.open(filename, 'rb') as f:
            for data in split_stream(
                    chain_streams([BytesIO(b'<root xmlns="http://www.loc.gov/MARC21/slim">'), f, BytesIO(b'</root>')])):
                if not start % 1000:
                    print('\r%08d' % start, end='', file=sys.stderr)
                yield data
                start += 1


def fetch_nusl_data(url, start, cache_dir, ses):
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

    resp = ses.get(full_url).content
    if cache_dir:
        with gzip.open(cache_path, 'wb') as f:
            f.write(resp)

    parsed = ElementTree.fromstring(resp)

    return resp, parsed


if __name__ == '__main__':
    run()
