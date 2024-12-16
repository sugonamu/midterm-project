from django.contrib import admin

from authentication.models import UserProfile, Property

admin.site.register(UserProfile)
admin.site.register(Property)