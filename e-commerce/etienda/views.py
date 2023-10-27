from django.shortcuts import render
from django.http import HttpResponse

from ecommerce.functions import product_collection, get_products, store_products


def index(request):
    """Render index page"""
    context = {}
    return render(request, 'landing.html', context=None)


def get_products(category):
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
    import_products(request)

    # Filter products by category 'men's clothing'
    products = get_products('men\'s clothing')
    return render(request, 'products.html', context={'products': products})


def womens_clothing(request):
    """Get all women's clothing"""
    import_products(request)

    # Filter products by category 'men's clothing'
    products = get_products('women\'s clothing')
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

    result = product_collection.find({'$and': query})  # Operator 'and' needed in case there is a
    # query over the same field (p.e: price)

    if order is not None:  # Ordering the result
        result = result.sort(order)
    return result


def aggregate_by_product():
    """Simulate user buying all products"""
    pipeline = [
        {"$group": {"_id": "_id", "count": {"$sum": '$price'}}},
    ]
    return product_collection.aggregate(pipeline)


def aggregate_by_category():
    """Create an aggregation"""
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": '$price'}}},
    ]
    return product_collection.aggregate(pipeline)


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
            # "\nCATEGORY:", prod.get('category'),
            # "\nIMAGE:", prod.get('image'),
            # "\nRATING :", prod.get('rating').get('rate'))


def response_to_json(products):
    """Converts the response to json"""
    response = []
    for prod in products:
        response.append(prod)
    return response


def print_total_price_by_category(bill):
    for category in bill:
        print("Category:", category.get('_id'), "\tTotal:", category.get('count'), "€")


def import_products(request):
    """Import products from the api if the database is empty"""
    if product_collection.count_documents({}) == 0:
        products = get_products()
        store_products(products)
        return HttpResponse("Products imported")
    else:
        return HttpResponse("Database is already populated")


# EJERCICIO 1
def ejercicio1(request):
    import_products(request)
    print("Finding electronic products between 100 and 200 euros, sorted by price...")
    products = filter_product(None, None, 100, 200, None, "electronics", None, "price")
    response = response_to_json(products)
    return HttpResponse(response)


# EJERCICIO 2
def ejercicio2(request):
    import_products(request)
    print("Finding products containing the word 'pocket' in the description...")
    products = filter_product(None, None, None, None, 'Pocket', None, None, None)
    response = response_to_json(products)
    return HttpResponse(response)


# EJERCICIO 3
def ejercicio3(request):
    import_products(request)
    print("Finding products with a score greater than 4...")
    products = filter_product(None, None, None, None, None, None, 4, None)
    response = response_to_json(products)
    return HttpResponse(response)


# EJERCICIO 4
def ejercicio4(request):
    import_products(request)
    print("Finding men's clothing, sorted by rating...")
    products = filter_product(None, None, None, None, None, "men's clothing", None, 'rating.rate')
    response = response_to_json(products)
    return HttpResponse(response)


# EJERCICIO 5
def ejercicio5(request):
    import_products(request)
    total = list(aggregate_by_product())
    return HttpResponse("Total billed: " + str(total[0].get('count')) + "€")


# EJERCICIO 6
def ejercicio6(request):
    import_products(request)
    bill = aggregate_by_category()
    bill = response_to_json(bill)
    return HttpResponse("Total billed by category: " + str(bill))
