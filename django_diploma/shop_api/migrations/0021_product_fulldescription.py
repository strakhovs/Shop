# Generated by Django 4.2.1 on 2023-07-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0020_product_on_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='fullDescription',
            field=models.TextField(default='', max_length=500, verbose_name='full description'),
        ),
    ]
