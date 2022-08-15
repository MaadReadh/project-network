from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers_count = models.IntegerField(default=0)
    followings_count = models.IntegerField(default=0)
    pass
   

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    likes_count = models.IntegerField(default=0)
    likes = models.ManyToManyField("User",related_name="likes",blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey("User",on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey("User",on_delete=models.CASCADE)
