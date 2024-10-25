from django.urls import path
from .views import *

appname = "wishlist"

URLPATTERNS = [
    path('', wishlist_view, name='show_wishlist'),
    path('wishlist/toggle/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
]