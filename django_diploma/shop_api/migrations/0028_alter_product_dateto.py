# Generated by Django 4.2.1 on 2023-07-29 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0027_product_datefrom_product_dateto_product_saleprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dateTo',
            field=models.DateField(null=True),
        ),
    ]