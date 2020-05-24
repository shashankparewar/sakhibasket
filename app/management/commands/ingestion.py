"""
usage: ./manage.py ingest_category_tree {{space separated csv files}}
"""
import csv

from django.core.management.base import BaseCommand

import app.models
from app.utils.common_utils import CommonUtils


class Command(BaseCommand):
    help = 'Ingest Category Tree'

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str)

    def handle(self, *args, **options):
        for csv_file in options['csv_files']:
            ingestor = ProductIngestor()
            ingestor.ingest_tree(csv_file)


class ProductIngestor:
    """
    Product Ingestor
    """
    def __init__(self):
        self.valid_models = {}
        self.f_names = ["name",  "category",	"description",	"price"]
        self.result = {f_name: {} for f_name in self.f_names}

    def ingest_tree(self, csv_file):
        """
        Ingest products from csv file
        :param csv_file:
        :type csv_file:
        :return:
        :rtype:
        """
        print(csv_file)
        self.result["product"] = {}
        writer = open("product_formatted.csv", "w")
        with open(csv_file) as file:
            reader = csv.DictReader(file, fieldnames=self.f_names)
            dict_writer = csv.DictWriter(writer, fieldnames=["category", "product"])
            dict_writer.writeheader()
            for row in reader:
                if not self.is_valid_row(row):
                    continue
                print(row)
                category = row.pop("category")
                self.set_valid_category(category)
                product = dict(category=self.valid_models["category"])
                row["price"] = CommonUtils.type_cast_value(row["price"], "float")
                product.update(row)
                item, created = app.models.Item.objects.get_or_create(**product)
                self.valid_models["product"] = item
                self.result["product"][str(item)] = created
                dict_writer.writerow({key: value.name for key, value in self.valid_models.items()})
        writer.close()
        return self.result

    def ingest_category_from_name(self, display_name: str):
        """
        Ingest category from display name
        :param display_name:
        :type display_name:
        :return:
        :rtype:
        """
        display_name = display_name.strip()
        name = CommonUtils.get_name_from_display_name(display_name)
        model_dict = dict(display_name=display_name, name=name)
        obj, created = app.models.Category.objects.get_or_create(**model_dict)
        print(display_name, created)
        self.result["category"][display_name] = created
        return obj

    def set_valid_category(self, name):
        """
        Validate category
        :param name:
        :type name:
        :return:
        :rtype:
        """
        self.valid_models["category"] = self.ingest_category_from_name(name)
        return True

    @staticmethod
    def is_valid_row(row):
        """
        Validate row
        :param row:
        :type row:
        :return:
        :rtype:
        """
        if not row["name"] or not row["category"] or not row["price"]:
            return False
        return True
