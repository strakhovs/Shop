from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignIn, SignUp

app_name = "shop_api"

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
]
