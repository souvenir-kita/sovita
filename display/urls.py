from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from display.views import display_main, create_product, delete_product, view_product, edit_product
from cart.views import add_product_to_cart, show_cart

app_name = 'display'

urlpatterns = [
    path('', display_main, name='display_main'),
    path('create-product/', create_product, name='create_product'),
    path('delete/<uuid:id>/', delete_product, name='delete_product'),
    path('view/<uuid:id>/', view_product, name="view_product"),
    path('edit/<uuid:id>/', edit_product, name="edit_product"),
    path('add-cart/<uuid:id>/', add_product_to_cart, name="add_product_to_cart"),
    path('show-cart/', show_cart, name="show_cart"),
]
