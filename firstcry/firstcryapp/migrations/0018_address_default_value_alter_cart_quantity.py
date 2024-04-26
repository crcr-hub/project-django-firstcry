# Generated by Django 4.2.7 on 2023-12-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstcryapp', '0017_alter_products_gender_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default_value',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
