# Generated by Django 4.2.1 on 2023-05-22 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0004_alter_product_date_alter_review_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]