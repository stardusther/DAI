import views as ecommerce_views

# Set the api URL for the
api = 'https://fakestoreapi.com/products'

ecommerce_views.truncate_database()  # Empty database

print("Importing database from:", api)
products = ecommerce_views.get_products(api)
ecommerce_views.store_products(products)  # Fill database
print("////////////////////////////////////////////////////////////////////////////////////////////")
print("Finding electronic products between 100 and 200 euros, sorted by price...")
ecommerce_views.print_products(ecommerce_views.filter_product(None, None, 100, 200, None, None, None,
                                                             'price'), True)
print("////////////////////////////////////////////////////////////////////////////////////////////")
print("Finding products containing the word 'pocket' in the description...")
ecommerce_views.print_products(ecommerce_views.filter_product(None, None, None, None, 'Pocket', None,
                                                             None, None), False)
print("////////////////////////////////////////////////////////////////////////////////////////////")

print("Finding products with a score greater than 4...")
ecommerce_views.print_products(ecommerce_views.filter_product(None, None, None, None, None, None, 4,
                                                             None), True)
print("////////////////////////////////////////////////////////////////////////////////////////////")

print("Finding men's clothing, sorted by rating...")
ecommerce_views.print_products(ecommerce_views.filter_product(None, None, None, None, None,
                                                             "men's clothing", None,
                                                             'rating.rate'), True)
print("////////////////////////////////////////////////////////////////////////////////////////////")
print("Total billed...")
total = list(ecommerce_views.aggregate_by_product())
print(total[0].get('count'))

print("////////////////////////////////////////////////////////////////////////////////////////////")
print("Total billed by category...")
ecommerce_views.print_total_price_by_category(ecommerce_views.aggregate_by_category())
