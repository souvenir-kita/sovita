from django.urls import path
from adminview.views import show_admin, edit_product, delete_product, show_xml, show_json, show_xml_by_id, show_json_by_id, create_product_ajax

app_name = 'adminview'

urlpatterns = [
    path('', show_admin, name="show_admin"),
    path('edit/<uuid:id>/', edit_product, name="edit_product"),
    path('delete/<uuid:id>/', delete_product, name="delete_product"),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('create-product-ajax/', create_product_ajax, name='create_product_ajax'),
]