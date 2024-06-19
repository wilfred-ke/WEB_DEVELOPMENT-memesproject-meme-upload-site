from django.contrib import admin
from .models import Image, LikeImage, TheProfile, FollowersCount, HiddenPost, Comment, RecentSearch

admin.site.register(Image)
admin.site.register(LikeImage)
admin.site.register(TheProfile)
admin.site.register(FollowersCount)
admin.site.register(HiddenPost)
admin.site.register(Comment)
admin.site.register(RecentSearch)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'date','caption']
    date_hierarchy = 'date'
    search_fields = ['user', 'caption', 'date']
