import views as ecommerce_views

# Set the api URL for the
api = 'https://fakestoreapi.com/products'


ecommerce_views.truncateDatabase()  # Empty database

print("Importing database from:", api)
products = ecommerce_views.getProducts(api)
ecommerce_views.storeProducts(products)  # Fill database
print("Finding electronic products between 100 and 200 euros, ordered by price...")
result = ecommerce_views.filterProduct(None, None, 100, 200, None, 'price')
print(result)
print("Finding products containing the word 'pocket' in the description...")

print("Finding products with a score greater than 4...")

print("Finding men's clothing, sorted by score...")






