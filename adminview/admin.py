from django.contrib import admin
from adminview.models import Product
from authentication.models import UserProfile

admin.site.register(UserProfile)
admin.site.register(Product)
