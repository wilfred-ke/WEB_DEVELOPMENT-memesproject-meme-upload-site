from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

class TheProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to="profile_images/", default='blank_pic.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images/")
    caption = models.TextField(max_length=200, editable=True, default='funny')
    date = models.DateTimeField(default=datetime.now, editable=False)
    likes = models.IntegerField(default=0)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.user

class LikeImage(models.Model):
    image_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username  

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
                    