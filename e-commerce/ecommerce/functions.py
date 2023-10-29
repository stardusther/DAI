# Functions to fill the database with products from the API
import os

import requests
from pymongo import MongoClient
from django.http import HttpResponse

# App imports
from etienda import models as ecommerce_models
from django.conf import settings


def get_product_collection():
    """Get the product collection"""
    # Database connection
    # https://pymongo.readthedocs.io/en/stable/tutorial.html
    client = MongoClient('mongo', 27017)
    store_db = client.store  # Database
    return store_db.products  # Collection


def get_image(url, id):
    """Get image from url and store it in the static folder"""
    data = requests.get(url).content
    filename = f'img_{id}.jpg'
    path = os.path.join(settings.STATIC_ROOT, 'img', filename)
    with open(path, 'wb') as file:
        file.write(data)
    return os.path.join('img', filename)


def import_products(request):
    """Import products from the api if the database is empty"""
    product_collection = get_product_collection()
    if product_collection.count_documents({}) == 0:
        products = get_products()
        store_products(products)
        return HttpResponse("Imported " + str(get_product_collection().count_documents({}))
                        + " products")
    else:
        return HttpResponse("Database is already populated")


def store_products(products):
    """Stores the products in the database"""
    for prod in products:
        try:
            product = ecommerce_models.Product(**prod)  # Get the product JSON
            product.image = get_image(prod.get('image'),
                                      prod.get('id'))  # Override Url validator changing url type
            print("PRODUCT:", product.title, "\tCategory:", product.category, "\tImage:", product.image)
            get_product_collection().insert_one(product.model_dump())  # Insert the product
        except Exception as err:
            print('Something went wrong while storing the product -->', str(err))
            break
    return HttpResponse("Imported " + str(get_product_collection().count_documents({}))
                        + " products")


def fill_database(request):
    """Fill database with products from the api"""
    try:
        products = get_products()
        response = store_products(products)
    except Exception as err:
        response = print('Something went wrong while filling the database -->', str(err))
    return HttpResponse(response)


def truncate_database(request):
    """Delete database data"""
    try:
        client = MongoClient('mongo', 27017)
        client.store.products.drop()
    except Exception as err:
        print('Something went wrong while truncating the database -->', str(err))

    return HttpResponse("Database truncated")


def get_products():
    """Get products from the api

    https://requests.readthedocs.io/en/latest/
    """
    api = 'https://fakestoreapi.com/products'  # API to get products

    try:
        response = requests.get(api).json()
    except Exception as err:
        print("The API is down. Try again later")
        response = None
    return response


def print_total_price_by_category(bill):
    for category in bill:
        print("Category:", category.get('_id'), "\tTotal:", category.get('count'), "€")


def print_products(products, small):
    """Pretty print products"""
    print("Found", len(list(products.clone())), "!")  # Cloning cursor to avoid consuming it

    if small:
        for prod in products:
            print("PRODUCT: (" + str(prod.get('_id')) + ")",
                  prod.get('title'),
                  "\t[" + str(prod.get('price')) + "€]",
                  "\tCategory:", prod.get('category'),
                  "\tRating:", prod.get('rating').get('rate'))
    else:
        for prod in products:
            print("--------------------------------------")
            print("PRODUCT: (" + str(prod.get('_id')) + ")",
                  prod.get('title'),
                  "\t[" + str(prod.get('price')) + "€]",
                  "\nDESCRIPTION:", prod.get('description'))

