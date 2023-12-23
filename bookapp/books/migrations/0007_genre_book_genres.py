# Generated by Django 5.0 on 2023-12-23 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_order_book_order_price_delete_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='books.genre'),
        ),
    ]
