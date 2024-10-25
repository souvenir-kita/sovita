from django.urls import path
from adminview.views import show_admin

app_name = 'adminview'

urlpatterns = [
    path('', show_admin, name="show_admin"),
]