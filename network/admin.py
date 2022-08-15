from django.contrib import admin

from network.models import Post, User

admin.site.register([
    User,
    Post
])
