# Generated by Django 3.0.3 on 2020-05-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0003_auto_20200509_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('men', 'men'), ('female', 'female'), ('bag', 'bag'), ('shoes', 'shoes'), ('watches', 'watches')], max_length=100),
        ),
    ]
