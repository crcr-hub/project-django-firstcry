# Generated by Django 4.2.7 on 2024-04-08 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstcryapp', '0074_alter_return_product_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='return_order',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
