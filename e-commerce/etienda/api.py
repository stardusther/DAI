import logging

from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post, http_put, http_delete, \
    http_patch
from bson.objectid import ObjectId
from ninja.security import django_auth, django_auth_superuser

# App imports
from etienda import serializers as etienda_serializers
from ecommerce import functions as ecommerce_functions
from ecommerce import views as ecommerce_views

api = NinjaExtraAPI(csrf=True)
logger = logging.getLogger(__name__)


# function based definition
@api.post("/login", tags=['Auth'])
def login(request, username: str, password: str):
    """Login"""
    data = {'username': username, 'password': password}
    request.data = data
    response = ecommerce_views.login(request)
    logger.debug(f'Login response: {response}')
    # token = response.json().get('token')
    return {'token': 0}


# class based definition
@api_controller('/', tags=['Products'], permissions=[])
class ProductAPI:
    @http_get("/product/{id}", response={200: etienda_serializers.ProductSerializer,
                                         404: etienda_serializers.MessageSerializer})
    def get_product(self, request, id: str):
        """Get a product"""
        try:
            db_product = ecommerce_functions.get_product_collection().find_one(
                {"_id": ObjectId(id)})

            if not db_product:
                logger.error(f'Product not found')
                return {"message": "Product not found"}, 404
            else:
                logger.debug(f'Product: {db_product}')
                return etienda_serializers.ProductSerializer(**db_product)
        except Exception as err:
            logger.error(f'Something went wrong while getting the product: {err}')
            return {"message": "Product not created"}, 404

    # Get products with ids between two numbers
    @http_get("/product", response={200: etienda_serializers.ProductSerializer,
                                    404: etienda_serializers.MessageSerializer})
    def get_products(self, request, lower_id: int, upper_id: int):
        """Get products with ids between two numbers"""
        try:
            products = []
            for i in range(lower_id, upper_id):
                db_product = ecommerce_functions.get_product_collection().find_one(
                    {"_id": ObjectId(i)})
                products.append(db_product)
            return etienda_serializers.ProductSerializer(products, many=True)
        except Exception as err:
            logger.error(f'Something went wrong while getting the product: {err}')
            return {"message": "Products not found"}, 404

    @http_post("/product",
               # auth=django_auth_superuser,
               response={200: etienda_serializers.ProductSerializer,
                         500: etienda_serializers.MessageSerializer}
               )
    def create_product(self, request, product: etienda_serializers.CreateProductSerializer):
        """Create a product"""

        try:
            # Turn id into a string for mongodb to accept it
            
            inserted = ecommerce_functions.get_product_collection().insert_one(product.dict())
            logger.debug(f'Creating product: {inserted.inserted_id}')
            db_product = ecommerce_functions.get_product_collection().find_one(
                {"_id": inserted.inserted_id})
            product_instance = etienda_serializers.ProductSerializer(**db_product)
            return product_instance
        except Exception as err:
            logger.error(f'Something went wrong while creating the product: {err}')
            return {"message": "Product not created"}

    @http_put("/product/{id}",
              # auth=django_auth_superuser,
              response={200: etienda_serializers.ProductSerializer,
                        500: etienda_serializers.MessageSerializer})
    def update_product(self, request, id: str,
                       product: etienda_serializers.CreateProductSerializer):
        """Update a product"""

        try:
            updated_product = ecommerce_functions.get_product_collection().update_one(
                {"_id": ObjectId(id)},  # Queryset Filter
                {"$set": product.dict(exclude_unset=True)}  # Updated data
            )

            if updated_product.modified_count > 0:
                logger.debug(f'Updated product: {id}')
                db_product = ecommerce_functions.get_product_collection().find_one(
                    {"_id": ObjectId(id)})
                product_instance = etienda_serializers.ProductSerializer(**db_product)
                return product_instance
        except Exception as err:
            logger.error(f'Something went wrong while updating the product: {err}')
            return {"message": "Product not found"}, 404

    @http_delete("/product/{id}",
                 auth=django_auth,
                 response={200: etienda_serializers.MessageSerializer,
                           500: etienda_serializers.MessageSerializer})
    def delete_product(self, request, id: str):
        """Delete a product"""

        try:
            ecommerce_functions.get_product_collection().delete_one({"_id": ObjectId(id)})
            return {"message": "Product deleted"}
        except Exception as err:
            logger.error(f'Something went wrong while deleting the product: {err}')
            return {"message": "Product deletion failed"}

    @http_patch("/product/{id}/rating", response={200: etienda_serializers.MessageSerializer,
                                                  404: etienda_serializers.MessageSerializer})
    def update_product_rating(self, request, id: str, rating: int):
        """Update the rating of a product"""
        try:
            db_product = ecommerce_functions.get_product_collection().find_one(
                {"_id": ObjectId(id)})
            logger.debug(f'In UPDATE Product: {db_product}')

            if not db_product:
                logger.error(f'Product not found')
                return {"message": "Product not found"}, 404

            old_rating = db_product.get('rating', {})
            old_count = old_rating.get('count', 0)
            old_rate = old_rating.get('rate', 0.0)
            user_rate = rating

            # Update the rating data
            new_count = old_count + 1
            new_rate = round(((old_rate * old_count) + user_rate) / new_count, 1)

            # Update the product's rating in the database
            updated_product = ecommerce_functions.get_product_collection().update_one(
                {"_id": ObjectId(id)},
                {"$set": {"rating.count": new_count, "rating.rate": new_rate, "rating.user_rate": user_rate}}
            )

            if updated_product.modified_count > 0:
                logger.debug(f'Updated rating of product: {id}')
                return {"message": "Product rating updated"}
        except Exception as err:
            logger.error(f'Something went wrong while updating the product rating: {err}')
            return {"message": "Product rating update failed"}, 500


api.register_controllers(
    ProductAPI
)
