from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addproject/", views.addproject, name="addproject"),
    path("view/<int:id>/", views.view, name="view"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("assign/<int:id>/", views.assign, name="assign"),
    path("action/<int:id>/", views.action, name="action"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("deletepr/<int:id>/", views.deletepr, name="deletepr"),
    path("compose/<int:id>/", views.compose, name="compose"),
    path("search/<int:id>/", views.search, name="search")
]






