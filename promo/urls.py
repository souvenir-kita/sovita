from django.urls import path
from promo.views import *

app_name = "promo"

urlpatterns = [
    path("", show_promo, name="show_promo"),
    path('json/', show_json, name='show_json'),
    path('add-promo', add_promo, name='add_promo'),
]
