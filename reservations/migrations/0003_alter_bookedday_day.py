# Generated by Django 5.0.4 on 2024-05-22 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0002_bookedday"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookedday",
            name="day",
            field=models.DateField(),
        ),
    ]
