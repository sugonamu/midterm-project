# Generated by Django 5.1.1 on 2024-10-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0003_alter_transaction_payment_method_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("VIRTUAL_ACCOUNT", "Virtual Account"),
                    ("CREDIT_CARD", "Credit Card"),
                ],
                default="CREDIT_CARD",
                max_length=255,
            ),
        ),
    ]
