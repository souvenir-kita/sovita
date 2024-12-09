from django.urls import path
from promo.views import *

app_name = "promo"

urlpatterns = [
    path("", show_promo, name="show_promo"),
    path('json/', show_json, name='show_json'),
    path('show_json_by_id/',show_json_by_id, name = 'show_json_by_id'),
    path('add-promo', add_promo, name='add_promo'),
    path('view_promo_admin/<uuid:id>', view_promo_admin, name='view_promo_admin'),
    path('delete/<uuid:id>', delete_promo, name='delete_promo'),
    path('edit_promo/<uuid:pk>/', edit_promo, name='edit_promo'),
    path('json/kode/<str:kode>/', show_json_by_kode, name='show_json_by_kode'),
    path('json_api/', json_api, name='json_api'),
    path('create-flutter/', create_promo_flutter, name='create_flutter'),
    path('edit-flutter/<uuid:pk>/',edit_promo_flutter, name='edit_flutter'),
    path('delete-flutter/<uuid:pk>/',delete_promo_flutter, name='delete_flutter')
]
