from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import datetime


class Image(models.Model):
    caption = models.CharField(max_length=200, editable=True, default='meme')
    photo = models.ImageField(upload_to="media/")
    date = models.DateTimeField(default=datetime.now, editable=False)
    likes = models.ManyToManyField(User, related_name="meme_like")
    dislikes = models.ManyToManyField(User, related_name="meme_dislike")

    # keep track or count of likes and dislikes
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()
    
    def __str__(self):
        return self.caption