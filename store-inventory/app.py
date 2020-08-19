# A Store Inventory
import csv
import datetime

from peewee import *

db = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = IntegerField(primary_key=True)
    product_name = CharField(max_length=255, unique=True)
    product_price = IntegerField(null=False)
    product_quantity = IntegerField(default=0)
    date_updated = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and table."""
    db.connect()
    db.create_tables([Product], safe=True)

if __name__ == '__main__':
    initialize()
