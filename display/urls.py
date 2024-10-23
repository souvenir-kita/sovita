from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from display.views import display_main, create_product, delete_product, view_product, edit_product, create_product_ajax
from display.views import show_xml, show_json, show_xml_by_id, show_json_by_id


app_name = 'display'

urlpatterns = [
    path('', display_main, name='display_main'),
    # path('create-product/', create_product, name='create_product'),
    path('delete/<uuid:id>/', delete_product, name='delete_product'),
    path('view/<uuid:id>/', view_product, name="view_product"),
    path('edit/<uuid:id>/', edit_product, name="edit_product"),
    path('create-product-ajax/', create_product_ajax, name='create_product_ajax'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]

