import json
import logging
import os
import shutil
import uuid

import click
from dojson.contrib.marc21.utils import create_record
from flask import cli

from invenio_initial_theses_conversion.main import url_nusl_data_generator, file_nusl_data_generator
from invenio_initial_theses_conversion.utils import fix_grantor

ERROR_DIR = "/tmp/import-nusl-theses"


@click.command("collect-org-units")
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
@cli.with_appcontext
def run(url, break_on_error, cache_dir, clean_output_dir, start):
    org_units = set()
    processed_ids = set()
    if clean_output_dir and os.path.exists(ERROR_DIR):
        shutil.rmtree(ERROR_DIR)

    if url.startswith('http'):
        gen = url_nusl_data_generator(start, url, cache_dir)
    else:
        gen = file_nusl_data_generator(start, url, cache_dir)
    try:
        for data in gen:

            for cf in data.iter('{http://www.loc.gov/MARC21/slim}controlfield'):
                if cf.attrib['tag'] == '001':
                    recid = cf.text
                    break
            else:
                recid = str(uuid.uuid4())

            if recid in processed_ids:
                logging.warning('Record with id %s already parsed, probably end of stream', recid)
                return

            processed_ids.add(recid)
            try:
                rec = create_record(data)
                rec = fix_grantor(rec)
                if "7102_" not in rec:
                    continue
                for org_unit in aslist(rec["7102_"]):
                    if not isinstance(org_unit, dict):
                        print(org_unit, recid)
                        continue
                    university = org_unit.get("a")
                    faculty = org_unit.get("g")
                    department = org_unit.get("b")
                    language = org_unit.get("9")

                    if faculty and not university:
                        logging.error("No university for faculty: %s", rec)
                        continue
                    if department and not faculty:
                        logging.error("No faculty for department: %s", rec)
                        continue

                    org_units.add((university, faculty, department, language))



            except Exception as e:
                logging.exception('Error in transformation')
                if break_on_error:
                    raise
    finally:
        with open("departments.json", "w") as f:
            json.dump(list(org_units), f)


def aslist(x):
    if isinstance(x, (tuple, list)):
        return x
    else:
        return [x]
