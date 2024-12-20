from django.urls import path

from authentication.views import *

app_name = "authentication"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    # path("landing/", landing_page, name="landing_page"),
    path('api-login/', api_login, name='api-login'),
    path('api-register/', api_register, name='api-register'),
    path('api-logout/', api_logout, name='api-logout'),
    path('user-profile/', user_profile_json, name='user_profile_json'),
]
