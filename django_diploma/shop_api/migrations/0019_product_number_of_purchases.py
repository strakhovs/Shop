# Generated by Django 4.2.1 on 2023-07-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0018_remove_image_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_purchases',
            field=models.IntegerField(default=0, verbose_name='number of purchases'),
        ),
    ]
