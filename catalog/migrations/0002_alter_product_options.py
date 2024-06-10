# Generated by Django 5.0.6 on 2024-06-06 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('cancel_product_publication', 'Can cancel product publication'), ('change_product_description', 'Can change product description'), ('change_product_category', 'Can change product category')], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]