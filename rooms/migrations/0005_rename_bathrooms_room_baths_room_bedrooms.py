# Generated by Django 5.0.4 on 2024-04-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0004_alter_amenity_options_alter_facility_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="room",
            old_name="bathrooms",
            new_name="baths",
        ),
        migrations.AddField(
            model_name="room",
            name="bedrooms",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
