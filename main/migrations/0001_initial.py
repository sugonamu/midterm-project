# Generated by Django 5.1 on 2024-10-22 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Hotel",
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
                ("title", models.CharField(max_length=255)),
                ("address", models.TextField(blank=True)),
                ("contact", models.CharField(blank=True, max_length=255)),
                ("price", models.CharField(max_length=50)),
                (
                    "rating",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Rating from 1.0 to 5.0",
                        max_digits=3,
                    ),
                ),
                ("amenities", models.TextField(blank=True)),
                ("location", models.CharField(max_length=255)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("slug", models.SlugField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotels",
                        to="main.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Hotels",
                "ordering": ("-created",),
            },
        ),
    ]
