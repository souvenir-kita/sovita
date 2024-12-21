from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', show_cart, name='show_cart'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('all-cart/', show_all_cart, name='show_all_cart'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add/<uuid:id>/', add_product_to_cart, name='add_product_to_cart'),
    path('add_with_note/<uuid:id>/', add_product_to_cart_with_note, name='add_product_to_cart_with_note'),
    path('edit/<uuid:id>/', edit_cart_product, name='edit_cart_product'),
    path('delete/<uuid:id>/', delete_cart_product, name='delete_cart_product'),
    path('inc_amount/<uuid:id>/', inc_amount, name='inc_amount'),
    path('dec_amount/<uuid:id>/', dec_amount, name='dec_amount'),
    path('update_note/<uuid:id>/', update_note, name='update_note'),
    path('sort/', sort_cart, name='sort_cart'),
    path('user-cart/', show_cart_json, name='show_cart_json'),
    path('user-json/<uuid:id>/', user_json, name='user_json'),
    path('user-cart-products/', user_cart_products, name='user_cart_products'),
]