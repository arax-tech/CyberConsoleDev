# Generated by Django 4.1.7 on 2023-06-07 14:06

import authentication.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("company", models.CharField(max_length=255)),
                ("group", models.CharField(max_length=255)),
                ("team", models.CharField(max_length=255, null=True)),
                ("company_name", models.CharField(max_length=255, null=True)),
                ("name", models.CharField(max_length=255)),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email"
                    ),
                ),
                ("address_first_line", models.CharField(max_length=255, null=True)),
                ("address_second_line", models.CharField(max_length=255, null=True)),
                ("address_town_city", models.CharField(max_length=255, null=True)),
                ("address_country_code", models.CharField(max_length=255, null=True)),
                ("address_country", models.CharField(max_length=255, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Admin", "Admin"),
                            ("Company", "Company"),
                            ("Client", "Client"),
                            ("Team", "Team"),
                        ],
                        default="Company",
                        max_length=255,
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="profile/placeholder.jpg",
                        upload_to=authentication.models.upload_to,
                        verbose_name="Image",
                    ),
                ),
                ("last_login", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
