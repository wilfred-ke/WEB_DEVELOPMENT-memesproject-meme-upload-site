from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import uuid
import os
import magic
import moviepy.editor as mp


ext_validator = FileExtensionValidator(['.png', '.jpg', '.jpeg', '.mp4', '.mkv', '.webm', '.avi', '.mov', '.gif'])
User = get_user_model()

def validate_file_mimetype(file):
    accept = ['image/png', 'image/jpg', 'image/jpeg', 'video/mp4', 'video/webm', 'video/avi', 'video/mov', 'video/gif', 'image/gif', 'video/mkv']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError("Unsupported file format")

class TheProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to="profile_images/", default='blank_pic.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

def generate_uuid():
    return str(uuid.uuid4())

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="post_images/", null=False, validators=[ext_validator, validate_file_mimetype])
    caption = models.TextField(max_length=200, editable=True, default='...')
    date = models.DateTimeField(default=datetime.now, editable=False)
    likes = models.IntegerField(default=0)

    def clean(self):
        if self.file and self.file.name.endswith(('.mp4', '.avi', '.mov', '.webm', '.mkv')):
            video = mp.VideoFileClip(self.file.path)
            if video.duration > 60:
                raise ValidationError("Video cannot be longer than 1 minute.")

    def save(self, *args, **kwargs):
        # Set is_image and is_video attributes based on file extension
        _, ext = os.path.splitext(self.file.name)
        if ext.lower() in ['.jpg', '.jpeg', '.png']:
            self.is_image = True
            self.is_video = False
        elif ext.lower() in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            self.is_image = False
            self.is_video = True
        else:
            # Handle other file types if needed
            pass

        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.user.username

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


class Comment(models.Model):
    file = models.ForeignKey(Image, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


    def __str__(self):
        return f'Comment by {self.user.username} on {self.file.id}'
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:20]}'

class HiddenPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Image, on_delete=models.CASCADE)
    hidden_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
