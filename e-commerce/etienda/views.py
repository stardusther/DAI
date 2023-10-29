from django.shortcuts import render
from django.http import HttpResponse

from ecommerce import functions as ecommerce_functions


def index(request):
    """Render index page"""
    context = {}
    return render(request, 'landing.html', context=None)


def get_products_from(category):
    """Get products from the selected category"""
    product_collection = filter_product(None, None, None, None, None, category, None, None)
    products = []
    for prod in product_collection:
        products.append(prod)
    return products


def categories(request):  # TODO: migración inicial de datos
    """Render categories page"""
    import_products(request)

    # Get all categories from the database
    prod_categories = aggregate_by_category()
    categories = []
    for category in prod_categories:
        categories.append(category.get('_id'))

    return render(request, 'categories.html', context={'categories': categories})


def mens_clothing(request):
    """Get all men's clothing"""
    ecommerce_functions.import_products(request)

    # Filter products by category 'men's clothing'
    products = get_products_from('men\'s clothing')
    return render(request, 'products.html', context={'products': products})


def womens_clothing(request):
    """Get all women's clothing"""
    ecommerce_functions.import_products(request)

    # Filter products by category 'men's clothing'
    products = get_products_from('women\'s clothing')
    return render(request, 'products.html', context={'products': products})


def filter_request(request):
    """Filter products by attribute"""
    # Get parameters from the request
    _id = request.GET.get('id', None)
    title = request.GET.get('title', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    description = request.GET.get('description', None)
    category = request.GET.get('category', None)
    score = request.GET.get('score', None)
    order = request.GET.get('order', None)

    # Get products from the database
    products = filter_product(_id, title, min_price, max_price, description, category, score, order)

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





