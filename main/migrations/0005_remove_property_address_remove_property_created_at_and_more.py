# Generated by Django 5.1.1 on 2024-10-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_booking_userprofile_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='address',
        ),
        migrations.RemoveField(
            model_name='property',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='property',
            name='description',
        ),
        migrations.RemoveField(
            model_name='property',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='property',
            name='number_of_bathrooms',
        ),
        migrations.RemoveField(
            model_name='property',
            name='number_of_bedrooms',
        ),
        migrations.RemoveField(
            model_name='property',
            name='number_of_guests',
        ),
        migrations.RemoveField(
            model_name='property',
            name='price_per_night',
        ),
        migrations.RemoveField(
            model_name='property',
            name='title',
        ),
        migrations.AddField(
            model_name='property',
            name='Amenities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Category',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Contact',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Hotel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Image_URL',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Page_URL',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Price',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='Address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
