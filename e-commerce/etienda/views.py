import os
from django.conf import settings
from django.shortcuts import render
from .forms import ProductForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from random import sample

# App imports
from ecommerce import functions as ecommerce_functions

import logging

logger = logging.getLogger(__name__)


def index(request):
    """Render index page"""
    ecommerce_functions.import_products(None)
    products = random_products()

    return render(request, 'products.html',
                  context={'categorias': get_categories(), 'products': products})


def random_products():
    """Get random set of 6 products from the database"""
    products = filter_product(
        None, None, None, None, None, None,
        None, None
    )

    random_products = []

    try:
        # Get a list of all products
        filtered_product_list = list(products)

        # Get 6 random products
        six_random_products = sample(filtered_product_list, 6)

        # Update is_media attribute
        for prod in six_random_products:
            prod = set_is_media(prod)
            random_products.append(prod)

        return random_products
    except Exception as e:
        logger.error(f'Error getting random products: {e}')
        return []


def set_is_media(prod):
    """Set is_media attribute to True if the product has an image"""
    if prod.get('image', None) is not None and prod['image']:  # Verify if the product has an image
        if prod['image'].startswith(settings.MEDIA_URL):  # Verify if the image is in the media folder
            prod['is_media'] = True
        else:
            prod['is_media'] = False
    else:  # If the product doesn't have an image
        prod['is_media'] = False

    return prod


def category(request, category):
    """Get products from the selected category"""
    product_collection = filter_product(None, None, None, None,
                                        None, category, None, None)
    products = []
    for prod in product_collection:
        logger.debug(f'Product: {prod}')
        prod = set_is_media(prod)
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
        prod = set_is_media(prod)
        products.append(prod)
    for prod in products_title:
        prod = set_is_media(prod)
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

    query = {}

    if _id is not None:
        query["id"] = _id

    if title is not None:
        query["title"] = {'$regex': title, "$options": 'i'}

    if min_price is not None:
        query["price"] = {"$gte": min_price}

    if max_price is not None:
        query["price"] = {"$lte": max_price}

    if score is not None:
        query["rating.rate"] = {"$gte": score}

    if description is not None:
        query["description"] = {'$regex': description, "$options": 'i'}

    if category is not None:
        query["category"] = {'$regex': f'^{category}', "$options": 'i'}

    try:
        result = ecommerce_functions.get_product_collection().find(query)
        if order is not None:
            result = result.sort(order)
        return result
    except Exception as e:
        logger.error(f'Error filtering products: {e}')
        return []


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


@staff_member_required  # Only for staff (superusers are considered staff)
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

                # Get image URL
                image_url = settings.MEDIA_URL + image.name
            else:
                image_url = None

            logger.info(f'Created prod\'s  image url: {image_url}')

            # Set product_data
            product_data = {
                'title': title,
                'price': float(price),
                'description': description,
                'category': category,
                'image': image_url,
                'rating': {
                    'rate': 0.0,
                    'count': 0
                }
            }

            # Create the product
            try:
                ecommerce_functions.get_product_collection().insert_one(product_data)
            except Exception as e:
                logger.error(f'Error creating product: {e}')
                messages.error(request, 'There was an error creating the product')
                return render(request, 'product_form.html',
                              {'form': form, 'categorias': get_categories()})

            # Redirect to index page and send a success message
            messages.success(request, 'The product has been successfully created')
            return index(request)  # Redirect to index page
    else:  # Render the form
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'categorias': get_categories()})
