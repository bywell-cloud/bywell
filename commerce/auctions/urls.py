from django.urls import path
from . import views

#app_name = 'auctions'
urlpatterns = [ 
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category/<int:id>/", views.category_single , name="categorysingle"),
    path("list/<int:id>/",views.list_single, name="listsingle"),
    path("submitbid/<int:id>/", views.submitbid, name="submitbid"),
    path("comment/<int:id>/" , views.comment , name = "comment"),
    path("closing/<int:id>/",views.closing_list , name="closelist"),
    path("create/" , views.create , name="create") ,
    path("winners/", views.winners , name="winners"),
    path("whishlist/<int:id>",views.whishlist , name="whishlist")  , 
    path("remove/<int:id>",views.remove , name="remove") , 
    path("view/<int:id>/<int:us_id>/",views.view , name="view") ,
    path("whishlistadd/<int:id>/",views.whishlistadd , name="whishlistadd")
]
