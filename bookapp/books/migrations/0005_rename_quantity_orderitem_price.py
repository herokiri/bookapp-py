# Generated by Django 5.0 on 2023-12-23 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quantity',
            new_name='price',
        ),
    ]
