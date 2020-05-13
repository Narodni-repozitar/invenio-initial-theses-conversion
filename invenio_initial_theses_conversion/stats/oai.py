import os
import traceback
from datetime import datetime

from invenio_initial_theses_conversion import config
from invenio_initial_theses_conversion.stats.parsers import MarcXMLParser
from invenio_search import current_search_client
from sickle import Sickle


class OAIRunner:

    def __init__(self):
        self.index_name = config.NUSL_ES_INDEX
        self.path = self._get_log_path()

    @property
    def index(self):
        _index = self.index_name
        if not current_search_client.indices.exists(_index):
            current_search_client.indices.create(
                index=_index,
                ignore=400,
                body={}
            )
        return _index

    def run(self):
        timestamp = datetime.utcnow()
        sickle = Sickle('http://invenio.nusl.cz/oai2d/')
        sickle.class_mapping['ListRecords'] = MarcXMLParser
        sickle.class_mapping['GetRecord'] = MarcXMLParser
        records = sickle.ListRecords(metadataPrefix='marcxml')
        for record in records:
            try:
                current_search_client.index(
                    index=self.index,
                    id=record.marc_dict["001"],
                    body=record.marc_dict
                )
            except:
                exc_traceback = traceback.format_exc()
                print(exc_traceback)
                print("\n\n\n")
                file_name = f'{timestamp.strftime("%Y%m%dT%H%M%S")}.err'
                file_path = os.path.join(self.path, file_name)
                with open(file_path, "a") as f:
                    f.write(
                        f"Dictionary: {record.marc_dict}\n\n"
                        f"{exc_traceback}\n\n\n\n")
                continue

    def _get_log_path(self):
        if not os.path.exists(config.NUSL_LOG_DIR):
            os.makedirs(config.NUSL_LOG_DIR)
        return config.NUSL_LOG_DIR
