from datetime import datetime

import django.utils.timezone
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, verbose_name='name')


class Specification(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    value = models.CharField(max_length=100, verbose_name='value')


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    title = models.CharField(max_length=250, verbose_name='title')
    image = models.ImageField(verbose_name='image')


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price', default=0)
    count = models.IntegerField(verbose_name='count', default=0)
    date = models.DateTimeField(verbose_name='date', default=django.utils.timezone.now)
    title = models.CharField(max_length=50, verbose_name='title', default='')
    description = models.TextField(max_length=250, verbose_name='description')
    freeDelivery = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name='tags')
    specifications = models.ManyToManyField(Specification, related_name='specifications')


class Image(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    image = models.ImageField(verbose_name='image')
    src = models.CharField(max_length=250, verbose_name='src')
    alt = models.CharField(max_length=50, verbose_name='alt')


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product id')
    author = models.CharField(max_length=200, verbose_name='author')
    email = models.EmailField(verbose_name='email')
    text = models.TextField(max_length=250, verbose_name='text')
    rate = models.IntegerField(verbose_name='rate')
    date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date')
