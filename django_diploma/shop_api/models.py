from datetime import datetime

import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='name')

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    value = models.CharField(max_length=100, verbose_name='value')

    def __str__(self):
        return self.name


class Category(models.Model):

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    title = models.CharField(max_length=50, verbose_name='category')
    image = models.ImageField(null=True, upload_to="categories/", verbose_name='image')
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               db_index=True,
                               related_name='subcategories')

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    count = models.IntegerField(verbose_name='count', default=0)
    date = models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)
    title = models.CharField(max_length=50, verbose_name='title', default='')
    description = models.TextField(max_length=250, verbose_name='description')
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tags')
    specifications = models.ManyToManyField(Specification, related_name='specifications')
    is_limited = models.BooleanField(verbose_name='is limited', default=False)

    def __str__(self):
        return self.title


def product_image_directory_path(instance, filename):
    return "products/{pk}/{filename}".format(pk=instance.pk, filename=filename)


class Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    image = models.ImageField(upload_to=product_image_directory_path, verbose_name='image')
    src = models.CharField(max_length=250, verbose_name='src')
    alt = models.CharField(max_length=50, verbose_name='alt')


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    author = models.CharField(max_length=200, verbose_name='author')
    email = models.EmailField(verbose_name='email')
    text = models.TextField(max_length=250, verbose_name='text')
    rate = models.IntegerField(verbose_name='rate')
    date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')


def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "users/{pk}/avatar/{filename}".format(
        pk=instance.id,
        filename=filename,
    )


class Profile(models.Model):
    class Meta:
        verbose_name_plural = 'profiles'
        verbose_name = 'profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    fullName = models.CharField(max_length=100, null=False, blank=True)
    email = models.EmailField(null=False, blank=True)
    phone = models.CharField(max_length=15, blank=True, verbose_name='phone')
    # avatar = models.OneToOneField(Avatar, models.CASCADE, null=True, blank=True)
    #  avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path,
    #                          verbose_name='avatar')


class Avatar(models.Model):
    class Meta:
        verbose_name = 'avatar'
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE, verbose_name='user')
    avatar = models.ImageField(null=True, upload_to=profile_avatar_directory_path, verbose_name='avatar')
    src = models.CharField(max_length=100)
    alt = models.CharField(max_length=200)
