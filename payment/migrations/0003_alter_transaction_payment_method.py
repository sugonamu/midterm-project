# Generated by Django 5.1.2 on 2024-10-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_transaction_booking_date_transaction_hotel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('CREDIT_CARD', 'Credit Card'), ('VIRTUAL_ACCOUNT', 'Virtual Account')], default='CREDIT_CARD', max_length=255),
        ),
    ]