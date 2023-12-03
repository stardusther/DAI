import logging

from ninja_extra import NinjaExtraAPI, api_controller, http_get, http_post, http_put, http_delete, \
    http_patch
from bson.objectid import ObjectId
from ninja.security import django_auth, django_auth_superuser

# App imports
from etienda import views as etienda_views
from etienda import serializers as etienda_serializers
from ecommerce import functions as ecommerce_functions

api = NinjaExtraAPI(csrf=True)
logger = logging.getLogger(__name__)


# function based definition
# @api.post("/login", tags=['Auth'])
# def login(request, username: str, password: str):
#     """Login"""
#     return
# # @api.get("/add", tags=['Math'])
# # def add(request, a: int, b: int):
# #     return {"result": a + b}

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
               auth=django_auth_superuser,
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
              auth=django_auth_superuser,
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
                 auth=django_auth_superuser,
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


api.register_controllers(
    ProductAPI
)
