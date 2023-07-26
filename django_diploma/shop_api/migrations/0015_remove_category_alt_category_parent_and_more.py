# Generated by Django 4.2.1 on 2023-06-08 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0014_category_alt_alter_category_image_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='alt',
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='shop_api.category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, verbose_name='title'),
        ),
    ]