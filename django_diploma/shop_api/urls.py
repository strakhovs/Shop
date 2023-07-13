from django.contrib.auth.views import LogoutView

from django.urls import path

from .views import SignIn, SignUp, ProfileView, AvatarUpdateView, PasswordUpdateView, CategoriesView, TagsView, \
    LimitedProductsView, PopularProductsView, BannersView, CatalogView, CategoryCatalogView, ProductView

app_name = "shop_api"

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/avatar/', AvatarUpdateView.as_view(), name='avatar_update'),
    path('profile/password/', PasswordUpdateView.as_view(), name='password_update'),
    path('categories/', CategoriesView.as_view()),
    path('tags/', TagsView.as_view()),
    path('products/limited/', LimitedProductsView.as_view()),
    path('products/popular/', PopularProductsView.as_view()),
    path('banners/', BannersView.as_view()),
    path('catalog/', CatalogView.as_view()),
    path('catalog/<int:category>/', CategoryCatalogView.as_view()),
    path('product/<int:product_id>/', ProductView.as_view()),
]
