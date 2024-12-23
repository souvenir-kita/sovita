from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from display.views import display_main, view_product
from display.views import show_xml, show_json, show_xml_by_id, show_json_by_id, search, to_landing, profile_view, search_flutter

from cart.views import add_product_to_cart, show_cart

app_name = 'display'

urlpatterns = [
    path('', to_landing, name='to_landing'),
    path('main/', display_main, name='display_main'),
    path('view/<uuid:id>/', view_product, name="view_product"),
    path('add-cart/<uuid:id>/', add_product_to_cart, name="add_product_to_cart"),
    path('show-cart/', show_cart, name="show_cart"),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('search/', search, name='search'),
    path('profile/', profile_view, name='profile'),
    path('search-flutter/<str:name>', search_flutter, name='search_flutter')
]

