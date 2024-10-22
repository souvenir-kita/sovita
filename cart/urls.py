from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', show_cart, name='show_cart'),
    path('xml-cart/', show_xml, name='show_xml'),
    path('json-cart/', show_json, name='show_json'),
    path('xml-cart/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json-cart/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add-cart/<uuid:id>/', add_product_to_cart, name="add_product_to_cart"),
]