
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new_post/", views.new_post, name= "new_post"),
    path("profile/<username>", views.profile_view, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("likepost", views.like_post_view, name="like-post"),
    path("comment", views.comment_view, name="comment-on-post"),
    path("likecomment", views.like_comment_view, name="like-comment"),
    path("follow", views.follow_view, name="follow-view"),
    path("following", views.following_view, name="following-view"),
]




