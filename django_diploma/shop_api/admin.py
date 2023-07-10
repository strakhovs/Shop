from django.contrib import admin
from django.contrib.auth.models import User

from .models import Product, Tag, Specification, Category, Profile, Avatar, Image, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "title", "description", "price", "freeDelivery", "category_id", "count", "date"


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = "product_id", "image"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = "name",


@admin.register(Specification)
class SpecAdmin(admin.ModelAdmin):
    list_display = "name", "value"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "title", "image"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "phone", "user_id"


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = "avatar", "src"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = "product_id", "author", "email", "text", "rate", "date"

