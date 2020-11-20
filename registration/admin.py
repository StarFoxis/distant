from django.contrib import admin

from .models import Style, Profile
# Register your models here.

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('user', 'style')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')