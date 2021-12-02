from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry_page, name ="entry"),
    path("create/", views.create, name ="create"),
    path("radpick/", views.radpick, name ="radpick"),
    path("wiki/edit/<str:title2>/", views.edit, name ="edit"),
    path("search/", views.search, name ="search")
]