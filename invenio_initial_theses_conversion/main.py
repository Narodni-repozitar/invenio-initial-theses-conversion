import gzip
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import traceback
import uuid
from collections import Counter, defaultdict
from io import BytesIO
from logging import StreamHandler
from xml.etree import ElementTree

import click
import requests
from dojson.contrib.marc21.utils import split_stream, create_record
from marshmallow import ValidationError

from invenio_initial_theses_conversion.rules.model import old_nusl
from invenio_nusl_theses.marshmallow.json import ThesisMetadataSchemaV1

ERROR_DIR = "/tmp/import-nusl-theses"
IGNORED_ERROR_FIELDS = {"studyField", "studyProgramme", "degreeGrantor", "title", "dateAccepted"}
LANGUAGE_EXCEPTIONS = {"scc":"srp", "scr":"hrv" }


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
@click.option('--start',
            default=1)
def run(url, break_on_error, cache_dir, clean_output_dir, start):
    processed_ids = set()
    ses = session()
    if clean_output_dir and os.path.exists(ERROR_DIR):
        shutil.rmtree(ERROR_DIR)
    error_counts = Counter()
    error_documents = defaultdict(list)
    try:
        while True:
            print('\r%08d' % start, end='', file=sys.stderr)
            sys.stderr.flush()
            resp, parsed = fetch_nusl_data(url, start, cache_dir, ses)
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
                    for datafield in data:
                        fix_language(datafield, "041", "0", "7", "a")
                        fix_language(datafield, "520", " ", " ", "9")
                        fix_language(datafield, "540", " ", " ", "9")
                    transformed = old_nusl.do(create_record(data))
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
                except Exception as e :
                    logging.exception('Error in transformation')
                    if break_on_error:
                        raise

            start += count
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


def fix_language(datafield, tag, ind1, ind2, code):
    if datafield.attrib["tag"] == tag and datafield.attrib["ind1"] == ind1 and datafield.attrib["ind2"] == ind2:
        for subfield in datafield:
            if subfield.attrib["code"] == code:
                subfield.text = LANGUAGE_EXCEPTIONS.get(subfield.text, subfield.text)


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
