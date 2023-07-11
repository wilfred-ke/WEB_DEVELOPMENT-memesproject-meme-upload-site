from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import datetime


class Image(models.Model):
    caption = models.CharField(max_length=200, editable=True, default='meme')
    photo = models.ImageField(upload_to="media/")
    date = models.DateTimeField(default=datetime.now, editable=False)
    
    def __str__(self):
        return self.caption