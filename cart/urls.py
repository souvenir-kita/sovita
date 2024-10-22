from django.urls import path
from .views import *
from . import views

app_name = 'cart'

urlpatterns = [
    path('', show_cart, name='show_cart'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('add/<uuid:id>/', views.add_product_to_cart, name='add_product_to_cart'),
]