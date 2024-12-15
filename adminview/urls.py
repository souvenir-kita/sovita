from django.urls import path
from adminview.views import show_admin, edit_product, delete_product, show_xml, show_json, show_xml_by_id, show_json_by_id, create_product_ajax, show_json_random, create_product_flutter, update_flutter, delete_flutter

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
    path('create-flutter/', create_product_flutter, name = "create_product_flutter"),
    path('update-flutter/<uuid:id>/', update_flutter, name='update_flutter'),
    path('json-random/', show_json_random, name="show_json_random"),
    path('delete-flutter/<uuid:id>/', delete_flutter, name='delete_flutter'),
]