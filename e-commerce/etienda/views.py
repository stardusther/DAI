import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib import messages

# App imports
from ecommerce import functions as ecommerce_functions
from etienda import models as etienda_models


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

    result = ecommerce_functions.get_product_collection().find(
        {'$and': query})  # Operator 'and' needed in case there is a
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


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the data from the form
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']

            # Get uploaded image
            image = request.FILES.get('image', None)
            # Store in static folder
            if image:
                file_path = os.path.join(settings.MEDIA_ROOT, image.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

                # Obtener la URL de la imagen
                image_url = settings.MEDIA_ROOT + image.name
            else:
                image_url = None

            # Set product_data
            product_data = {
                'title': title,
                'price': float(price),
                'description': description,
                'category': category,
                'image': image_url,
                'rating': {
                    'rate': 0.0,
                    'count': 1
                }
            }

            # Create the product
            ecommerce_functions.get_product_collection().insert_one(product_data)

            # Redirect to index page and send a success message
            messages.success(request, 'The product has been successfully created')
            return render(request, 'landing.html', context={'categorias': get_categories()})
    else:  # Render the form
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'categorias': get_categories()})
