# Generated by Django 4.1.3 on 2022-11-20 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightprice',
            name='legId',
            field=models.TextField(db_index=True),
        ),
    ]
