# Generated by Django 5.1.1 on 2024-10-27 10:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0007_merge_20241027_1042"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("CREDIT_CARD", "Credit Card"),
                    ("VIRTUAL_ACCOUNT", "Virtual Account"),
                ],
                default="CREDIT_CARD",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                choices=[("PAID", "Paid"), ("UNPAID", "Unpaid")],
                default="UNPAID",
                max_length=255,
            ),
        ),
    ]
