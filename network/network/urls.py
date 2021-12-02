
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("test/", views.test, name="test"),
    path("editpost/<int:id>/", views.editpost, name="editpost"),
    path("likesadd/<int:id>/", views.likesadd, name="likesadd"),
    path("follow/<int:id>/", views.follow, name="follow"),
    path("following/", views.following, name="following"),
    path("unfollow/<int:id>/", views.unfollow, name="unfollow"),
    path("profile/<int:id>/", views.profile, name="profile")
]
