from django.urls import path
from .views import *

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('toggle/<uuid:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('add-wishlist/', add_wishlist_flutter, name='add_wishlist_flutter'),
    path('edit-wishlist/', update_wishlist_flutter, name='add_wishlist_flutter'),
    path('remove-wishlist/<uuid:product_id>/', remove_wishlist_flutter, name='remove_wishlist_flutter'),
    path('json/', show_json, name='json'),
]