from pymongo import MongoClient
import requests
from PIL import Image
from pprint import pprint

import models as ecommerce_models

# Database connection
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)
store_db = client.store  # Database
product_collection = store_db.products  # Collection


# https://requests.readthedocs.io/en/latest/
def getProducts(api):
    """Get products from the api"""
    response = requests.get(api)
    return response.json()


def getImage(url):
    return Image.open(requests.get(url, stream=True).raw)


def storeProducts(products):
    """Stores the products in the database"""
    for prod in products:
        try:
            product = ecommerce_models.Product(**prod)  # Get the product JSON
            product.image = prod.get('image')  # Override Url validator changing url type
            product_collection.insert_one(product.model_dump())  # Insert the product
        except Exception as err:
            print('Something went wrong while storing the product -->', str(err))
            break
    print("Imported", product_collection.count_documents({}), "products")


def truncateDatabase():
    """Delete database data"""
    try:
        client.store.products.drop()
    except Exception as err:
        print('Something went wrong while truncating the database -->', str(err))


def filterProduct(_id, _title, min_price, max_price, _description, order):
    """Filter products by attribute"""
    result = product_collection

    if _id is not None:
        result = result.find({"id": _id})

    if _title is not None:
        result = result.find({"title": _title})

    if min_price is not None:
        result = result.find({"price": {"$gte": min_price}})

    if max_price is not None:
        result = result.find({"price": {"$lte": max_price}})

    if _description is not None:
        result = result.find({"description": {"$lte": max_price}})

    if order is not None:
        result = result.sort(order)
    return result