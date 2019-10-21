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
from flask import cli
from marshmallow import ValidationError

from invenio_initial_theses_conversion.rules.model import old_nusl
from invenio_initial_theses_conversion.utils import fix_language, fix_grantor, fix_keywords, split_stream_oai_nusl
from invenio_nusl_theses.marshmallow import ThesisMetadataSchemaV1
from invenio_nusl_theses.proxies import nusl_theses
from invenio_oarepo.current_api import current_api

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO) #logování SQLAlchemy
from invenio_records_draft.marshmallow import DraftSchemaWrapper

ERROR_DIR = "/tmp/import-nusl-theses"
IGNORED_ERROR_FIELDS = {"title", "dateAccepted", "language", "degreeGrantor",
                        "subject"}  # "studyProgramme", "studyField"


def path_safe(text):
    return "".join([c for c in text if re.match(r'\w', c)])


class NuslLogHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
        self.transformed = None
        self.recid = None

    def setRecord(self, record, recid):
        self.source_record = record
        self.recid = recid

    def setTransformedRecord(self, transformed):
        self.transformed = transformed

    def emit(self, record):
        msg = self.format(record)
        if self.recid:
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

        else:
            super().emit(record)


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


@click.command("initial-theses-conversion-chunks")
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
@click.option('--start',
              default=1)
@click.option('--stop')
@cli.with_appcontext
@click.pass_context
def run_chunks(ctx, url, break_on_error, cache_dir, clean_output_dir, start, stop):
    while True:
        start = int(start)
        ctx.forward(run, start=start, stop=stop)
        start += int(stop)


@click.command("initial-theses-conversion")
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
@click.option('--start',
              default=1)
@click.option('--stop',
              default=100000000000000)
@cli.with_appcontext
def run(url, break_on_error, cache_dir, clean_output_dir, start, stop):
    """
    Fetch data from old nusl and convert into new nusl as json.
    :param url: Url for data collection
    :param break_on_error: If true the script break at the error, oterwise it will log and continue with next record.
    :param cache_dir: Path to the cache directory
    :param clean_output_dir:
    :param start: Number of starting record
    :param stop: Number of records that will be fetched
    :return:
    """
    with current_api.app_context():
        _run(url, break_on_error, cache_dir, clean_output_dir, start, stop)


def _run(url, break_on_error, cache_dir, clean_output_dir, start, stop):
    processed_ids = set()
    if clean_output_dir and os.path.exists(ERROR_DIR):
        shutil.rmtree(ERROR_DIR)
    error_counts = Counter()
    error_documents = defaultdict(list)
    try:
        if "oai" in url:
            gen = url_nusl_data_generator(start, url, cache_dir, oai=True)
        elif url.startswith('http'):
            gen = url_nusl_data_generator(start, url, cache_dir)
        else:
            gen = file_nusl_data_generator(start, url, cache_dir)

        return data_loop_collector(break_on_error, error_counts, error_documents, gen, processed_ids, stop)

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


def data_loop_collector(break_on_error, error_counts, error_documents, gen, processed_ids, stop):
    i = 0
    for data in gen:
        i += 1
        if i >= int(stop):
            break

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
        marshmallowed = None
        try:
            # PŘEVOD XML NA GroupableOrderedDict
            rec = create_record(data)

            if rec.get('980__') and rec['980__'].get('a') not in (
                    # test jestli doctype je vysokoškolská práce, ostatní nezpracováváme
                    'bakalarske_prace',
                    'diplomove_prace',
                    'disertacni_prace',
                    'habilitacni_prace',
                    'rigorozni_prace'
            ):
                continue

            # Fix data before transformation into JSON
            rec = fix_language(rec)
            rec = fix_grantor(rec)  # Sjednocení grantora pod pole 7102
            rec = fix_keywords(rec)

            transformed = old_nusl.do(rec)  # PŘEVOD GroupableOrderedDict na Dict
            ch.setTransformedRecord(transformed)
            try:
                # Validace dat podle Marshmallow a JSON schematu
                marshmallowed = nusl_theses.validate(DraftSchemaWrapper(ThesisMetadataSchemaV1), transformed)
            except ValidationError as e:
                for field in e.field_names:
                    error_counts[field] += 1
                    error_documents[field].append(recid)
                if set(e.field_names) - IGNORED_ERROR_FIELDS:
                    raise
                continue

            # uložení do databáze/invenia
            nusl_theses.import_old_nusl_record(marshmallowed)
        except Exception as e:
            logging.exception('Error in transformation')
            logging.error('data %s', marshmallowed)
            if break_on_error:
                raise


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


def url_nusl_data_generator(start, url, cache_dir, oai=False):
    """

    :param start:
    :param url:
    :param cache_dir:
    :param oai:
    :return:
    """
    ses = session()
    token = None
    while True:
        print('\r%08d' % start, end='', file=sys.stderr)  # vytiskne červeně číslo záznamu (start)
        sys.stderr.flush()
        if not oai:
            resp, parsed = fetch_nusl_data(url, start, cache_dir,
                                           ses)  # return response of one record from server and parsed response
            stream_generator = split_stream(BytesIO(resp))
        else:
            resp, parsed, token = fetch_nusl_data(url, start, cache_dir,
                                                  ses, oai=True, res_token=token)
            stream_generator = split_stream_oai_nusl(BytesIO(resp))

        count = len(
            list(parsed.iter('{http://www.loc.gov/MARC21/slim}record')))  # return number of records from one response
        if count:
            for data in stream_generator:
                yield data
        start += count
        if token == "":
            break


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


def fetch_nusl_data(url, start, cache_dir, ses=requests.Session(), oai=False, res_token=None):
    """
    The function returns request response and parsed xml.
    :param url: Endpoint
    :param start:
    :param cache_dir: Directory where is saved cache
    :param ses: Request session
    :param oai: If the endpoint is oai: https://invenio.nusl.cz/oai2d/?verb=ListRecords&metadataPrefix=marcxml
    :param res_token: Resumption token that is responsible for pagination
    :return: Tuple with response, parsed XML (ElementTree) and resumptionToken
    """
    if oai:
        if res_token is None:
            full_url = f"{url}?verb=ListRecords&metadataPrefix=marcxml"
        else:
            full_url = f"{url}?verb=ListRecords&resumptionToken={res_token}"
    else:
        full_url = f'{url}&jrec={start}'  # full url address of concrete record
    # Reading from cache
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
    # if record is not present in cache
    resp = ses.get(full_url).content
    # save into cache
    if cache_dir:
        with gzip.open(cache_path, 'wb') as f:  # data compression
            f.write(resp)

    parsed = ElementTree.fromstring(resp)  # parsování XML

    # resumption token
    if oai:
        token = parsed.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken").text
    else:
        token = None

    return resp, parsed, token


if __name__ == '__main__':
    run()
