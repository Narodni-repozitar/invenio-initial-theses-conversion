import csv
import functools
import os


class InstitutionTaxonomy:

    @property
    def institutions(cls):
        return cls._load_institutions()

    @functools.lru_cache(maxsize=1)
    def _load_institutions(cls):
        with open(os.path.join(os.path.dirname(__file__), 'institutions.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar="'")
            institutions = {
                row['code']: row for row in csv_reader
            }
        with open(os.path.join(os.path.dirname(__file__), 'institutions_hierarchy.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',', quotechar="'")
            for row in csv_reader:
                if row['code'] in institutions:
                    institutions[row['code']].update(row)
                else:
                    print('No institution for hierarchy code', row['code'])
            return institutions

    def __getitem__(self, item):
        return self.institutions.get(item)


institution_taxonomy = InstitutionTaxonomy()
