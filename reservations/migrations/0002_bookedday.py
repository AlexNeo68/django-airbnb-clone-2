# Generated by Django 5.0.4 on 2024-05-22 04:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookedDay",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("day", models.DateTimeField()),
                (
                    "reservation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="booked_days",
                        to="reservations.reservation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Booked Day",
                "verbose_name_plural": "Booked Days",
            },
        ),
    ]
