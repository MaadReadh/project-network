
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/create", views.create_post, name="create_post"), 
    path("post/edit", views.edit_post, name="edit_post"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
]
