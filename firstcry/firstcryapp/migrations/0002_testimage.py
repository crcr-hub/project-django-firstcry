# Generated by Django 4.2.7 on 2023-11-29 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstcryapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='testimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titile', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=800)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
            ],
        ),
    ]
