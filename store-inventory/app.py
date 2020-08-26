# A Store Inventory
from collections import OrderedDict
import csv
import datetime
import os

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


def add_products():
    for product in product_list:
        try:
            Product.create(product_name=product['product_name'],
                           product_price=product['product_price'],
                           product_quantity=product['product_quantity'],
                           date_updated=product['date_updated'])
        except IntegrityError:
            product_record = Product.get(product_name=product['product_name'])
            product_record.product_price = product['product_price']
            product_record.product_quantity = product['product_quantity']
            product_record.date_updated = product['date_updated']
            product_record.save()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        try:
            choice = input('Action: ').lower().strip()
            if choice in menu:
                clear()
                menu[choice]()
            if choice not in menu and choice != 'q':
                raise ValueError
        except ValueError:
            print("\nThat is not a valid entry. Please select 'v', 'a', or 'b'\n")


def view_entry():
    """View product entry by product_id."""
    view_record = True

    while view_record:
        pass

def add_entry():
    """Add product entry."""
    add_record = True

    while add_record:
        try:
            prod_name = input("Please provide a product name. ").title()
            if prod_name.isnumeric():
                raise TypeError
            prod_quantity = input("\nHow many {} would you like? ".format(prod_name))
            if prod_quantity.isalpha():
                raise TypeError
            prod_price = input("\nWhat is the price of {}? ".format(prod_name))
            if '.' in prod_price or '$' in prod_price:
                prod_price = prod_price.replace('.', '').replace('$', '')
            if '.' not in prod_price and '$' not in prod_price and len(prod_price) >= 1:
                prod_price = prod_price + '00'
            if prod_price.isalpha():
                raise TypeError
            add_product = input("\nAdd product to the database? [Y]es/[N]o ")
            if add_product.lower() in ['y', 'yes']:
                try:
                    Product.create(product_name=prod_name,
                                   product_price=int(prod_price),
                                   product_quantity=prod_quantity)
                except IntegrityError:
                    product_record = Product.get(product_name=prod_name)
                    product_record.product_quantity = prod_quantity
                    product_record.product_price = int(prod_price)
                    product_record.date_updated = datetime.datetime.now()
                    product_record.save()
                    print("\nSaved successfully!\n")
                    break
            else:
                break
        except TypeError:
            print("\nNot a valid entry.\n")


def backup_csv():
    """Backup the database to a CSV file."""
    with open('backup_inventory.csv', 'w', newline='') as csvfile:
        backup_writer = csv.writer(csvfile)
        product_backup = Product.select(Product.product_name, Product.product_price,
                                        Product.product_quantity, Product.date_updated)

        backup_writer.writerow(product.keys())
        backup_writer.writerows(product_backup.tuples())

menu = OrderedDict([
    ('v', view_entry),
    ('a', add_entry),
    ('b', backup_csv)
])

if __name__ == '__main__':
    with open('inventory.csv', newline='') as csvfile:
        product_read = csv.DictReader(csvfile)
        product_list = list(product_read)
        for product in product_list:
            product['product_quantity'] = int(product['product_quantity'])
            product['product_price'] = int(product['product_price'].replace('$', '').replace('.', ''))
            product['date_updated'] = datetime.datetime.strptime(product['date_updated'], '%m/%d/%Y')

    initialize()
    add_products()
    menu_loop()
