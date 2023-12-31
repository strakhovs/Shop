# Generated by Django 4.2.1 on 2023-05-22 21:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('image', models.ImageField(upload_to='', verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('count', models.IntegerField(default=0, verbose_name='count')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 5, 22, 21, 1, 33, 293091), verbose_name='date')),
                ('title', models.CharField(default='', max_length=50, verbose_name='title')),
                ('description', models.TextField(max_length=250, verbose_name='description')),
                ('freeDelivery', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop_api.category', verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('value', models.CharField(max_length=100, verbose_name='value')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200, verbose_name='author')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('text', models.TextField(max_length=250, verbose_name='text')),
                ('rate', models.IntegerField(verbose_name='rate')),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 5, 22, 21, 1, 33, 294785), verbose_name='date')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_api.product', verbose_name='product id')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='specifications',
            field=models.ManyToManyField(related_name='specifications', to='shop_api.specification'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_name='tags', to='shop_api.tag'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='image')),
                ('src', models.CharField(max_length=250, verbose_name='src')),
                ('alt', models.CharField(max_length=50, verbose_name='alt')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_api.product', verbose_name='product id')),
            ],
        ),
    ]
