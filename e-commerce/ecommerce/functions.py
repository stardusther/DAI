# Functions to fill the database with products from the API
import requests
from pymongo import MongoClient
from django.http import HttpResponse

# App imports
from etienda import models as ecommerce_models
from django.conf import settings

# Database connection
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)
store_db = client.store  # Database
product_collection = store_db.products  # Collection
api = 'https://fakestoreapi.com/products'  # API to get products


def get_image(url, id):
    """Get image from url and store it in the static folder"""
    data = requests.get(url).content
    path = str(settings.STATIC_ROOT) + 'img_' + str(id) + '.jpg'
    file = open(path, 'wb')
    file.write(data)
    file.close()
    return path


def store_products(products):
    """Stores the products in the database"""
    for prod in products:
        try:
            product = ecommerce_models.Product(**prod)  # Get the product JSON
            product.image = get_image(prod.get('image'),
                                      prod.get('id'))  # Override Url validator changing url type
            product_collection.insert_one(product.model_dump())  # Insert the product
        except Exception as err:
            print('Something went wrong while storing the product -->', str(err))
            break
    return HttpResponse("Imported " + str(product_collection.count_documents({})) + " products")


def fill_database(request):
    """Fill database with products from the api"""
    try:
        products = get_products()
        print("PRODS", products)
        response = store_products(products)
    except Exception as err:
        response = print('Something went wrong while filling the database -->', str(err))
    return HttpResponse(response)


def truncate_database(request):
    """Delete database data"""
    try:
        client.store.products.drop()
    except Exception as err:
        print('Something went wrong while truncating the database -->', str(err))

    return HttpResponse("Database truncated")

def get_products():
    """Get products from the api

    https://requests.readthedocs.io/en/latest/
    """
    try:
        response = requests.get(api).json()
    except Exception as err:
        print("The API is down. Using decoy database")
        response = [{"id": 1, "title": "fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
                     "price": 109.95,
                     "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
                     "category": "men's clothing",
                     "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
                     "rating": {"rate": 3.9, "count": 120}},
                    {"id": 2, "title": "Mens Casual Premium Slim Fit T-Shirts ", "price": 22.3,
                     "description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. And Solid stitched shirts with round neck made for durability and a great fit for casual fashion wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.",
                     "category": "men's clothing",
                     "image": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
                     "rating": {"rate": 4.1, "count": 259}},
                    {"id": 3, "title": "Mens Cotton Jacket", "price": 55.99,
                     "description": "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing, cycling, traveling or other outdoors. Good gift choice for you or your family member. A warm hearted love to Father, husband or son in this thanksgiving or Christmas Day.",
                     "category": "men's clothing",
                     "image": "https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
                     "rating": {"rate": 4.7, "count": 500}},
                    {"id": 4, "title": "Mens Casual Slim Fit", "price": 15.99,
                     "description": "The color could be slightly different between on the screen "
                                    "and in practice. / Please note that body builds vary by "
                                    "person, therefore, detailed size information should be "
                                    "reviewed below on the product description.",
                     "category": "men's clothing",
                     "image": "https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
                     "rating": {"rate": 2.1, "count": 430}},
                    {"id": 5,
                     "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
                     "price": 695,
                     "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
                     "category": "jewelery",
                     "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg",
                     "rating": {"rate": 4.6,
                                "count": 400}},
                    ]
    return response
