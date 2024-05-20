from django.contrib import admin
from .models import Image, LikeImage, TheProfile, FollowersCount

admin.site.register(Image)
admin.site.register(LikeImage)
admin.site.register(TheProfile)
admin.site.register(FollowersCount)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'date','caption']
    date_hierarchy = 'date'
    search_fields = ['user', 'caption', 'date']
