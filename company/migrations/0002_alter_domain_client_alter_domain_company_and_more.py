# Generated by Django 4.1.7 on 2023-06-15 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="domain",
            name="client",
            field=models.ForeignKey(
                db_column="client",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="domain_client",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="domain",
            name="company",
            field=models.ForeignKey(
                db_column="company",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="domain_company",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="domain",
            name="group",
            field=models.ForeignKey(
                db_column="group",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="domain_group",
                to="company.group",
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="user",
            field=models.ForeignKey(
                db_column="user",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="log_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]