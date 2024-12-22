from django.urls import path
from review.views import *

app_name = 'review'

urlpatterns = [
    path('<uuid:id>/', show_review, name='show_review'),
    path('create-review/<uuid:id>/', create_review , name='create_review'),
    path('edit-review/<uuid:id>/', edit_review, name='edit_review'),
    path('delete-review/<uuid:id>/', delete_review, name='delete_review'),
    path('json/', show_json_all, name='show_json_all'),
    path('json/<uuid:product_id>/', show_json, name='show_json'),
    path('create-flutter/<uuid:product_id>/', create_review_flutter, name='create_review_flutter'),
    path('edit-flutter/<str:product_id>/', edit_review_flutter, name='edit_review_flutter'),
    path('delete-flutter/<str:product_id>/', delete_review_flutter, name='delete_review_flutter'),
    path('product/<uuid:product_id>/reviews/', get_product_reviews, name='get_product_reviews'),

]