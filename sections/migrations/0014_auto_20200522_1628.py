# Generated by Django 3.0.3 on 2020-05-22 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0013_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
