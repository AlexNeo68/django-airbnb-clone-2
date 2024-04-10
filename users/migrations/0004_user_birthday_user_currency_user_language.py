# Generated by Django 5.0.4 on 2024-04-09 20:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_user_avatar_user_gender_alter_user_bio"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="birthday",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="currency",
            field=models.CharField(
                blank=True,
                choices=[("rub", "RUB"), ("usd", "USD")],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                blank=True,
                choices=[("ru", "Russian"), ("en", "English")],
                max_length=2,
                null=True,
            ),
        ),
    ]
