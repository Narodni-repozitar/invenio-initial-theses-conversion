import csv
import functools
import os


class InstitutionTaxonomy:

    @property
    def institutions(cls):
        return cls._load_institutions()

    @functools.lru_cache(maxsize=1)
    def _load_institutions(cls):
        with open(os.path.join(os.path.dirname(__file__), 'institutions_ids.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar="'")
            institutions = {
                row['code']: row for row in csv_reader
            }
            return institutions

    def __getitem__(self, item):
        return self.institutions.get(item)


institution_taxonomy = InstitutionTaxonomy()
