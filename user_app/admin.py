from django.contrib import admin
from .models import Profile
# from modeltranslation.admin import TranslationAdmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'age', 'sex', 'seeking', 'city')
