from django.contrib import admin
from django.contrib.auth.models import User

from .models import Product, Tag, Specification, Category, Profile, Avatar


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = "title", "description", "price", "freeDelivery", "category_id", "count", "date"


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
