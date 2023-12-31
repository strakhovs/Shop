# Generated by Django 4.2.1 on 2023-07-02 10:42

from django.db import migrations, models
import shop_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0016_alter_category_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_limited',
            field=models.BooleanField(default=False, verbose_name='is limited'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=shop_api.models.product_image_directory_path, verbose_name='image'),
        ),
    ]
