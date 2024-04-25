from django.contrib import admin
from .models import Image, Profile

admin.site.register(Image)
admin.site.register(Profile)

class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'date','caption']
