from django.shortcuts import render
from django.http import HttpResponse

from ecommerce import functions as ecommerce_functions


def index(request):
    """Render index page"""
    ecommerce_functions.import_products(None)

    return render(request, 'landing.html', context={'categorias': get_categories()})


def category(request, category):
    """Get products from the selected category"""
    product_collection = filter_product(None, None, None, None,
                                        None, category, None, None)
    products = []
    for prod in product_collection:
        products.append(prod)
    return render(request, 'products.html', context={'categorias': get_categories(),
                                                     'category': category, 'products': products})


def get_categories():  # TODO: migración inicial de datos
    """Render categories page"""
    # Get all categories from the database
    prod_categories = aggregate_by_category()
    categories = []
    for category in prod_categories:
        categories.append(category.get('_id'))
    return categories


def filter_request(request):
    """Filter products by attribute"""
    # # Get parameters from the request
    # _id = request.GET.get('id', None)
    # title = request.GET.get('title', None)
    # min_price = request.GET.get('min_price', None)
    # max_price = request.GET.get('max_price', None)
    # description = request.GET.get('description', None)
    # category = request.GET.get('category', None)
    # score = request.GET.get('score', None)
    # order = request.GET.get('order', None)
    search_term = request.GET.get('search_term', None)

    # Get products from the database (filtered by description
    products_desc = filter_product(None, None, None, None,
                                   search_term, None, None, None)
    # Get products from the database (filtered by title)
    products_title = filter_product(None, search_term, None, None,
                                    None, None, None, None)

    # Merge both lists
    products = []
    for prod in products_desc:
        products.append(prod)
    for prod in products_title:
        if prod not in products:
            products.append(prod)

    # Render products
    return render(request, 'products.html', context={'products': products})


def filter_product(_id, title, min_price, max_price, description, category, score, order):
    """Filter products by attribute

    :param _id:
    :param title:
    :param min_price:
    :param max_price:
    :param description:
    :param category:
    :param score:
    :param order:

    """
    query = []

    if _id is not None:
        query.append({"id": _id})

    if title is not None:
        query.append({"title": title})

    if min_price is not None:
        query.append({"price": {"$gte": min_price}})

    if max_price is not None:
        query.append({"price": {"$lte": max_price}})

    if score is not None:
        query.append({"rating.rate": {"$gte": score}})

    if description is not None:  # Case-insensitive
        query.append({'description': {'$regex': description, "$options": 'i'}})

    if category is not None:  # Case-insensitive
        query.append({'category': {'$regex': f'^{category}', "$options": 'i'}})

    result = ecommerce_functions.get_product_collection().find({'$and': query})  # Operator 'and' needed in case there is a
    # query over the same field (p.e: price)

    if order is not None:  # Ordering the result
        result = result.sort(order)
    return result


def aggregate_by_product():
    """Simulate user buying all products"""
    pipeline = [
        {"$group": {"_id": "_id", "count": {"$sum": '$price'}}},
    ]
    return ecommerce_functions.get_product_collection().aggregate(pipeline)


def aggregate_by_category():
    """Create an aggregation"""
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": '$price'}}},
    ]
    return ecommerce_functions.get_product_collection().aggregate(pipeline)





