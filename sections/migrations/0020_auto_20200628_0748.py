# Generated by Django 3.0.3 on 2020-06-28 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0019_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
