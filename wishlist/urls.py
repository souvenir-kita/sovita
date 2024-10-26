from django.urls import path
from .views import *

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('toggle/<uuid:product_id>/', toggle_wishlist, name='toggle_wishlist'),
]