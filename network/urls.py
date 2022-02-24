
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user>", views.user_profile, name="user_profile"),
    path("profile", views.profile, name="profile"),
    path("posts", views.posts, name="posts"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path("liked_post/", views.liked_post, name="liked_post"),
    path("likes/<int:user>", views.likedposts_page, name="likedposts_page"),
    path("follow_post/", views.follow_post, name="follow_post"),
    path("following", views.following_page, name="following")
]
